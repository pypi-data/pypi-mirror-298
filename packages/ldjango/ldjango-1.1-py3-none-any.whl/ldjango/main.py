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

        # Create .gitignore
        with open(f"{project_name}/.gitignore", 'w') as gitignore:
            gitignore.write('/media/\n/static/\n')

        print(f"Successfully created {project_name} with apps: {', '.join(app_names)}!")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
