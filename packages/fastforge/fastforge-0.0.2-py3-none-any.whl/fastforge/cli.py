import os
import click


@click.group()
def fastforge():
    """FastForge: A simple FastAPI utility CLI."""
    pass


@fastforge.command()
@click.argument("app_name")
def create_app(app_name):
    """Generate a FastAPI sub-app folder with the given APP_NAME."""
    # Directories and files to create
    files = [
        "__init__.py",
        "router.py",
        "schemas.py",
        "models.py",
        "dependencies.py",
        "config.py",
        "constants.py",
        "exceptions.py",
        "service.py",
        "utils.py",
    ]

    # Create the main directory for the sub-app
    try:
        os.makedirs(app_name, exist_ok=True)
        click.echo(f"Created directory: {app_name}")
    except OSError as error:
        click.echo(f"Failed to create directory: {app_name} due to {error}")
        return

    # Create all necessary files within the directory
    for file in files:
        file_path = os.path.join(app_name, file)
        with open(file_path, "w") as f:
            f.write("")  # Creates an empty file
        click.echo(f"Created file: {file_path}")
