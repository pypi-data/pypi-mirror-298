import click

from .main import create_project_structure


@click.command()
def cli():
    project_name = click.prompt("What is the name of your project?")
    app_count = click.prompt("How many apps do you want to create?", type=int)
    
    app_names = []
    for i in range(app_count):
        app_name = click.prompt(f"Django App Name {i + 1}")
        app_names.append(app_name)
    
    create_project_structure(project_name, app_names)

if __name__ == '__main__':
    cli()
