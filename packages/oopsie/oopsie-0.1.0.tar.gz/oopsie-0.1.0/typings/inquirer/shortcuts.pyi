from typing import TypeVar

import inquirer.render.console
from _typeshed import Incomplete

_T = TypeVar("_T")

def list_input(
    message: str,
    *,
    choices: list[_T],
    render: inquirer.render.console.ConsoleRender = ...,
    **kwargs: Incomplete,
) -> _T: ...
