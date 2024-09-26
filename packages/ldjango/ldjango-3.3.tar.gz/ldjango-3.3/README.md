# 🐍 ldjango: Your Django Project Sidekick! 🚀

[![PyPI version](https://badge.fury.io/py/ldjango.svg)](https://badge.fury.io/py/ldjango)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Tired of setting up Django projects manually? Meet `ldjango` - your magical wand for creating perfectly structured Django projects in a snap! 🪄✨


## 🎥 See ldjango in Action!

![Demo ldjango](https://raw.githubusercontent.com/lrndwy/ldjango/main/Screen%20Recording%20Sept%2026%20(1).gif)

Watch how ldjango creates a Django project easily and quickly!



## 🌟 What's So Special?

- **Lightning-Fast Setup**: Create a fully structured Django project with just one command!
- **Smart App Generation**: Craft multiple Django apps automagically!
- **Perfect Project Structure**: Get an organized project layout that even Marie Kondo would approve!
- **CLI Superpowers**: Use intuitive command-line options to customize your project creation.
- **Tailwind CSS Integration**: Enjoy the power of Tailwind CSS right out of the box!
- **Static Files**: Static files are automatically compiled and ready for production.
- **Media Files**: Media files are stored in a dedicated folder for easy management.
- **Git-Friendly**: Comes with a `.gitignore` file. Because we care about your repo's cleanliness.
- **Dedicated Static Folder**: Keep your static files organized and separate from your project.
- **HTML Templates**: Use a base template for your HTML to maintain consistency across your project.
- **Django Settings**: A well-organized settings file to manage your project configurations.
- **URL Routing**: A centralized URL routing system to manage all your app URLs.
- **Database**: Uses SQLite by default, but you can easily switch to your preferred database.
- **JavaScript Support**: Includes a `node_modules` folder for managing JavaScript dependencies.
- **NPM Scripts**: Use NPM scripts to compile your CSS and run other development tasks.
- **Django Commands**: Use Django commands to manage your project and apps.
- **Version Control**: Includes a `.gitignore` file to exclude unnecessary files from your repository.


## 🛠️ Installation

To get started with `ldjango`, follow these steps:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

2. Activate the virtual environment:
   - For Windows:
     ```bash
     venv\Scripts\activate
     ```
   - For macOS and Linux:
     ```bash
     source venv/bin/activate
     ```

3. Install `ldjango`:
   ```bash
   pip install ldjango
   ```

Now `ldjango` is ready to use in your virtual environment!

## 🚀 Quickstart

Launch your Django rocket with this simple command:

```bash
ldjango makeproject
```

Follow the prompts, and watch the magic happen! ✨

## 📚 Command Reference

- `ldjango makeproject`: Start the interactive project creation wizard
- `ldjango -h` or `ldjango --help`: Display help information
- `ldjango --version`: Show the version of ldjango you're using

## 📁 The ldjango Special: Project Structure

Your shiny new Django project will look like this:

```
project_root/
│
├── apps/                       # Main folder containing all the applications in the Django project
│   ├── apps1/                   # First application (apps1) in the project
│   │   ├── migrations/          # Folder to store database migration files
│   │   ├── admin.py             # Configuration for Django's admin panel
│   │   ├── apps.py              # Configuration for the app in Django
│   │   ├── models.py            # Defines the database models for this app
│   │   ├── tests.py             # File to write unit tests
│   │   ├── views.py             # Logic for handling views in this app
│
│   ├── apps2/                   # Second application (apps2) in the project
│   │   ├── migrations/          # Folder to store database migration files
│   │   ├── admin.py             # Configuration for Django's admin panel
│   │   ├── apps.py              # Configuration for the app in Django
│   │   ├── models.py            # Defines the database models for this app
│   │   ├── tests.py             # File to write unit tests
│   │   ├── views.py             # Logic for handling views in this app
│
│   ├── More another apps/       # More apps in the project
│
│   ├── urls.py                  # URL routing for all the apps inside the `apps` folder
│
├── core/                        # Core folder containing overall project configuration
│   ├── asgi.py                  # ASGI configuration for running asynchronous servers
│   ├── settings.py              # Main configuration file for the Django project
│   ├── urls.py                  # Global URL routing for the entire project
│   ├── wsgi.py                  # WSGI configuration for running web servers
│
├── media/                       # Folder for storing user-uploaded files (images, documents, etc.)
│
├── node_modules/                # Folder containing JavaScript dependencies from npm (e.g., for Tailwind CSS)
│
├── static/                      # Folder for static files like CSS, JavaScript, and images
│   └── css/
│       ├── input.css            # Input CSS file (e.g., Tailwind CSS)
│       ├── output.css           # Output CSS file after processing
│
├── staticfiles/                 # Folder to store static files that are ready for production
│   ├── admin/                   # Static files for Django's admin panel
│   └── css/                     # Additional CSS files for the app
│
├── templates/                   # Folder for storing HTML templates
│   ├── base.html                # Base HTML template for the application
│
├── .gitignore                   # File to specify files/folders that Git should ignore
├── db.sqlite3                   # SQLite database used by the project
├── manage.py                    # Command-line script to manage the Django project
├── package-lock.json            # File locking the versions of npm dependencies
├── package.json                 # Configuration file for npm dependencies
└── tailwind.config.js           # Configuration file for Tailwind CSS

```

## 🎭 Features That'll Make You Go "Wow!"

1. **App-tastic Organization**: All your apps neatly tucked into the `apps` folder. No more app chaos!
2. **URL Mastery**: A pre-configured `urls.py` in the `apps` folder to rule all your app URLs.
3. **Ready, Set, Django**: `core` folder with all the Django project essentials, ready to rock.
4. **Static & Media**: Dedicated folders for your static files and media. Marie Kondo would be proud!
5. **Git-Friendly**: Comes with a `.gitignore` file. Because we care about your repo's cleanliness.
6. **Tailwind CSS Integration**: Enjoy the power of Tailwind CSS right out of the box!
7. **HTML Templates**: Use a base template for your HTML to maintain consistency across your project.
8. **Django Settings**: A well-organized settings file to manage your project configurations.
9. **Database**: Uses SQLite by default, but you can easily switch to your preferred database.
10. **JavaScript Support**: Includes a `node_modules` folder for managing JavaScript dependencies.
11. **NPM Scripts**: Use NPM scripts to compile your CSS and run other development tasks.
12. **Django Commands**: Use Django commands to manage your project and apps.

## 🤔 Why Choose ldjango?

- **Time-Saver Supreme**: Say goodbye to repetitive project setup tasks.
- **Consistency Champion**: Every project follows the same clean, logical structure.
- **Beginner's Best Friend**: Perfect for Django newbies to start on the right foot.
- **Customization King**: Flexible enough to adapt to your unique project needs.
- **Tailwind CSS**: Tailwind CSS is integrated into the project, so you can start styling your project right away.
- **Static Files**: Static files are automatically compiled and ready for production.
- **Media Files**: Media files are stored in a dedicated folder for easy management.
- **Git-Friendly**: Comes with a `.gitignore` file. Because we care about your repo's cleanliness.
- **Dedicated Static Folder**: Keep your static files organized and separate from your project.
- **HTML Templates**: Use a base template for your HTML to maintain consistency across your project.
- **Django Settings**: A well-organized settings file to manage your project configurations.
- **URL Routing**: A centralized URL routing system to manage all your app URLs.
- **Database**: Uses SQLite by default, but you can easily switch to your preferred database.
- **JavaScript Support**: Includes a `node_modules` folder for managing JavaScript dependencies.
- **NPM Scripts**: Use NPM scripts to compile your CSS and run other development tasks.


## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Let's Connect!

Liaranda - [@lrnd.__](https://instagram.com/lrnd.__) - hafiztamvan15@gmail.com

Project Link: [Liaranda](https://github.com/lrndwy)

---

Ready to djangofy your development process? Give ldjango a spin and watch your productivity soar! 🚀🐍

