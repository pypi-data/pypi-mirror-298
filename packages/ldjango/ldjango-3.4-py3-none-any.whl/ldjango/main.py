import os
import subprocess
import sys
import time

import click
from tqdm import tqdm


def create_project_structure(project_name, app_names):
    try:
        total_steps = 12  # Updated number of steps
        with tqdm(total=total_steps, desc=click.style("Creating project", fg="green", bold=True), unit="step", bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
            # Function to run command without output
            def run_command(command):
                subprocess.run(command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                pbar.update(1)
                time.sleep(0.5)  # Add a small delay to make the progress bar appear smoother

            # Create project folders
            os.makedirs(project_name, exist_ok=True)
            os.makedirs(f"{project_name}/apps", exist_ok=True)
            os.makedirs(f"{project_name}/templates", exist_ok=True)
            os.makedirs(f"{project_name}/media", exist_ok=True)
            os.makedirs(f"{project_name}/static", exist_ok=True)
            pbar.update(1)

            # Initialize Django project
            run_command(['django-admin', 'startproject', 'core', project_name])

            # Create apps
            for app_name in app_names:
                app_path = f"{project_name}/apps/{app_name}"
                os.makedirs(app_path, exist_ok=True)
                run_command(['django-admin', 'startapp', app_name, app_path])

                # Update apps.py
                app_py = f"{app_path}/apps.py"
                if os.path.exists(app_py):
                    with open(app_py, 'r') as file:
                        content = file.read()
                    content = content.replace(f"name = '{app_name}'", f"name = 'apps.{app_name}'")
                    with open(app_py, 'w') as file:
                        file.write(content)

            # Create urls.py in apps folder
            urls_path = f"{project_name}/apps/urls.py"
            with open(urls_path, 'w') as file:
                file.write('from django.urls import path\n from ldjango import landing_page\nurlpatterns = [\npath("", landing_page, name="landing_page")\n]\n')

            # Update settings.py
            settings_path = f"{project_name}/core/settings.py"
            if os.path.exists(settings_path):
                with open(settings_path, 'r') as settings_file:
                    settings_content = settings_file.read()
                
                # Update ALLOWED_HOSTS
                settings_content = settings_content.replace("ALLOWED_HOSTS = []", "ALLOWED_HOSTS = ['*']")
                
                # Update MIDDLEWARE
                middleware_index = settings_content.find('MIDDLEWARE = [')
                if middleware_index != -1:
                    security_middleware_index = settings_content.find("'django.middleware.security.SecurityMiddleware',", middleware_index)
                    if security_middleware_index != -1:
                        insert_index = settings_content.find('\n', security_middleware_index) + 1
                        updated_middleware = (
                            settings_content[:insert_index] +
                            "    'whitenoise.middleware.WhiteNoiseMiddleware',\n" +
                            settings_content[insert_index:]
                        )
                        settings_content = updated_middleware
                    else:
                        raise ValueError("SecurityMiddleware is not in MIDDLEWARE")
                else:
                    raise ValueError("MIDDLEWARE not found in settings.py")

                # Update INSTALLED_APPS
                apps_index = settings_content.find('INSTALLED_APPS = [')
                if apps_index != -1:
                    end_index = settings_content.find(']', apps_index)
                    if end_index != -1:
                        new_apps = '\n    ' + ',\n    '.join([f"'apps.{app_name}'" for app_name in app_names])
                        settings_content = settings_content[:end_index] + new_apps + settings_content[end_index:]
                    else:
                        raise ValueError("INSTALLED_APPS format is not as expected")
                else:
                    raise ValueError("INSTALLED_APPS not found in settings.py")

                # Update TEMPLATES
                templates_index = settings_content.find('TEMPLATES = [')
                if templates_index != -1:
                    dirs_index = settings_content.find("'DIRS': [", templates_index)
                    if dirs_index != -1:
                        end_dirs_index = settings_content.find(']', dirs_index)
                        if end_dirs_index != -1:
                            settings_content = (
                                settings_content[:dirs_index+8] +
                                "[BASE_DIR / 'templates'" +
                                settings_content[end_dirs_index:]
                            )
                        else:
                            raise ValueError("TEMPLATES['DIRS'] format is not as expected")
                    else:
                        raise ValueError("TEMPLATES['DIRS'] not found in settings.py")
                else:
                    raise ValueError("TEMPLATES not found in settings.py")

                # Add static and media configurations
                settings_content += "\n\nSTATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'\n"
                settings_content += "STATICFILES_DIRS = [BASE_DIR / 'static']\n"
                settings_content += "STATIC_ROOT = BASE_DIR / 'staticfiles'\n"
                settings_content += "MEDIA_URL = '/media/'\n"
                settings_content += "MEDIA_ROOT = BASE_DIR / 'media'\n"

                # Write back to settings.py
                with open(settings_path, 'w') as settings_file:
                    settings_file.write(settings_content)
            else:
                raise FileNotFoundError(f"settings.py file not found in {settings_path}")

            # Install Tailwind
            os.chdir(project_name)
            run_command(['npm', 'install', '-D', 'tailwindcss'])
            run_command(['npx', 'tailwindcss', 'init'])
            os.chdir('..')

            # Update tailwind.config.js
            tailwind_config = f"{project_name}/tailwind.config.js"
            tailwind_content = """/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        './templates/**/*.html',
        './templates/*.html',
    ],
    theme: {
        extend: {},
    },
    plugins: [],
}"""
            with open(tailwind_config, 'w') as config_file:
                config_file.write(tailwind_content)

            # Create input.css
            os.makedirs(f"{project_name}/static/css", exist_ok=True)
            with open(f"{project_name}/static/css/input.css", 'w') as input_css:
                input_css.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;")

            # Run Tailwind build command
            os.chdir(project_name)
            try:
                run_command(['npx', 'tailwindcss', '-i', './static/css/input.css', '-o', './static/css/output.css'])
            except KeyboardInterrupt:
                click.echo(click.style("Tailwind build process interrupted by user.", fg="yellow"))
            finally:
                os.chdir('..')

            # Create base.html
            base_html_content = """{% load static %}
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ldjango</title>
    <link href="{% static 'css/output.css' %}" rel="stylesheet">
    {% block head %}
    {% endblock %}
</head>

<body>
    {% block content %}
    {% endblock %}
    {% block footer %}
    {% endblock %}
</body>

</html>"""
            with open(f"{project_name}/templates/base.html", 'w') as base_html:
                base_html.write(base_html_content)

            # Update core/urls.py
            urls_path = f"{project_name}/core/urls.py"
            with open(urls_path, 'r') as urls_file:
                urls_content = urls_file.read()
            urls_content += "\nfrom django.conf import settings\n"
            urls_content += "from django.conf.urls.static import static\n\n"
            urls_content += "urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)\n"
            urls_content += "urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\n"
            with open(urls_path, 'w') as urls_file:
                urls_file.write(urls_content)

            # Run migrations and collectstatic
            os.chdir(project_name)
            run_command(['python', 'manage.py', 'migrate'])
            run_command(['python', 'manage.py', 'collectstatic', '--noinput'])

            # Generate requirements.txt
            run_command(['pip', 'freeze', '>', 'requirements.txt'])
            os.chdir('..')
            
            # Create .gitignore
            with open(f"{project_name}/.gitignore", 'w') as gitignore:
                gitignore.write('''*.pyc
*.pyo
*.pyd
*.log
*.db
*.sqlite3
*.sqlite
*.sqlite-shm
*.sqlite-wal
*.DS_Store
./dist
./media
./node_modules
./venv
/media
/static
/node_modules
.hintrc
''')

            # Ensure the progress bar reaches 100%
            while pbar.n < total_steps:
                pbar.update(1)
                time.sleep(0.1)

        click.echo(click.style(f"\n🎉 Congratulations! Project {project_name} has been successfully created with apps: {', '.join(app_names)}! 🎉", fg="green", bold=True))
        click.echo(click.style("Let's get your project up and running with these exciting steps:", fg="cyan"))
        
        click.echo(click.style("\n1. Unleash the power of Tailwind CSS:", fg="yellow"))
        click.echo(click.style(f"   cd {project_name} && npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch", fg="magenta"))
        click.echo(click.style("   (Remember to close this terminal when you're done with the Tailwind magic!)", fg="yellow"))
        
        click.echo(click.style("\n2. Gather your static assets:", fg="yellow"))
        click.echo(click.style(f"   cd {project_name} && python manage.py collectstatic", fg="magenta"))
        
        click.echo(click.style("\n3. Launch your development server:", fg="yellow"))
        click.echo(click.style(f"   cd {project_name} && python manage.py runserver", fg="magenta"))
        
        click.echo(click.style("\nYou're all set! Happy coding!", fg="green", bold=True))
    except Exception as e:
        click.echo(click.style("\n❌ An error occurred during project creation.", fg="red", bold=True))
        click.echo(click.style(f"Error details: {str(e)}", fg="red"))
        click.echo(click.style("\n❌ An error occurred during project creation.", fg="red", bold=True))
        click.echo(click.style(f"Error details: {str(e)}", fg="red"))
