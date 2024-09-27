"""app command for engineai CLI."""

import click
from rich.console import Console
from rich.table import Table

from engineai.sdk.cli.utils import write_console
from engineai.sdk.dashboard.clients.mutation.app_api import AppAPI
from engineai.sdk.internal.clients.exceptions import APIServerError
from engineai.sdk.internal.exceptions import UnauthenticatedError

from .app_rule import rule


@click.group(name="app", invoke_without_command=False)
def app() -> None:
    """App commands."""


@app.command(
    "ls",
    help="""List all apps.

            \b
            WORKSPACE_NAME: workspace to be listed.
            """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
def list_workspace_app(workspace_name: str) -> None:
    """List workspace apps.

    Args:
        workspace_name: workspace to be listed.
    """
    api = AppAPI()
    try:
        apps = api.list_workspace_apps(workspace_name)
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)

    if apps:
        slug = apps.get("slug")
        workspace_apps = apps.get("apps", [])

        if not workspace_apps:
            write_console("No apps found\n", 0)
            return

        console = Console()
        table = Table(
            title=f"Apps of workspace '{slug}'",
            show_header=False,
            show_edge=True,
        )
        for current_app in workspace_apps:
            table.add_row(current_app.get("slug"))
        console.print(table)


@app.command(
    "add",
    help="""Add new app.

            \b
            WORKSPACE_NAME: workspace to be added.
            APP_NAME: app to be added.
            TITLE: app title.
            """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "app_name",
    required=True,
    type=str,
)
@click.argument(
    "title",
    required=True,
    type=str,
)
def add_app(workspace_name: str, app_name: str, title: str) -> None:
    """Add new app.

    Args:
        workspace_name: workspace to be added.
        app_name: app to be added.
        title: app title.
    """
    api = AppAPI()

    try:
        api.create_app(workspace_name, app_name, title)
        write_console(
            f"Successfully created app `{app_name}` within workspace "
            f"`{workspace_name}`\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


@app.command(
    "rename",
    help="""Update current app.

        \b
        workspace_NAME: workspace to be updated.
        APP_NAME: app to be updated.
        NEW_APP_NAME: new app name.
        """,
)
@click.argument(
    "workspace_name",
    required=True,
    type=str,
)
@click.argument(
    "app_name",
    required=True,
    type=str,
)
@click.argument(
    "new_app_name",
    required=True,
    type=str,
)
def update(workspace_name: str, app_name: str, new_app_name: str) -> None:
    """Update current app.

    Args:
        workspace_name: workspace to be updated.
        app_name: app to be updated.
        new_app_name: new app name.
    """
    api = AppAPI()
    try:
        api.update_app(workspace_name, app_name, new_app_name)
        write_console(
            f"Successfully renamed app `{app_name}` within the workspace "
            f"`{workspace_name}` to `{new_app_name}`\n",
            0,
        )
    except (APIServerError, UnauthenticatedError) as e:
        write_console(f"{e}\n", 1)


app.add_command(rule)
