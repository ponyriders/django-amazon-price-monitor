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
    AWS_SECRET_ACCESS_KEY = '<your-aws-secret-key>'

*You can get these values from the accounts area of your Amazon account.*

Set the setting for selecting the Amazon region store and your associate handle:

     # possible values: ['US', 'FR', 'CN', 'UK', 'CA', 'DE', 'JP', 'IT', 'ES']
     AMAZON_PRODUCT_API_REGION = 'DE'

     # can be found in your Amazon associate account
     AMAZON_PRODUCT_API_ASSOC_TAG = '<your-assoc-tag>'

TODO: add necessary celery settings: BROKER_URL, CELERY_RESULT_DBURI, ?
TODO: add the other settings!


Celery Tasks
============
The app uses [Celery](http://celeryproject.org) as distributed task queue. The following tasks are consumed:

ProductSynchronizeTask (PeriodicTask)
-------------------------------------

This is the Celery task responsible for the synchronization of products:

Syncs the products initially created with only the ASIN and updates products with a last synchronization date older than
settings.AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES (number of minutes). Prices for these products are created, too.
Runs by default every 5 minutes, overwrite the run time by setting the PRICE_MONITOR_PRODUCT_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES setting.

NotifySubscriberTask (Task)
---------------------------
Sends out an email to a single subscriber of a product that has reached the price limit. Is called through ProductSynchronizeTask.


Management Commands
===================
There is a management command to batch create a number of products by providing their ASIN:

    python manage.py price_monitor_batch_create_products "<ASIN1>,<ASIN2>,<ASIN3>"


Logger
======

The app uses the logger "price_monitor" to log error and info messages.
Please see the [Django logging documentation](https://docs.djangoproject.com/en/1.5/topics/logging/ "Django logging documentation") for how to setup loggers.