from setuptools import find_packages, setup

longDesc = """
# 🐍 ldjango: Your Django Project Sidekick! 🚀

[![PyPI version](https://badge.fury.io/py/ldjango.svg)](https://badge.fury.io/py/ldjango)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Tired of setting up Django projects manually? Meet `ldjango` - your magical wand for creating perfectly structured Django projects in a snap! 🪄✨

## 🌟 What's So Special?

- **Lightning-Fast Setup**: Create a fully structured Django project with just one command!
- **Smart App Generation**: Craft multiple Django apps automagically!
- **Perfect Project Structure**: Get an organized project layout that even Marie Kondo would approve!
- **CLI Superpowers**: Use intuitive command-line options to customize your project creation.

## 🛠️ Installation

Getting `ldjango` is easier than eating a slice of pizza:

```bash
pip install ldjango
```

## 🚀 Quickstart

Launch your Django rocket with this simple command:

```bash
ldjango makeproject
```

Follow the prompts, and watch the magic happen! ✨

## 📚 Command Reference

- `ldjango makeproject`: Start the interactive project creation wizard
- `ldjango -h` or `ldjango makeproject --help`: Display help information
- `ldjango --version`: Show the version of ldjango you're using

## 📁 The ldjango Special: Project Structure

Your shiny new Django project will look like this:

```
/YourAwesomeProject
├── /core (Django Project)
│   ├── settings.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── urls.py
├── /apps
│   ├── /your_cool_app1
│   │   └── [standard Django app files]
│   ├── /your_awesome_app2
│   │   └── [standard Django app files]
│   └── urls.py
├── /static
├── /media
├── /templates
├── manage.py
└── .gitignore
```

## 🎭 Features That'll Make You Go "Wow!"

1. **App-tastic Organization**: All your apps neatly tucked into the `apps` folder. No more app chaos!
2. **URL Mastery**: A pre-configured `urls.py` in the `apps` folder to rule all your app URLs.
3. **Ready, Set, Django**: `core` folder with all the Django project essentials, ready to rock.
4. **Static & Media**: Dedicated folders for your static files and media. Marie Kondo would be proud!
5. **Git-Friendly**: Comes with a `.gitignore` file. Because we care about your repo's cleanliness.

## 🤔 Why Choose ldjango?

- **Time-Saver Supreme**: Say goodbye to repetitive project setup tasks.
- **Consistency Champion**: Every project follows the same clean, logical structure.
- **Beginner's Best Friend**: Perfect for Django newbies to start on the right foot.
- **Customization King**: Flexible enough to adapt to your unique project needs.

## 🤝 Wanna Make ldjango Even More Awesome?

We love contributions! Here's how you can join the ldjango enhancement party:

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/CoolNewFeature`)
3. Commit your changes (`git commit -m 'Add some CoolNewFeature'`)
4. Push to the branch (`git push origin feature/CoolNewFeature`)
5. Open a Pull Request and let's chat!

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 📞 Let's Connect!

Liaranda - [@your_twitter](https://twitter.com/your_twitter) - hafiztamvan15@gmail.com

Project Link: [Liaranda](https://github.com/lrndwy)

---

Ready to djangofy your development process? Give ldjango a spin and watch your productivity soar! 🚀🐍
"""

setup(
    name='ldjango',
    version='1.1',
    packages=find_packages(),
    install_requires=[
        'Click',
        'Django',
    ],
    entry_points={
        'console_scripts': [
            'ldjango = ldjango.cli:cli',
        ],
    },
    description='CLI tool for creating Django projects with a predefined structure.',
    long_description=longDesc,
    author='Liaranda',
    author_email='hafiztamvan15@gmail.com',
    license='MIT',
)
