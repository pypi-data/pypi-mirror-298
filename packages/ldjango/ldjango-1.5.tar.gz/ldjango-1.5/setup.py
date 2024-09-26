from setuptools import find_packages, setup

setup(
    name='ldjango',
    version='1.5',
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
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Liaranda',
    author_email='hafiztamvan15@gmail.com',
    license='MIT',
)
