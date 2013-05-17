django-amazon-price-monitor
===========================

Monitors prices of Amazon products via Product Advertising API


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