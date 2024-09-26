"""Implementation of the Kedro Expectations Hooks."""

import multiprocessing.process

import great_expectations as ge
import os
from typing import Any, Dict, cast, Callable

from great_expectations.checkpoint.checkpoint import CheckpointResult, Checkpoint
from great_expectations.core import (
    RunIdentifier,
    ExpectationSuiteValidationResult,
    ExpectationValidationResult,
    IDDict,
)
from great_expectations.core.batch import LegacyBatchDefinition
from great_expectations.data_context.types.resource_identifiers import (
    ValidationResultIdentifier,
    ExpectationSuiteIdentifier,
)
from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro_datasets.partitions.partitioned_dataset import PartitionedDataset
from kedro.pipeline.node import Node
from kedro.framework.context import KedroContext
from .notification import BaseNotifier
from .exceptions import SuiteValidationFailure
import importlib
from pandas import DataFrame as PandasDataFrame
from .utils import (
    dot_to_underscore,
    validate,
    get_suite_name,
    get_all_expectations,
    base_ge_folder_exists,
    location_is_kedro_root_folder,
    split_suite_name,
)


RUN_NAME = "kedro_expectations_auto_validation"


class KedroExpectationsCheckpointResult:

    def __init__(self, suite_name: str, run_results: dict, success: bool):
        self.suite_name = suite_name
        self.run_results = run_results
        self.success = success


