#!/usr/bin/env python
from setuptools import setup


def get_requirements(requirements_file='requirements.txt'):
    """
    Returns a list of package requirements read from the given file.
    :param requirements_file: the file to read
    :return: list of package requirements
    """
    with open(requirements_file, 'r') as f:
        return [line for line in f.read().splitlines() if not line.startswith('#')]

setup(
    name='django-amazon-price-monitor',
    description='Monitors prices of Amazon products via Product Advertising API',
    version=__import__('price_monitor').get_version().replace(' ', '-'),
    author='Alexander Herrmann & Martin Mrose',
    author_email='mrosemartin84@gmail.com',
    license='MIT',
    url='https://github.com/ponyriders/django-amazon-price-monitor',
    packages=['price_monitor'],
    long_description=open('README.md').read(),
    install_requires=get_requirements(),
    tests_require=get_requirements('requirements_test.txt'),
    dependency_links=[]
)
