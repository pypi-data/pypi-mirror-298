import sys
import time

import click
from colorama import Fore, Style, init

from .main import create_project_structure

version = '5.0'

# Initialize colorama
init(autoreset=True)

# ASCII art for LDJANGO with colors
LDJANGO_ASCII = f"""
   __     _  _                         
  / /  __| |(_) __ _ _ __   __ _  ___  
 / /  / _` || |/ _` | '_ \ / _` |/ _ \ 
/ /__| (_| || | (_| | | | | (_| | (_) |
\____/\__,_|/ |\__,_|_| |_|\__, |\___/ 
          |__/             |___/       
"""

def display_ascii_art():
    for i in range(len(LDJANGO_ASCII)):
        print(f"{Fore.GREEN}{Style.BRIGHT}{LDJANGO_ASCII[i]}{Style.RESET_ALL}", end='', flush=True)
        time.sleep(0.001)
    print()

@click.group()
@click.version_option(version=version, message=f'{LDJANGO_ASCII}\n{Fore.GREEN}ldjango version {version}{Style.RESET_ALL}')
@click.help_option('-h', '--help')
def cli():
    """ldjango: CLI tool for creating Django projects with a predefined structure."""
    display_ascii_art()
    pass

@cli.command()
def makeproject():
    """Create a new Django project with a predefined structure."""
    click.echo(f"{Fore.YELLOW}{Style.BRIGHT}Welcome to ldjango: Your Django project creator!{Style.RESET_ALL}")
    
    project_name = click.prompt(f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}Enter your project name{Style.RESET_ALL}", default="MyProject", prompt_suffix=": ", show_default=True)
    
    app_count = click.prompt(
        f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}How many applications do you want to create?{Style.RESET_ALL}",
        type=click.IntRange(min=1),
        default=1,
        show_default=True,
        prompt_suffix=': ',
    )
    
    app_names = []
    for i in range(app_count):
        app_name = click.prompt(
            f"{Fore.CYAN}{Style.BRIGHT}? {Fore.MAGENTA}{Style.NORMAL}Django Application Name {i + 1}{Style.RESET_ALL}",
            default=f"MyApp{i + 1}",
            prompt_suffix=": ",
            show_default=True,
        )
        app_names.append(app_name)
    
    click.echo(f"\n{Fore.GREEN}{Style.BRIGHT}Creating your Django project...{Style.RESET_ALL}")
    create_project_structure(project_name, app_names)

if __name__ == '__main__':
    cli()