class KedroExpectationsHooks:
    """Implementation of the Kedro Expectations Hooks."""

    def __init__(
        self,
        on_failure: str = "continue",
        check_orphan_expectation_suites: bool = True,
        single_datasource_check: bool = True,
        notify_config: BaseNotifier = None,
        expectation_tags: list[str] = None,
        parallel_validation: bool = False,
    ) -> None:
        """
        Note: These params will be overwritten if your parameters.yml contains hook_options. 

        :param on_failure: Defines what to do when a validation fails. Valid strings are "continue" (failures are \
            visible in the data docs), "raise_fast" (directly raise a SuiteValidationFailure) and "raise_later" (raise \
            a SuiteValidationFailure at the end of the pipeline run, containing information on all failures).
        :param check_orphan_expectation_suites: Boolean to sanity check, if all expectation suites have a \
            corresponding data source.
        :param single_datasource_check: Boolean if each datasource should only be checked once per run (in cases the \
            datasource is used as nodes' input multiple times)
        :param notify_config: Configuration for sending a summarizing notification message about the run, e.g. via email
        :param expectation_tags: List of tags used to filter which expectation suites will be used for validation.
        :param parallel_validation: Boolean to enable parallel validation of datasets. If enabled, each validation will \
            be run in a separate process and the pipeline can continue without waiting. Processes are joined at the end of \
            the pipeline run. NOTICE: This feature is only available for the "raise_later" and "continue" on_failure modes. \
            It ONLY WORKS if the node is run as part of a pipeline run, not in isolation. COPIES ALL INPUT DATA!!!
        """

        self.on_failure = on_failure
        self.check_orphan_expectation_suites = check_orphan_expectation_suites
        self.single_datasource_check = single_datasource_check
        self.expectation_tags = expectation_tags
        self.parallel_validation = parallel_validation

        self._run_id = None
        self._process_pool = []
        if parallel_validation:
            self._manager = multiprocessing.Manager()
            self._datasource_run_counter = self._manager.dict()
            self._fail_log = self._manager.list()
            self.checkpoint_results = self._manager.list()
        else:
            self._manager = None
            self.checkpoint_results = []
            self._fail_log = []
            self._datasource_run_counter = {}

        self._notifier = notify_config
        self._validation_runner = None

        self._run_init_assertions()
        self._build_validation_runner()

    def _build_validation_runner(self):
        self._validation_runner = ValidationRunner(
            on_failure=self.on_failure,
            single_datasource_check=self.single_datasource_check,
            datasource_run_counter=self._datasource_run_counter,
            expectation_tags=self.expectation_tags,
            run_id=self._run_id,
            notifier=self._notifier,
            fail_log=self._fail_log,
            checkpoint_results=self.checkpoint_results,
        )

    def _run_init_assertions(self):

        assert self.on_failure in ["continue", "raise_fast", "raise_later"], (
            f"Argument 'on_failure' has to be one of "
            f"'continue', 'raise_fast' or 'raise_later', "
            f"but was {self.on_failure}."
        )

        if self.on_failure == "raise_fast":
            assert (
                not self.parallel_validation
            ), "Parallel validation is not supported with 'raise_fast' on_failure mode."

    @hook_impl
    def after_context_created(self, context: KedroContext) -> None:
        config_loader = context.config_loader["parameters"]
        if "hook_options" not in config_loader:
            return

        hook_options = config_loader["hook_options"]

        self.on_failure = hook_options.get("on_failure", self.on_failure)
        self.check_orphan_expectation_suites = hook_options.get(
            "check_orphan_expectation_suites", self.check_orphan_expectation_suites
        )
        self.single_datasource_check = hook_options.get(
            "single_datasource_check", self.single_datasource_check
        )
        self.expectation_tags = hook_options.get(
            "expectation_tags", self.expectation_tags
        )
        self.parallel_validation = hook_options.get(
            "parallel_validation", self.parallel_validation
        )

        notifier_options = hook_options.get("notify_config", {})

        notifier_class = notifier_options.get("class")
        notifier_module = notifier_options.get("module")
        notifier_kwargs = notifier_options.get("kwargs")

        if notifier_class and notifier_module:
            try:
                module = importlib.import_module(notifier_module)
                notifier = getattr(module, notifier_class)
                self._notifier = notifier(**notifier_kwargs)
            except (ImportError, AttributeError) as e:
                print("Error while importing notifier: ", e)

        self._run_init_assertions()
        self._build_validation_runner()

    @hook_impl
    def after_catalog_created(
        self,
        catalog: DataCatalog,
        conf_catalog,
        conf_creds,
        feed_dict,
        save_version,
        load_versions,
    ) -> None:
        # Store the session id of the run for the validation result timestamp
        self._run_id = RunIdentifier(run_name="kedro_gx", run_time=None)
        self._validation_runner.run_id = self._run_id
        # Make sure each expectation suite has a corresponding dataset.
        if self.check_orphan_expectation_suites:
            gx = ge.get_context()
            exp_datasets = set(entry.name.split(".")[0] for entry in gx.suites.all())
            catalog_datasets = set(
                entry
                for entry in catalog.list()
                if not entry.startswith("params:") and entry != "parameters"
            )
            orphan_expectation_suites = exp_datasets - catalog_datasets
            if len(orphan_expectation_suites) > 0:
                msg = (
                    f"Found orphan expectation suites not corresponding to any dataset in the catalog: "
                    f"{orphan_expectation_suites}."
                )
                self._validation_runner.publish_failure_msg(msg=msg)

    @hook_impl
    def before_node_run(
        self,
        catalog: DataCatalog,
        inputs: Dict[str, Any],
        node: Node,
    ) -> None:
        """Validate inputs that are supported and have an expectation suite available."""
        if (
            self.before_node_run
            and base_ge_folder_exists(verbose=False)
            and location_is_kedro_root_folder()
        ):

            if not self.parallel_validation:
                self._validation_runner.catalog = catalog
                self._validation_runner.data = inputs
                self._validation_runner._run_validation()
                return

            name = node.name + "-" + "_".join(inputs.keys())
            process = multiprocessing.Process(
                target=KedroExpectationsHooks.create_and_run_validation_runner,
                args=(
                    catalog,
                    inputs,
                    self.on_failure,
                    self.single_datasource_check,
                    self._datasource_run_counter,
                    self.expectation_tags,
                    self._run_id,
                    self._notifier,
                    self._fail_log,
                    self.checkpoint_results,
                ),
                name=name,
            )
            process.start()
            self._process_pool.append(process)

    @hook_impl
    def after_pipeline_run(
        self, run_params: Dict, run_result, pipeline, catalog: DataCatalog
    ):
        if self.parallel_validation:
            print("Waiting for parallel validations to finish...", flush=True)

            for process in self._process_pool:
                print("Joining process: ", process.name, flush=True)
                process.join()

            print("Parallel validations finished!", flush=True)

        self._validation_runner.send_notification()

        # finally raise Exception if validations failed and option is set
        if self._fail_log:
            if self.on_failure == "raise_later":
                raise SuiteValidationFailure(
                    "During pipeline run one or more expectation suite validations failed:\n"
                    + "\n".join(self._fail_log)
                    + "\n"
                )
            else:
                print(
                    "During pipeline run one or more expectation suite validations failed:\n"
                    + "\n".join(self._fail_log)
                    + "\n"
                )

    @staticmethod
    def create_and_run_validation_runner(
        catalog: DataCatalog,
        inputs: Dict[str, Any],
        on_failure: str,
        single_datasource_check: bool,
        datasource_run_counter: dict,
        expectation_tags: list[str],
        run_id: RunIdentifier,
        notifier: BaseNotifier,
        fail_log: list[str],
        checkpoint_results: list[KedroExpectationsCheckpointResult],
    ):
        runner = ValidationRunner(
            on_failure=on_failure,
            single_datasource_check=single_datasource_check,
            datasource_run_counter=datasource_run_counter,
            expectation_tags=expectation_tags,
            run_id=run_id,
            notifier=notifier,
            fail_log=fail_log,
            checkpoint_results=checkpoint_results,
            catalog=catalog,
            inputs=inputs,
        )
        runner._run_validation()


