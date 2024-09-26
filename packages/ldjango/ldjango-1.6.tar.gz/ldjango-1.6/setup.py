import pkg_resources
from setuptools import find_packages, setup


def get_latest_version(package):
    try:
        return pkg_resources.get_distribution(package).version
    except pkg_resources.DistributionNotFound:
        return None

required_packages = ['Click', 'Django']
install_requires = [f"{pkg}>={get_latest_version(pkg) or '0'}" for pkg in required_packages]

setup(
    name='ldjango',
    version='1.6',
    packages=find_packages(),
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

