django-amazon-price-monitor
===========================

Monitors prices of Amazon products via Product Advertising API.
Relies on python-amazon-simple-product-api under the hood.


Setup
=====

Add the app "price_monitor" to *INSTALLED_APPS*:

    INSTALLED_APPS = (
        ...
        'price_monitor',
    )

Add the following settings to your settings file:

    AWS_ACCESS_KEY_ID = '<your-aws-access-key>'
    AWS_SECRET_ACCESS_KEY = '<your-aws-secret-key>

*You can get these values from the accounts area of your Amazon account.*

Set the setting for selecting the Amazon region store and your associate handle:

     # possible values: ['US', 'FR', 'CN', 'UK', 'CA', 'DE', 'JP', 'IT', 'ES']
     AMAZON_PRODUCT_API_REGION = 'DE'

     # can be found in your Amazon associate account
     AMAZON_PRODUCT_API_ASSOC_TAG = '<your-assoc-tag>'

Celery tasks
============

TODO add description, defaults and recommended settings
