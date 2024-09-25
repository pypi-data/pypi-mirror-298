import click.testing
import pytest

from oopsie import _cli as cli


def test_trivial() -> None:
    assert True


@pytest.mark.skip("Still figuring out how to test the CLI, if at all")
def test_cli_trivial() -> None:
    runner = click.testing.CliRunner()
    result = runner.invoke(cli.main)
    if result.exception:
        raise result.exception
    assert result.exit_code == 0
    assert result.output == "option 1 [enter/↑/↓/ctrl+c]\nselected='option 1'\n"
