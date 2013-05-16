#!/usr/bin/env python
from setuptools import setup


setup(
    name='django-amazon-price-monitor',
    description='Monitors prices of Amazon products via Product Advertising API',
    version='0.1.0',
    author='Alexander Herrmann & Martin Mrose',
    author_email='mrosemartin84@gmail.com',
    license='MIT',
    url='https://github.com/ponyriders/django-amazon-price-monitor',
    packages=['django_amazon_price_monitor'],
    long_description=open('README.md').read(),
    install_requires=[
        'python-amazon-simple-product-api==1.4.0',
    ],
    dependency_links=[
    ]
)
