import os
import subprocess


def create_project_structure(project_name, app_names):
    try:
        # Create project folders
        os.makedirs(project_name, exist_ok=True)
        os.makedirs(f"{project_name}/apps", exist_ok=True)
        os.makedirs(f"{project_name}/templates", exist_ok=True)
        os.makedirs(f"{project_name}/media", exist_ok=True)
        os.makedirs(f"{project_name}/static", exist_ok=True)

        # Initialize Django project
        subprocess.run(['django-admin', 'startproject', 'core', project_name], check=True)

        # Create apps
        for app_name in app_names:
            app_path = f"{project_name}/apps/{app_name}"
            os.makedirs(app_path, exist_ok=True)  # Ensure the app folder exists

            # Create Django app inside the folder
            subprocess.run(['django-admin', 'startapp', app_name, app_path], check=True)

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
            file.write('from django.urls import path\n\nurlpatterns = []\n')

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
                end_middleware_index = settings_content.find(']', middleware_index)
                if end_middleware_index != -1:
                    updated_middleware = settings_content[:end_middleware_index] + \
                        "\n    'whitenoise.middleware.WhiteNoiseMiddleware'," + \
                        settings_content[end_middleware_index:]
                    settings_content = updated_middleware

            # Find INSTALLED_APPS position
            apps_index = settings_content.find('INSTALLED_APPS = [')
            if apps_index != -1:
                # Find the end of INSTALLED_APPS
                end_index = settings_content.find(']', apps_index)
                if end_index != -1:
                    # Insert new apps
                    new_apps = '\n    ' + ',\n    '.join([f"'apps.{app_name}'" for app_name in app_names])
                    updated_content = settings_content[:end_index] + new_apps + settings_content[end_index:]
                    
                    # Write back to settings.py
                    with open(settings_path, 'w') as settings_file:
                        settings_file.write(updated_content)
                else:
                    raise ValueError("INSTALLED_APPS format is not as expected")
            else:
                raise ValueError("INSTALLED_APPS not found in settings.py")
        else:
            raise FileNotFoundError(f"settings.py file not found in {settings_path}")

        # Update TEMPLATES
        templates_index = settings_content.find('TEMPLATES = [')
        if templates_index != -1:
            dirs_index = settings_content.find("'DIRS': [", templates_index)
            if dirs_index != -1:
                end_dirs_index = settings_content.find(']', dirs_index)
                if end_dirs_index != -1:
                    updated_content = (
                        settings_content[:dirs_index+8] +
                        "[BASE_DIR / 'templates'" +
                        settings_content[end_dirs_index:]
                    )
                    
                    # Write back to settings.py
                    with open(settings_path, 'w') as settings_file:
                        settings_file.write(updated_content)
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

        # Install Tailwind
        os.chdir(project_name)
        subprocess.run(['npm', 'install', '-D', 'tailwindcss'], check=True)
        subprocess.run(['npx', 'tailwindcss', 'init'], check=True)
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
            subprocess.run(['npx', 'tailwindcss', '-i', './static/css/input.css', '-o', './static/css/output.css'], check=True)
        except KeyboardInterrupt:
            print("Tailwind build process interrupted by user.")
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
        subprocess.run(['python', 'manage.py', 'migrate'], check=True)
        subprocess.run(['python', 'manage.py', 'collectstatic', '--noinput'], check=True)
        os.chdir('..')

        # Create .gitignore
        with open(f"{project_name}/.gitignore", 'w') as gitignore:
            gitignore.write('/media/\n/static/\n')

        print(f"Successfully created {project_name} with apps: {', '.join(app_names)}!")
        print("Tailwind has been installed and configured.")
        print("To start the Tailwind watch process, run:")
        print(f"cd {project_name} && npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
