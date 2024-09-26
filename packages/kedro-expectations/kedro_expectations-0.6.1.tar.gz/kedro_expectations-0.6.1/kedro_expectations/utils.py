import ntpath
import os
import glob
from typing import Union

import pandas as pd
import great_expectations as ge
from great_expectations.data_context import FileDataContext
from great_expectations.datasource.fluent import PandasDatasource, DataAsset
from great_expectations.experimental.rule_based_profiler import RuleBasedProfiler
from kedro.framework.session import KedroSession
from kedro_datasets.partitions import PartitionedDataset

from .assistant.rules import get_onboarding_rules, DATASET_TYPE

from .constants import (
    _DEFAULT_PANDAS_DATASOURCE_NAME,
    _DEFAULT_BATCH_DEFINITION_WHOLE_DATAFRAME_NAME,
)
import click
from time import sleep


def base_ge_folder_exists(verbose=True):
    base_folder = os.getcwd()
    ge_folder_legacy = os.path.join(base_folder, "great_expectations")
    ge_folder = os.path.join(base_folder, "gx")
    if os.path.exists(ge_folder) or os.path.exists(ge_folder_legacy):
        return True
    else:
        if verbose is True:
            message = """
            This command has NOT been run
            Kedro expectations wasn't initiated yet!
            Please run \'kedro expectations init\' before running this command.
            """
            print(message)
        return False


def location_is_kedro_root_folder():
    try:
        project_path = os.getcwd()
        KedroSession.create(project_path=project_path)
        return True
    except ModuleNotFoundError:
        print(
            """
        Cannot run command!
        You need to be in a kedro root folder to use Kedro Expectations!
        """
        )
        return False


def is_dataset_in_catalog(input, catalog):
    if input in catalog.list():
        return True
    else:
        print(
            f"\n\nThe input {input} was not found at the DataCatalog.\n",
            "The following datasets are available for use:\n",
        )
        print(*catalog.list(), sep=", ")
        return False


def dot_to_underscore(value):
    adjusted_value = str(value).replace(".", "_")
    return adjusted_value


def get_or_add_pandas_datasource(
    ge_context: FileDataContext, name=_DEFAULT_PANDAS_DATASOURCE_NAME
) -> PandasDatasource:
    try:
        return ge_context.get_datasource(name)
    except ValueError:
        return ge_context.data_sources.add_pandas(name)


def get_or_add_dataframe_asset(ge_context: FileDataContext, name: str) -> DataAsset:
    datasource = get_or_add_pandas_datasource(ge_context=ge_context)
    try:
        return datasource.get_asset(name)
    except LookupError:
        return datasource.add_dataframe_asset(name)


def get_or_add_batch_definition(
    data_asset: DataAsset, name: str = _DEFAULT_BATCH_DEFINITION_WHOLE_DATAFRAME_NAME
) -> ge.core.batch_definition.BatchDefinition:
    try:
        return data_asset.get_batch_definition(name)
    except KeyError:
        return data_asset.add_batch_definition(name)


def get_or_add_validation_definition(
    ge_context: FileDataContext, suite_name: str, dataset_name: str
) -> ge.ValidationDefinition:
    """
    Get a validation definition for a already specified suite and dataset. Adds the validation definition (using whole
    dataframe batch), if it does not exist.

    :param ge_context: Great expectation context
    :param suite_name: Name of the expectation suite
    :param dataset_name: Name of the kedro data_set (normally the first part of the suite name)

    :return: ge.ValidationDefinition object to use, e.g. for a great expectation checkpoint
    """

    vd_name = f"{suite_name}_validation_definition"

    try:
        return ge_context.validation_definitions.get(vd_name)
    except (
        ge.exceptions.DataContextError,
        ge.exceptions.ResourceFreshnessAggregateError,
    ):
        # Create a Validation Definition
        dataframe_asset = get_or_add_dataframe_asset(
            ge_context=ge_context, name=dataset_name
        )
        batch_definition = get_or_add_batch_definition(dataframe_asset)
        validation_definition = ge.ValidationDefinition(
            data=batch_definition,
            suite=ge_context.suites.get(suite_name),
            name=vd_name,
        )
        # Add the Validation Definition to the Data Context
        ge_context.validation_definitions.add(validation_definition)

        return validation_definition


def get_or_add_checkpoint(
    ge_context: FileDataContext,
    name: str,
    validation_definitions: list[ge.ValidationDefinition],
    action_list: list[ge.checkpoint.actions.DataDocsAction],
    overwrite: bool = False,
) -> ge.Checkpoint:
    try:
        checkpoint = ge_context.checkpoints.get(name)
        if (
            validation_definitions is not None
            and checkpoint.validation_definitions != validation_definitions
        ):
            if overwrite:
                checkpoint.validation_definitions.clear()
                checkpoint.validation_definitions.extend(validation_definitions)
            else:
                raise ValueError(
                    f"Checkpoint {name} exists but has different validation definitions. "
                    f"Set overwrite to True if they should be overwritten"
                )
        if action_list is not None and checkpoint.actions != action_list:
            if overwrite:
                checkpoint.actions.clear()
                checkpoint.actions.extend(action_list)
            else:
                raise ValueError(
                    f"Checkpoint {name} exists but has different actions defined. "
                    f"Set overwrite to True if they should be overwritten"
                )
        checkpoint.save()

    except ge.exceptions.DataContextError:
        # Create the Checkpoint
        checkpoint = ge.Checkpoint(
            name=name,
            validation_definitions=validation_definitions,
            actions=action_list,
            result_format={"result_format": "COMPLETE"},
        )
        ge_context.checkpoints.add(checkpoint)

    return checkpoint


