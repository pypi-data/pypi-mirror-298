import os
import subprocess


def create_project_structure(project_name, app_names):
    # Create project folder
    os.makedirs(f"{project_name}/core", exist_ok=True)
    os.makedirs(f"{project_name}/apps", exist_ok=True)
    os.makedirs(f"{project_name}/templates", exist_ok=True)
    os.makedirs(f"{project_name}/media", exist_ok=True)
    os.makedirs(f"{project_name}/static", exist_ok=True)

    # Initialize Django project
    subprocess.run(['django-admin', 'startproject', 'core', f"{project_name}/core"])
    
    # Create apps
    for app_name in app_names:
        app_path = f"{project_name}/apps/{app_name}"
        subprocess.run(['django-admin', 'startapp', app_name, app_path])
        
        # Update apps.py
        app_py = f"{app_path}/apps.py"
        with open(app_py, 'r') as file:
            content = file.read()
        content = content.replace(f"name = '{app_name}'", f"name = 'apps.{app_name}'")
        with open(app_py, 'w') as file:
            file.write(content)

    # Create urls.py in apps folder
    urls_path = f"{project_name}/apps/urls.py"
    with open(urls_path, 'w') as file:
        file.write('from django.urls import path\n\nurlpatterns = []\n')

    # Create manage.py
    subprocess.run(['django-admin', 'startproject', 'core', f"{project_name}"])
    
    # Update settings.py
    settings_path = f"{project_name}/core/core/settings.py"
    with open(settings_path, 'a') as settings_file:
        for app_name in app_names:
            settings_file.write(f"\nINSTALLED_APPS.append('apps.{app_name}')")

    # Create .gitignore
    with open(f"{project_name}/.gitignore", 'w') as gitignore:
        gitignore.write('/media/\n/static/\n')

    print(f"Successfully created {project_name} with apps: {', '.join(app_names)}!")
