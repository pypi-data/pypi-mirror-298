import sys

import click
import inquirer


@click.command(
    context_settings={  # https://click.palletsprojects.com/en/8.1.x/api/#click.Context
        "show_default": True,
        "help_option_names": ("--help", "-h"),
        "max_content_width": float("inf"),
        "auto_envvar_prefix": "OOPSIE",
    }
)
@click.version_option(message=f"%(prog)s, version %(version)s using Python {sys.version.partition(' ')[0]}")
@click.option("--yes/--no", "-y/-n", help="Execute fixed command without confirmation.", default=False)
def main(
    *,
    yes: bool,
) -> None:
    """Suggest corrections for failed CLI commands."""
    # TODO: get choices from rules
    choices = ["option 1", "another choice", "maybe this one"]

    selected = choices[0] if yes else inquirer.list_input("What command do you want to run?", choices=choices)

    # TODO: execute selected choice
    click.echo(f"{selected=}")