def validate(
    ge_context: FileDataContext,
    dataset_name: str,
    suite_name: str,
    validation_df: pd.DataFrame,
    run_id: Union[None, ge.core.RunIdentifier] = None,
):
    validation_definition = get_or_add_validation_definition(
        ge_context=ge_context, suite_name=suite_name, dataset_name=dataset_name
    )

    # Create a list of Actions for the Checkpoint to perform
    action_list = [
        # This Action updates the Data Docs static website with the Validation
        #   Results after the Checkpoint is run.
        ge.checkpoint.UpdateDataDocsAction(
            name="update_all_data_docs",
        ),
    ]

    checkpoint_name = f"{suite_name}_kedro_checkpoint"
    checkpoint = get_or_add_checkpoint(
        ge_context=ge_context,
        name=checkpoint_name,
        validation_definitions=[validation_definition],
        action_list=action_list,
    )

    validation_result = checkpoint.run(
        run_id=run_id, batch_parameters={"dataframe": validation_df}
    )
    return validation_result


def get_all_expectations(ge_context, adjusted_key):
    exp_suites_pattern = os.path.join(
        os.path.normpath(
            ge_context.expectations_store.store_backend.full_base_directory
        ),
        adjusted_key,
        "*.json",
    )
    all_expectations = glob.glob(exp_suites_pattern)
    return all_expectations


def get_suite_name(exp_file, adjusted_key):
    parent_path, filename = ntpath.split(exp_file)
    suite_name = adjusted_key + "." + filename[:-5]
    return suite_name


def split_suite_name(suite_name) -> tuple:
    return tuple(suite_name.split("."))


def populate_new_suite(
    input_data: pd.DataFrame, expectation_suite_name: str, dataset_type: DATASET_TYPE
):
    ge_context = ge.get_context(mode="file")

    data_asset = get_or_add_dataframe_asset(
        ge_context, name=expectation_suite_name.split(".")[0]
    )
    batch_definition = get_or_add_batch_definition(data_asset=data_asset)

    click.echo("\n\nYour dataset has the following columns:")
    click.echo(input_data.columns.values)
    click.echo(
        "One by one, type the name of the columns you do NOT want to validate.\nOnce you are finished, "
        "type 0 to continue"
    )
    column_to_remove = ""
    exclude_column_names = []
    while column_to_remove != "0":
        column_to_remove = click.prompt("", type=str)
        if column_to_remove == "0":
            pass
        elif column_to_remove not in input_data.columns:
            print(
                f"The column {column_to_remove} doesn't exist in this dataframe. Try typing again"
            )
        else:
            exclude_column_names.append(column_to_remove)

    if exclude_column_names:
        print("The following columns are not going to be validated:")
        print(exclude_column_names)
        sleep(3)
    else:
        print("You chose for all columns to be validated!")
        sleep(3)

    # Removing duplicates
    exclude_column_names = [*set(exclude_column_names)]

    if len(exclude_column_names) >= len(input_data.columns.values):
        print(
            "\n\nAll the columns were marked to be excluded!", "Impossible to validate!"
        )
    else:
        rules = get_onboarding_rules(dataset_type=dataset_type)
        profiler = RuleBasedProfiler(
            name="Onboarding Profiler",
            rules=rules,
            data_context=ge_context,
            config_version=1.0,
        )

        # Run the profiler (excluding the defined column names) and store the generated suite
        batch = batch_definition.get_batch(
            batch_parameters={
                "dataframe": input_data.drop(columns=exclude_column_names)
            }
        )
        result = profiler.run(batch_list=[batch])
        suite = result.get_expectation_suite(name=expectation_suite_name)
        suite.save()

        print(
            "\nFor more information about how to edit the expectations suite, access: "
            "https://docs.greatexpectations.io/docs/guides/expectations/creating_custom_expectations/overview/\n"
        )
        return suite


def choose_valid_suite_name():
    suite_name = "."
    while "." in suite_name or "," in suite_name or " " in suite_name:
        suite_name = click.prompt("", type=str)
        if "." in suite_name or " " in suite_name:
            print(
                "Please choose another name for your suite.",
                "It cannot contain dots, commas or spaces",
            )
    return suite_name


def choose_valid_dataset_name(catalog):
    dataset_name = click.prompt("", type=str)
    while not isinstance(getattr(catalog.datasets, dataset_name), PartitionedDataset):
        print(f"The dataset {dataset_name} is not partitioned! Type again:")
        dataset_name = click.prompt("", type=str)
    return dataset_name
