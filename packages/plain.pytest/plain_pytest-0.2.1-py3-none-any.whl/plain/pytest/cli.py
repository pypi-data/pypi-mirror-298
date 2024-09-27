import os
import sys

import click

import pytest
from plain.runtime import settings


@click.command(
    context_settings={
        "ignore_unknown_options": True,
    }
)
@click.argument("pytest_args", nargs=-1, type=click.UNPROCESSED)
def cli(pytest_args):
    """Run tests with pytest"""

    plain_tmp_dir = str(settings.PLAIN_TEMP_PATH)

    if not os.path.exists(os.path.join(plain_tmp_dir, ".gitignore")):
        os.makedirs(plain_tmp_dir, exist_ok=True)
        with open(os.path.join(plain_tmp_dir, ".gitignore"), "w") as f:
            f.write("*\n")

    # Turn deprecation warnings into errors
    #     if "-W" not in pytest_args:
    #         pytest_args = list(pytest_args)  # Make sure it's a list instead of tuple
    #         pytest_args.append("-W")
    #         pytest_args.append("error::DeprecationWarning")

    # has to happen before setup() to be more useful? initial setup() may fail if doesn't have the required variables
    # or don't set it by default at all... could warn on != TEST?
    os.environ.setdefault("PLAIN_ENV", "test")

    click.secho(f"Running pytest with PLAIN_ENV={os.environ['PLAIN_ENV']}", bold=True)

    returncode = pytest.main(list(pytest_args))
    if returncode:
        sys.exit(returncode)