class ValidationRunner:

    def __init__(
        self,
        on_failure: str,
        single_datasource_check: bool,
        datasource_run_counter: dict,
        expectation_tags: list[str],
        run_id: RunIdentifier,
        notifier: BaseNotifier,
        fail_log: list[str],
        checkpoint_results: list[KedroExpectationsCheckpointResult],
        catalog: DataCatalog = None,
        inputs: Dict[str, Any] = None,
    ):

        self.catalog = catalog
        self.data = inputs
        self.on_failure = on_failure
        self.single_datasource_check = single_datasource_check
        self.datasource_run_counter = datasource_run_counter
        self.expectation_tags = expectation_tags
        self.run_id = run_id
        self.notifier = notifier
        self.fail_log = fail_log
        self.checkpoint_results = checkpoint_results

    def _run_validation(self) -> None:
        ge_context = ge.get_context()
        for key, value in self.data.items():
            if (
                self.single_datasource_check
                and self.datasource_run_counter.get(key, 0) > 0
            ):
                # skip each further check after the first
                continue
            self.datasource_run_counter[key] = (
                self.datasource_run_counter.get(key, 0) + 1
            )
            catalog_key = key.replace(":", "__").replace(".", "__")
            adjusted_key = dot_to_underscore(key)

            if isinstance(
                getattr(self.catalog.datasets, catalog_key), PartitionedDataset
            ):
                partitions = cast(Dict[str, Callable], value)
            else:
                partitions = {adjusted_key: lambda: value}

            for casted_key, casted_value in partitions.items():
                # Looking for a general expectation
                current_key = adjusted_key
                all_expectations = get_all_expectations(
                    ge_context=ge_context, adjusted_key=current_key
                )
                ge_adjusted_key = current_key

                # Looking for a specific expectation
                if (
                    not all_expectations and casted_key != adjusted_key
                ):  # partition dataset
                    adjusted_key_pt2 = dot_to_underscore(casted_key)
                    current_key = os.path.join(adjusted_key, adjusted_key_pt2)
                    all_expectations = get_all_expectations(
                        ge_context=ge_context, adjusted_key=current_key
                    )
                    ge_adjusted_key = current_key + "." + adjusted_key_pt2

                # filter expactations for given tag
                expectations_filtered = []
                if self.expectation_tags is not None:
                    for expectation in all_expectations:
                        suite_name = get_suite_name(expectation, ge_adjusted_key)
                        file = ge_context.suites.get(suite_name)
                        if set(self.expectation_tags) & set(file["meta"]["tags"]):
                            expectations_filtered.append(expectation)

                    if not expectations_filtered:
                        print(
                            f"No expectation suite for tags {self.expectation_tags}.",
                            "Validation will be skipped!",
                        )
                else:
                    expectations_filtered = all_expectations

                for exp_file in expectations_filtered:
                    suite_name = get_suite_name(exp_file, ge_adjusted_key)
                    value = casted_value()
                    if isinstance(value, PandasDataFrame):
                        result = validate(
                            ge_context,
                            dataset_name=casted_key,
                            suite_name=suite_name,
                            validation_df=value,
                            run_id=self.run_id,
                        )
                        suite_name = result.name.replace("_kedro_checkpoint", "")
                        kedro_gx_result = KedroExpectationsCheckpointResult(
                            suite_name, result.run_results, result.success
                        )
                        self.checkpoint_results.append(kedro_gx_result)
                    else:
                        raise SuiteValidationFailure(
                            f"Dataset {adjusted_key} is no Pandas DataFrame and not supported by Kedro Expectations"
                        )
                    if not result.success:
                        msg = f"Suite {suite_name} for DataSet {current_key} failed!"
                        self.publish_failure_msg(
                            msg=msg,
                        )
                if not all_expectations:
                    print(
                        f'No expectation suite was found for "{key}".',
                        "Validation will be skipped!",
                    )

    def publish_failure_msg(self, msg: str):
        self.fail_log.append(msg)
        if self.on_failure == "raise_fast":
            self.send_notification()
            raise SuiteValidationFailure(msg)

    def send_notification(self):
        if self.notifier is not None and self.notifier.will_notify(
            len(self.fail_log) == 0
        ):
            # summarize the successful and failed validations for email report
            failed_validation_results: list[ExpectationValidationResult] = []
            failed_expectation_suite_results: dict[
                ExpectationSuiteIdentifier, ExpectationSuiteValidationResult
            ] = {}
            successful_expectations = 0
            evaluated_expectations = 0
            # payload = {"update_data_docs": {"class": "UpdateDataDocsAction"}}
            for checkpoint_result in self.checkpoint_results:
                suite_name = checkpoint_result.suite_name
                dataset_name, _ = split_suite_name(suite_name)

                for (
                    validation_result_id,
                    validation_result,
                ) in checkpoint_result.run_results.items():
                    validation_result: ExpectationSuiteValidationResult = (
                        checkpoint_result.run_results[validation_result_id]
                    )

                    if not validation_result.success:
                        # doc_key = "_".join(validation_result_id.to_tuple())
                        # doc_links = ge_context.get_docs_sites_urls(
                        #     resource_identifier=validation_result_id,
                        #     site_name="local_site",
                        # )
                        # if doc_links[0]["site_url"] is not None:
                        #     payload["update_data_docs"][doc_key] = doc_links[0][
                        #         "site_url"
                        #     ].replace("%5C", "/")
                        # else:
                        #     payload["update_data_docs"][doc_key] = None

                        failed_expectation_suite_results[validation_result_id] = (
                            validation_result
                        )

                        failed_validation_results.extend(
                            [
                                result
                                for result in validation_result.results
                                if not result.success
                            ]
                        )
                    successful_expectations += validation_result.statistics[
                        "successful_expectations"
                    ]
                    evaluated_expectations += validation_result.statistics[
                        "evaluated_expectations"
                    ]

            if evaluated_expectations == 0:
                success_percent = None
            else:
                success_percent = successful_expectations / evaluated_expectations * 100

            # create a summarizing validation result
            summary_validation_result = ExpectationSuiteValidationResult(
                suite_name="Summary_Expectation_Suite",
                success=len(failed_validation_results) == 0,
                results=failed_validation_results,
                statistics={
                    "successful_expectations": successful_expectations,
                    "evaluated_expectations": evaluated_expectations,
                    "success_percent": success_percent,
                    "unsuccessful_expectations": evaluated_expectations
                    - successful_expectations,
                },
                meta={
                    "expectation_suite_name": "Summary_Expectation_Suite",
                    "batch_kwargs": {"data_asset_name": "All"},
                    "run_id": self.run_id,
                },
            )

            # create a summarizing checkpoint result
            checkpoint_result = CheckpointResult(
                run_id=self.run_id,
                run_results={
                    ValidationResultIdentifier(
                        expectation_suite_identifier=ExpectationSuiteIdentifier(
                            "Summary_Expectation_Suite"
                        ),
                        run_id=self.run_id,
                        batch_identifier=f"summary",
                    ): summary_validation_result,
                    **failed_expectation_suite_results,
                },
                checkpoint_config=Checkpoint(
                    name=self.notifier.subject,  # define this here, as it will be the subject of the msg (e.g. email)
                    validation_definitions=[],
                ),
                result_url=None,
            )

            self.notifier.run(checkpoint_result=checkpoint_result)
