import sys
import time

import click
from colorama import Fore, Style, init

from .main import create_project_structure

version = '4.2'

# Initialize colorama
init(autoreset=True)

# ASCII art for LDJANGO with colors
LDJANGO_ASCII = f"""{Fore.CYAN}

   __     _  _                         
  / /  __| |(_) __ _ _ __   __ _  ___  
 / /  / _` || |/ _` | '_ \ / _` |/ _ \ 
/ /__| (_| || | (_| | | | | (_| | (_) |
\____/\__,_|/ |\__,_|_| |_|\__, |\___/ 
          |__/             |___/       

{Style.RESET_ALL}"""

def display_ascii_animation():
    for line in LDJANGO_ASCII.split('\n'):
        sys.stdout.write(line + '\n')
        sys.stdout.flush()
        time.sleep(0.1)

@click.group()
@click.version_option(version=version, message=f'{LDJANGO_ASCII}\n{Fore.GREEN}ldjango version {version}{Style.RESET_ALL}')
@click.help_option('-h', '--help')
def cli():
    """ldjango: CLI tool for creating Django projects with a predefined structure."""
    display_ascii_animation()
    pass

@cli.command()
def makeproject():
    click.echo(f"{Fore.YELLOW}Welcome to ldjango: Your Django project creator!{Style.RESET_ALL}")
    """Create a new Django project with a predefined structure."""
    project_name = click.prompt(f"{Fore.CYAN}Enter your project name{Style.RESET_ALL}", default="MyProject", prompt_suffix=": ", show_default=True)
    app_count = click.prompt(
        f"{Fore.CYAN}How many applications do you want to create? (Use up/down arrow keys to adjust){Style.RESET_ALL}",
        type=click.IntRange(min=1),
        default=1,
        show_default=True,
        prompt_suffix=': ',
        value_proc=lambda x: max(1, int(x)) if x.isdigit() else 1
    )
    
    app_names = []
    for i in range(app_count):
        app_name = click.prompt(
            f"{Fore.MAGENTA}Django Application Name {i + 1}{Style.RESET_ALL}",
            default=f"MyApp{i + 1}",
            prompt_suffix=": ",
            show_default=True
        )
        app_names.append(app_name)
    
    click.echo(f"\n{Fore.GREEN}Creating your Django project...{Style.RESET_ALL}")
    create_project_structure(project_name, app_names)

if __name__ == '__main__':
    cli()
