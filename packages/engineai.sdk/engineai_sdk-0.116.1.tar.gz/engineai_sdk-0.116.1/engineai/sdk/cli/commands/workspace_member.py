"""workspace member command for engineai CLI."""

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.workspace_api import WorkspaceAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

WORKSPACE_ROLE = ["ADMIN", "MEMBER"]


@click.group()
def member() -> None:
    """Workspace member commands."""


@member.command(
    "add",
    help="""Add new member to workspace.

            \b
            WORKSPACE_NAME: workspace to be updated.
            EMAIL: the user to be added to workspace.
            ROLE: role for the user in the workspace (ADMIN or MEMBER).
    """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(WORKSPACE_ROLE, case_sensitive=False),
)
def add_workspace_member(workspace_name: str, email: str, role: str) -> None:
    """Add new member to workspace.

    Args:
        workspace_name: workspace to be updated.
        email: user to be added to workspace.
        role: role for the user in the workspace (ADMIN or MEMBER).
    """
    api = WorkspaceAPI()
    member_role = role.upper()
    try:
        api.add_workspace_member(workspace_name, email, member_role)
        write_console(
            f"User `{email}` added to workspace `{workspace_name}` with role "
            f"`{member_role}` successfully\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "update",
    help="""Update member role in workspace.

            \b
            WORKSPACE_NAME: workspace to be updated.
            EMAIL: the user to be updated in the workspace.
            ROLE: new role for the user in the workspace (ADMIN or MEMBER).
    """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
@click.argument(
    "role",
    required=True,
    type=click.Choice(WORKSPACE_ROLE, case_sensitive=False),
)
def update_workspace_member_role(workspace_name: str, email: str, role: str) -> None:
    """Update member role in workspace.

    Args:
        workspace_name: workspace to be updated.
        email: user to be updated in the workspace.
        role: new role for the user in the workspace (ADMIN or MEMBER).
    """
    api = WorkspaceAPI()
    member_role = role.upper()
    try:
        api.update_workspace_member(workspace_name, email, member_role)
        write_console(
            f"User `{email}` updated to role `{member_role}` in workspace "
            f"`{workspace_name}` with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "rm",
    help="""Remove member from workspace.

            \b
            WORKSPACE_NAME: workspace to be updated.
            EMAIL: the user to be removed from workspace.
        """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
def remove_workspace_member(workspace_name: str, email: str) -> None:
    """Remove member from workspace.

    Args:
        workspace_name: workspace to be updated.
        email: user to be removed from workspace.
    """
    api = WorkspaceAPI()
    try:
        api.remove_workspace_member(workspace_name, email)
        write_console(
            f"User `{email}` removed from workspace `{workspace_name}` with success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@member.command(
    "ls",
    help="""List all member in workspace.

            \b
            workspace_name: workspace to be selected.
        """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
def ls_workspace_member(workspace_name: str) -> None:
    """List all member in workspace.

    Args:
        workspace_name: workspace to be selected.
    """
    api = WorkspaceAPI()
    try:
        workspaces = api.list_workspace_member(workspace_name)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if workspaces:
        slug = workspaces.get("slug")
        members = workspaces.get("members")
        console = Console()
        table = Table(
            title=f"Members of workspace '{slug}'",
            show_header=False,
            show_edge=True,
        )

        table.add_row("Member", "Role")
        table.add_section()
        for user in members:
            table.add_row(user.get("user").get("email"), user.get("role"))
        console.print(table)
    else:
        write_console("No workspace member found\n", 0)


@member.command(
    "transfer",
    help="""Transfer workspace to another member.

            \b
            WORKSPACE_NAME: workspace to be updated.
            EMAIL: member to be new workspace owner.
        """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "email",
    required=True,
    type=str,
)
def transfer_workspace(workspace_name: str, email: str) -> None:
    """Transfer workspace to another member.

    Args:
        workspace_name: workspace to be updated.
        email: member to be new workspace owner.
    """
    api = WorkspaceAPI()
    try:
        api.transfer_workspace(workspace_name, email)
        write_console(
            f"Workspace `{workspace_name}` transferred to user `{email}` with "
            "success\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)
