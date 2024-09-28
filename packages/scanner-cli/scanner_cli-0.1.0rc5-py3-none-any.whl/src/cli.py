""" Contains code for Python CLI """

import glob
import os
from typing import Any, Callable

import click

from scanner_client import Scanner
from scanner_client.detection_rule_yaml import validate_and_read_file

_CLICK_OPTIONS = [
    click.option(
        "--api-url",
        envvar="SCANNER_API_URL",
        help="The API URL of your Scanner instance. Go to Settings > API Keys in Scanner to find your API URL.",
    ),
    click.option(
        "--api-key",
        envvar="SCANNER_API_KEY",
        help="Scanner API key. Go to Settings > API Keys in Scanner to find your API keys or to create a new API key.",
    ),
    click.option(
        "-f",
        "--file",
        "file_paths",
        help="File to validate. This must be .yml or .yaml file with the correct schema header.",
        multiple=True,
    ),
    click.option(
        "-d",
        "--dir",
        "directories",
        help="Directory to validate. Only .yml or .yaml files with the correct schema header will be validated.",
        multiple=True,
    ),
    click.option(
        "-r",
        "recursive",
        is_flag=True,
        show_default=True,
        default=False,
        help="Recursively search directory for valid YAML files.",
    ),
]


def _click_options(func) -> Callable[..., Any]:
    for option in reversed(_CLICK_OPTIONS):
        func = option(func)

    return func


def _is_valid_file(file_path: str) -> bool:
    try:
        validate_and_read_file(file_path)
        return True
    except:
        return False


def _get_valid_files_in_directory(directory: str, recursive: bool) -> list[str]:
    if not os.path.exists(directory):
        raise click.exceptions.ClickException(
            message=(
                f"Directory {directory} not found."
            )
        )

    return [f for f in glob.iglob(f"{directory}/**", recursive=recursive) if _is_valid_file(f)]


def _get_valid_files(file_paths: str, directories: str, recursive: bool) -> list[str]:
    files = [f for f in file_paths if _is_valid_file(f)]

    for d in directories:
        files.extend(_get_valid_files_in_directory(d, recursive))

    return files


def _validate_shared_options(api_url: str, api_key: str, file_paths: str, directories: str) -> None:
    if api_url is None:
        raise click.exceptions.UsageError(
            message=(
                "Pass --api-url option or set `SCANNER_API_URL` environment variable."
            )
        )

    if api_key is None:
        raise click.exceptions.UsageError(
            message=(
                "Pass --api-key option or set `SCANNER_API_KEY` environment variable."
            )
        )

    if not file_paths and not directories:
        raise click.exceptions.UsageError(
            message=(
                "Either --file or --dir must be provided."
            )
        )


@click.group()
def cli():
    """ Python CLI for Scanner API """


@cli.command()
@_click_options
def validate(api_url: str, api_key: str, file_paths: str, directories: str, recursive: bool):
    """ Validate detection rules """
    _validate_shared_options(api_url, api_key, file_paths, directories)

    scanner_client = Scanner(api_url, api_key)

    files = _get_valid_files(file_paths, directories, recursive)
    click.echo(f'Validating {len(files)} {"file" if len(files) == 1 else "files"}')

    for file in files:
        try:
            result = scanner_client.detection_rule_yaml.validate(file)

            if result.is_valid:
                click.echo(f"{file}: " + click.style("Valid", fg="green"))
            else:
                click.echo(f"{file}: " + click.style(f"{result.error}", fg="red"))
        except Exception as e:
            click.echo(f"{file}: " + click.style(e, fg="red"))



@cli.command()
@_click_options
def run_tests(api_url: str, api_key: str, file_paths: str, directories: str, recursive: bool):
    """ Run detection rule tests """
    _validate_shared_options(api_url, api_key, file_paths, directories)

    scanner_client = Scanner(api_url, api_key)

    files = _get_valid_files(file_paths, directories, recursive)
    click.echo(f'Running tests on {len(files)} {"file" if len(files) == 1 else "files"}')

    for file in files:
        try:
            response = scanner_client.detection_rule_yaml.run_tests(file)
            results = response.results.to_dict()

            click.secho(f"{file}", bold=True)
            if len(results) == 0:
                click.secho("No tests found", fg="yellow")
            else:
                for name, status in response.results.to_dict().items():
                    if status == "Passed":
                        click.echo(f"{name}: " + click.style("Passed", fg="green"))
                    else:
                        click.echo(f"{name}: " + click.style("Failed", fg="red"))

            click.echo("")
        except Exception as e:
            click.secho(f"{file}", bold=True)
            click.secho(e, fg="red")
            click.echo("")


if __name__ == "__main__":
    cli()
