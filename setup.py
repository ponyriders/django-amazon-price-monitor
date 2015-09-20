#!/usr/bin/env python
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
        'Django<1.9',
        'six',  # TODO still relevant?
        # for product advertising api
        'beautifulsoup4',
        'bottlenose>=0.6.2',
        'celery>=3',
        'python-dateutil',
        # for pm api
        'djangorestframework>=3.0.4',
        # for graphs
        'pygal>=1.5.1',
        'lxml',
        # pygal png output
        'CairoSVG',
        'tinycss',
        'cssselect',
    ],
    license='MIT',
    zip_safe=False,
)
