import click

from .main import create_project_structure

version = '1.1'

# ASCII art for LDJANGO
LDJANGO_ASCII = """

   __     _  _                         
  / /  __| |(_) __ _ _ __   __ _  ___  
 / /  / _` || |/ _` | '_ \ / _` |/ _ \ 
/ /__| (_| || | (_| | | | | (_| | (_) |
\____/\__,_|/ |\__,_|_| |_|\__, |\___/ 
          |__/             |___/       

"""

@click.group()
@click.version_option(version=version, message=f'{LDJANGO_ASCII}\nldjango version {version}')
@click.help_option('-h', '--help')
def cli():
    """ldjango: CLI tool for creating Django projects with a predefined structure."""
    click.echo(LDJANGO_ASCII)
    pass

@cli.command()
def makeproject():
    click.echo("ldjango: CLI tool for creating Django projects with a predefined structure.")
    """Create a new Django project with a predefined structure."""
    project_name = click.prompt("What is your project name?")
    app_count = click.prompt("How many applications do you want to create?", type=int)
    
    app_names = []
    for i in range(app_count):
        app_name = click.prompt(f"Django Application Name {i + 1}")
        app_names.append(app_name)
    
    create_project_structure(project_name, app_names)

if __name__ == '__main__':
    cli()
