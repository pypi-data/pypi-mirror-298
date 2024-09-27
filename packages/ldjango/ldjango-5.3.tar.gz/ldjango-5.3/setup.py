import pkg_resources
from setuptools import find_packages, setup

from ldjango.cli import version


def get_latest_version(package):
    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        return None

required_packages = ['Click', 'Django','whitenoise','tqdm','colorama','prompt-toolkit']
install_requires = [f"{pkg}>={get_latest_version(pkg) or '0'}" for pkg in required_packages]

setup(
    name='ldjango',
    version=version,
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
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


