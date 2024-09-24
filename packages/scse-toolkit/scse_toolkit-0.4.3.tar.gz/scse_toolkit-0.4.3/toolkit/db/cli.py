from pathlib import Path

import typer
from rich import print_json
from rich.console import Console
from rich.table import Table

from .alembic import AlembicController


class AlembicCli(typer.Typer):
    controller: AlembicController

    def __init__(self, *args, controller: AlembicController, **kwargs):
        super().__init__(*args, **kwargs)
        self.controller = controller
        self.console = Console()

        @self.command()
        def compare():
            """Compare the current metadata structure (populated by database models) against the database.
            Note: Currently there is a bug emitting some unnecessary changes when using this command."""
            changes = self.controller.compare_metadata(self.controller.get_metadata())
            if len(changes) == 0:
                typer.secho("No changes to the database schema detected.", fg="green")
                raise typer.Exit()
            else:
                typer.secho(
                    f"Detected changes resulting in {len(changes)} operation(s):",
                    fg="green",
                )
                print_json(data=changes, default=lambda x: repr(x))

        @self.command()
        def revisions():
            """List all database revisions."""
            table = Table("ID", "Branch Labels", "File Name")
            revisions = self.controller.list_revisions()
            for script in revisions:
                path = Path(script.path)
                table.add_row(
                    script.revision, ", ".join(script.branch_labels), path.name
                )
            script_location = self.controller.alembic_config.get_main_option(
                "script_location"
            )
            typer.echo(f"Found {len(revisions)} revision(s) in {script_location}:")
            self.console.print(table)

        @self.command()
        def autogenerate(
            message: str,
            override_rev_id: str | None = typer.Option(
                None, help="Override the revision id generated."
            ),
        ):
            """Autogenerate a new migration revision."""
            script = self.controller.autogenerate_revision(
                message, rev_id=override_rev_id
            )
            typer.secho(
                f"Generated revision '{script.revision}' at {script.path}", fg="green"
            )

        @self.command()
        def upgrade(
            revision: str = typer.Argument(
                "head", help="Revision ID or 'head' (default) for the newest revision."
            ),
        ):
            """Upgrade the database to the given revision ('head' per default)."""
            self.controller.upgrade_database(revision)
            typer.secho(f"Upgraded database to revision '{revision}'.", fg="green")

        @self.command()
        def downgrade(
            revision: str = typer.Argument(
                "-1",
                help="Revision ID or '-<int>' (default: '-1') for the nth previous revision.",
            ),
        ):
            """Downgrade the database to the given revision (first previous revision per default)."""
            self.controller.downgrade_database(revision)
            typer.secho(f"Downgraded database to revision '{revision}'.", fg="green")

        @self.command()
        def stamp(
            revision: str = typer.Argument(
                "head", help="Revision ID or 'head' (default) for the newest revision."
            ),
        ):
            """Stamp the database to the given revision !without running migrations!.
            This may break the migration logic. Use with care!"""
            if typer.confirm(
                f"Are you sure you want to stamp this database to revision '{revision}'?"
            ):
                self.controller.stamp_database(revision)
                typer.secho(f"Stamped database to revision '{revision}'.", fg="green")
            else:
                raise typer.Abort()
