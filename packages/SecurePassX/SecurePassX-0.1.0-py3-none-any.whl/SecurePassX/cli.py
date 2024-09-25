from typing import Optional, List
from pathlib import Path
import typer
from SecurePassX import ERRORS, SecurePassX, __app_name__, __version__, config, database, security
from SecurePassX import __app_name__, __version__

app = typer.Typer()

@app.command()
def init(
    db_path: str = typer.Option(
        str(database.DEFAULT_DB_FILE_PATH),
        "--db-path",
        "-db",
        prompt=" database location?",
    ),
) -> None:
    """Initialize the database."""
    app_init_error = config.init_app(db_path)
    if app_init_error:
        typer.secho(
            f'Creating config file failed with "{ERRORS[app_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    db_init_error = database.init_database(Path(db_path))
    if db_init_error:
        typer.secho(
            f'Creating database failed with "{ERRORS[db_init_error]}"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)
    else:
        typer.secho(f"The database is {db_path}", fg=typer.colors.GREEN)

def get_secreter() -> SecurePassX.SecPassSecret:
    if config.CONFIG_FILE_PATH.exists():
        db_path = database.get_database_path(config.CONFIG_FILE_PATH)
    else:
        typer.secho(
            'Config file not found. Please run "secpass init"',
            fg=typer.colors.RED
        )
        raise typer.Exit(1)
    if db_path.exists():
        return SecurePassX.SecPassSecret(db_path)
    else:
        typer.secho(
            'Database not found. Please, run "secpass init"',
            fg=typer.colors.RED,
        )
        raise typer.Exit(1)

@app.command()
def add(
    title: List[str] = typer.Argument(...),
    username: str = typer.Option(2, "--username", "-u"),
    password: str = typer.Option(3, "--password", "-p")
) -> None:
    """Add a Secret"""
    secreter = get_secreter()
    secret, error = secreter.add(title, username, password)
    if error:
        typer.secho(
            f'Adding scret failed with "{ERRORS[error]}"', fg=typer.colors.RED
        )
        raise typer.Exit(1)
    else:
        typer.secho(
            f"""secret: "{secret['Title']}" was added """,
            fg=typer.colors.GREEN,
        )

@app.command(name="list")
def list_all() -> None:
    """Lsit all Screts"""
    secreter = get_secreter()
    secret_list = secreter.get_secret_list()
    if len(secret_list) == 0:
        typer.secho(
            "There are no secrets in the secpass list yet", fg=typer.colors.RED
        )
        raise typer.Exit()
    typer.secho("\nsecret list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Username  ",
        "| Title  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    for id, secret in enumerate(secret_list, 1):
        title, username, password = secret.values()
        typer.secho(
            f"{id}{(len(columns[0]) - len(str(id))) * ' '}"
            f"| {username}{(len(columns[1]) - len(str(username)) - 4) * ' '}"
            f"| {title}",
            fg=typer.colors.BLUE,
        )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)

@app.command()
def remove(
    secret_id: int = typer.Argument(...),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="Force deletion without confirmation",
    )
) -> None:
    """Remove a secret using its SECRET_ID"""
    secreter = get_secreter()

    def _remove():
        secret, error = secreter.remove(secret_id)
        if error:
            typer.secho(
                f'Removing secret # {secret_id} failed with "{ERRORS[error]}"',
                fg=typer.colors.RED
            )
            raise typer.Exit(1)
        else:
            typer.secho(
                f"""secret # {secret_id}: '{secret["Title"]}' was removed"""
            )
        
    if force:
        _remove()
    else:
        secret_list  = secreter.get_secret_list()
        try:
            secret = secret_list[secret_id - 1]
        except IndexError:
            typer.secho("Invalid SECRET_ID", fg=typer.colors.RED)
            raise typer.Exit(1)
        delete = typer.confirm(
            f"Delete secret # {secret_id}: {secret['Title']}?"
        )
        if delete:
            _remove()
        else:
            typer.echo("Operation Cancelled")

@app.command(name="get")
def get(
    secret_id: int = typer.Argument(...)
) -> None:
    """Get the Decrypted Password of a Secret"""
    secreter = get_secreter()
    secret = secreter.get_secret(secret_id)
    typer.secho("\nsecret list:\n", fg=typer.colors.BLUE, bold=True)
    columns = (
        "ID.  ",
        "| Username  ",
        "| Password  ",
        "| Title  ",
    )
    headers = "".join(columns)
    typer.secho(headers, fg=typer.colors.BLUE, bold=True)
    typer.secho("-" * len(headers), fg=typer.colors.BLUE)
    title, username, password = secret.secret['Title'], secret.secret['Username'], secret.secret['Password']
    typer.secho(
        f"{secret_id}{(len(columns[0]) - len(str(secret_id))) * ' '}"
        f"| {username}{(len(columns[1]) - len(str(username)) - 4) * ' '}"
        f"| {security.decrypt(password)}{(len(columns[2]) - len(str(password)) - 2) * ' '}"
        f"| {title}",
        fg=typer.colors.BLUE,
    )
    typer.secho("-" * len(headers) + "\n", fg=typer.colors.BLUE)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()

@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return