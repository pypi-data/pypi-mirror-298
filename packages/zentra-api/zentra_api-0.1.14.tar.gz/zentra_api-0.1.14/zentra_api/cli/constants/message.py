from enum import Enum
import textwrap
import typer

from rich.console import Console
from rich.panel import Panel

from zentra_api.cli.constants import (
    ERROR_GUIDE_URL,
    FAIL,
    GITHUB_ISSUES_URL,
    MAGIC,
    ROOT_COMMAND,
    CommonErrorCodes,
    RouteErrorCodes,
    RouteSuccessCodes,
    SetupSuccessCodes,
)


def creation_msg(project_name: str, project_type: str, project_path: str) -> str:
    return f"\n{MAGIC} Creating new [green]{project_type}[/green] project called: [magenta]{project_name}[/magenta] -> [yellow]{project_path}[/yellow] {MAGIC}\n"


MORE_HELP_INFO = f"""
[dark_goldenrod]Need more help?[/dark_goldenrod] 
  Check our [bright_blue][link={ERROR_GUIDE_URL}]Error Message Guide[/link][/bright_blue].

[red]Really stuck?[/red] 
  Report the issue [bright_blue][link={GITHUB_ISSUES_URL}]on GitHub[/link][/bright_blue].
"""

BUILD_COMMANDS = f"""
[dark_goldenrod]Start Building![/dark_goldenrod]
    - Create some database tables 
    [yellow]{ROOT_COMMAND} add-table <>[/yellow]
    - And some routes 
    [cyan]{ROOT_COMMAND} add-route <>[/cyan]
"""

MISSING_PROJECT = f"""
Have you run [yellow]{ROOT_COMMAND} init[/yellow] and are 
you in the [magenta]project[/magenta] directory?
"""

ROUTE_CREATED = """
Access them in the [magenta]api[/magenta] directory.
"""

ROUTE_SET_EXISTS = """
You've already created a set of API routes with this name!
"""

UNKNOWN_ERROR = f"""
{FAIL} 🥴 Well this is awkward... We didn't account for this! 🥴 {FAIL}

You've encountered something unexpected 🤯. Please report this issue on [bright_blue][link={GITHUB_ISSUES_URL}]GitHub[/link][/bright_blue].
"""


def error_msg_with_checks(title: str, desc: str) -> str:
    """Formats error messages that have a title and a list of checks."""
    return textwrap.dedent(f"\n{FAIL} [bright_red]{title}[/bright_red] {FAIL}\n") + desc


def success_msg_with_checks(title: str, desc: str, icon: str = MAGIC) -> str:
    """Formats success messages that have a title and a list of checks."""
    return (
        textwrap.dedent(f"\n{icon} [bright_green]{title}[/bright_green] {icon}\n")
        + desc
    )


SUCCESS_MSG_MAP = {
    SetupSuccessCodes.TEST_SUCCESS: success_msg_with_checks("Test", desc=""),
    SetupSuccessCodes.COMPLETE: "",
    SetupSuccessCodes.ALREADY_CONFIGURED: "",
}

COMMON_ERROR_MAP = {
    CommonErrorCodes.TEST_ERROR: error_msg_with_checks("Test", desc=""),
    CommonErrorCodes.PROJECT_NOT_FOUND: error_msg_with_checks(
        "Project not found!",
        desc=MISSING_PROJECT,
    ),
}

ROUTE_SUCCESS_MAP = {
    RouteSuccessCodes.CREATED: success_msg_with_checks(
        "Route set created!",
        desc=ROUTE_CREATED,
    ),
}

ROUTE_ERROR_MAP = {
    RouteErrorCodes.FOLDER_EXISTS: error_msg_with_checks(
        "Route set already exists!",
        desc=ROUTE_SET_EXISTS,
    ),
}

MSG_MAPPER = {
    **SUCCESS_MSG_MAP,
    **COMMON_ERROR_MAP,
    **ROUTE_SUCCESS_MAP,
    **ROUTE_ERROR_MAP,
}


class MessageHandler:
    """Handles all the error and success messages for the CLI."""

    def __init__(self, console: Console, msg_mapper: dict[Enum, str]) -> None:
        self.console = console
        self.msg_mapper = msg_mapper

    @staticmethod
    def __error_msg(msg: str, e: typer.Exit) -> Panel:
        """Handles error messages and returns a panel with their information."""
        err_str = "[cyan]Error code[/cyan]"
        error_code = f"\n{err_str}: {e.exit_code.value}\n"

        return Panel(
            msg + MORE_HELP_INFO + error_code,
            expand=False,
            border_style="bright_red",
        )

    @staticmethod
    def __success_msg(msg: str, e: typer.Exit) -> Panel:
        """Handles success messages and returns a panel with their information."""
        return Panel(msg, expand=False, border_style="bright_green")

    def msg(self, e: typer.Exit) -> None:
        """Assigns a success or error message depending on the code received."""
        try:
            if e.exit_code not in self.msg_mapper.keys():
                e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

            msg = textwrap.dedent(self.msg_mapper.get(e.exit_code, UNKNOWN_ERROR))

        except AttributeError:
            e.exit_code = CommonErrorCodes.UNKNOWN_ERROR

        msg_type = e.exit_code.__class__.__name__

        if msg != "":
            panel = (
                self.__error_msg(msg, e)
                if "Error" in msg_type
                else self.__success_msg(msg, e)
            )
            self.console.print(panel)
