import functools
from pathlib import Path
from click import exceptions as click_exceptions
from ploomber_cloud import exceptions
import click
import shutil
from enum import Enum
from typing import Type

from ploomber_cloud.messages import FEATURE_PROMPT_MSG


def requires_init(func):
    """
    Wrapper around a function that checks and prompts if necessary
    for project initialization
    """
    from ploomber_cloud import init

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check for init, if not, prompt and run init flow
        if not Path("ploomber-cloud.json").exists():
            run_init = click.confirm(
                "Project must be initialized to continue. Would you like to initialize?"
            )

            if not run_init:
                raise exceptions.BasePloomberCloudException(
                    "This command requires a ploomber-cloud.json file.\n"
                    "Run 'ploomber-cloud init' to initialize your project."
                )

            init.init(from_existing=False, force=False, verbose=False)

        return func(*args, **kwargs)

    return wrapper


def requires_permission(permission: str):
    """
    Wrapper around a function that lets it execute only
    if the user invoking it has the required permissions
    """
    from ploomber_cloud import resources

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if (
                permission
                not in resources._get_resource_config_for_user_type()["allowedFeatures"]
            ):
                raise exceptions.UserTierForbiddenException()
            return func(*args, **kwargs)

        return wrapper

    return decorator


def pretty_print(
    obj: list, delimiter: str = ",", last_delimiter: str = "and", repr_: bool = False
) -> str:
    """
    Returns a formatted string representation of an array
    """
    if repr_:
        sorted_ = sorted(repr(element) for element in obj)
    else:
        sorted_ = sorted(f"'{element}'" for element in obj)

    if len(sorted_) > 1:
        sorted_[-1] = f"{last_delimiter} {sorted_[-1]}"

    return f"{delimiter} ".join(sorted_)


def raise_error_on_duplicate_keys(ordered_pairs):
    """Reject duplicate keys."""
    d = {}
    duplicate_keys = []
    for k, v in ordered_pairs:
        if k in d:
            duplicate_keys.append(k)
        else:
            d[k] = v
    if duplicate_keys:
        raise ValueError(f"Duplicate keys: {pretty_print(duplicate_keys)}")
    return d


def prompt_for_choice_from_list(
    choices, initial_prompt, index=False, ignore_case=False
):
    """Prompt a user to choose from options in a list format"""
    choices.append("exit")
    if ignore_case:
        choices = [c.lower() for c in choices]
    prompt = []
    for i, item in enumerate(choices):
        prompt.append(f"  {i+1}. {item}\n")

    prompt.append(initial_prompt)

    prompt_str = "".join(prompt)
    choice = None

    # Prompt user for choice
    while True:
        choice = click.prompt(prompt_str, type=str)
        if ignore_case:
            choice = choice.lower()
        # Case: user enters number
        if choice.isnumeric() and 0 < int(choice) <= len(choices):
            choice = choices[int(choice) - 1]
            break
        elif choice in choices:  # Case: user enters id
            break
        else:  # Case: user enters invalid
            click.echo("Please enter a valid choice.")

    if choice == "exit":
        click.echo("Exited.")
        raise click_exceptions.Exit()

    if index:
        return choices.index(choice)

    return choice


def print_divider():
    """Print a horizontal line the width of the terminal"""
    w, _ = shutil.get_terminal_size()
    click.echo("—" * w)


def get_project_details_mappings(projects):
    """Function for returning lookup of:
    1. Project ID that is displayed to the user and its original ID.
       Projects with custom name are displayed as project id (custom name).
    2. Project custom names and the corresponding ID.
    """

    display_id_mapping = {}
    project_name_mapping = {}

    for project in projects:
        pid = display_id = project["id"]
        name = project["name"]
        if name and pid != name:
            display_id = f"{pid} ({name})"
        display_id_mapping[display_id], project_name_mapping[name] = pid, pid

    return display_id_mapping, project_name_mapping


def prompt_for_feature(feature_enum: Type[Enum]):
    """
    Helper function to help prompt for a feature

    Params:
    _______
    - feature_enum: Type[Enum]
        Enum class with the features to choose from
    """

    click.echo(
        FEATURE_PROMPT_MSG
    )  # use echo since capsys doesn't capture the prompt output
    feature = prompt_for_choice_from_list(
        [feature.value for feature in feature_enum], ""
    )
    return feature
