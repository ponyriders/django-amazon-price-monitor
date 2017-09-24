#!/usr/bin/env python
"""Setup file for the django-amazon-price-monitor package."""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


readme = open('README.rst').read()
history = open('HISTORY.rst').read()

setup(
    name='django-amazon-price-monitor',
    version=__import__('price_monitor').get_version().replace(' ', '-'),
    description='Monitors prices of Amazon products via Product Advertising API',
    long_description=readme + '\n\n' + history,
    author='Alexander Herrmann, Martin Mrose',
    author_email='django-amazon-price-monitor@googlegroups.com',
    url='https://github.com/ponyriders/django-amazon-price-monitor',
    packages=[
        'price_monitor'
    ],
    include_package_data=True,
    install_requires=[
        # main dependencies
        'Django>=1.8,<2',
        # for product advertising api
        'beautifulsoup4',
        'bottlenose>=0.6.2',
        'celery>=4,<5',
        'python-dateutil>=2.5.1',
        # for pm api
        'djangorestframework>=3.3',
        # for graphs
        'pygal>=2.0.7',
        'lxml',
        # pygal png output
        'CairoSVG<2',
        'tinycss',
        'cssselect',
    ],
    license='MIT',
    zip_safe=False,
)
