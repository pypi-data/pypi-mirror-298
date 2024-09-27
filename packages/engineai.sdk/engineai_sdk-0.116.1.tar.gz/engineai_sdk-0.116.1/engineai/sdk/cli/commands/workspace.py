"""workspace command for engineai CLI."""

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.workspace_api import WorkspaceAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

from .workspace_member import member

WORKSPACE_ROLE = ["ADMIN", "MEMBER"]


@click.group(name="workspace", invoke_without_command=False)
def workspace() -> None:
    """Workspace commands."""


@workspace.command()
def ls() -> None:
    """List all workspace."""
    api = WorkspaceAPI()
    try:
        workspace_list = api.list_workspace()
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if workspace_list:
        console = Console()
        table = Table(
            title="workspace",
            show_header=False,
            show_edge=True,
        )
        for current_workspace in workspace_list:
            table.add_row(current_workspace.get("slug"))
        console.print(table)
    else:
        write_console("No workspace found\n", 0)


@workspace.command("add")
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
def add_workspace(workspace_name: str) -> None:
    """Add new workspace.

    Args:
        workspace_name: workspace to be added.
    """
    api = WorkspaceAPI()
    try:
        api.create_workspace(workspace_name)
        write_console(f"workspace `{workspace_name}` added successfully\n", 0)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@workspace.command("rm")
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
def remove_workspace(workspace_name: str) -> None:
    """Remove workspace.

    Args:
        workspace_name: workspace to be removed.
    """
    api = WorkspaceAPI()
    try:
        api.delete_workspace(workspace_name)
        write_console(f"workspace `{workspace_name}` removed successfully\n", 0)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@workspace.command("rename")
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "new_workspace_name",
    required=True,
    type=str,
)
def update(workspace_name: str, new_workspace_name: str) -> None:
    """Update current workspace.

    Args:
        workspace_name: workspace to be updated.
        new_workspace_name: new workspace name.
    """
    api = WorkspaceAPI()
    try:
        api.update_workspace(workspace_name, new_workspace_name)
        write_console(
            f"workspace `{workspace_name}` renamed to `{new_workspace_name}` with "
            "success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


workspace.add_command(member)
