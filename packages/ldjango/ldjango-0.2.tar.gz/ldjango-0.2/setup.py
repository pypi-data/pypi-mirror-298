from setuptools import find_packages, setup

setup(
    name='ldjango',
    version='0.2',
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
)
