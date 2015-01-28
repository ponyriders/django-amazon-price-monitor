<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](http://doctoc.herokuapp.com/)*

- [django-amazon-price-monitor](#django-amazon-price-monitor)
  - [What does it do?](#what-does-it-do)
  - [Setup](#setup)
    - [Prerequisites](#prerequisites)
    - [Included angular libraries](#included-angular-libraries)
    - [Basic setup](#basic-setup)
    - [South](#south)
    - [Settings](#settings)
      - [Must have settings](#must-have-settings)
        - [AWS and Product Advertising API credentials](#aws-and-product-advertising-api-credentials)
        - [Images protocol and domain](#images-protocol-and-domain)
      - [Nice to have settings](#nice-to-have-settings)
        - [Product synchronization](#product-synchronization)
        - [Notifications](#notifications)
        - [Caching](#caching)
    - [Celery settings](#celery-settings)
  - [Management Commands](#management-commands)
  - [Loggers](#loggers)
    - [price_monitor](#price_monitor)
    - [price_monitor.product_advertising_api](#price_monitorproduct_advertising_api)
  - [Models](#models)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# django-amazon-price-monitor

Monitors prices of Amazon products via Product Advertising API.
Relies on python-amazon-simple-product-api under the hood.

| Branch          | Build status |
| --------------- | ------------ |
| master          | [![Build Status](https://travis-ci.org/ponyriders/django-amazon-price-monitor.svg?branch=master)](https://travis-ci.org/ponyriders/django-amazon-price-monitor) |
| angular-frontend | [![Build Status](https://travis-ci.org/ponyriders/django-amazon-price-monitor.svg?branch=angular-frontend)](https://travis-ci.org/ponyriders/django-amazon-price-monitor) |
| data-reduction  | [![Build Status](https://travis-ci.org/ponyriders/django-amazon-price-monitor.svg?branch=data-reduction)](https://travis-ci.org/ponyriders/django-amazon-price-monitor) |

## What does it do?

*TODO add a description and a workflow view*

## Setup

### Prerequisites

- Python 2.7, 3.2, 3.3, 3.4

```
Django>=1.5,<1.7
djangorestframework>=2.3.13
beautifulsoup4>=4.3.2
bottlenose>=0.6.2
celery>=3
six
```

### Included angular libraries

- angular-django-rest-resource ([commit: 81d752b363668d674201c09d7a2ce6f418a44f13](https://github.com/blacklocus/angular-django-rest-resource/tree/81d752b363668d674201c09d7a2ce6f418a44f13))

### Basic setup

Add the app "price_monitor" to *INSTALLED_APPS*:

    INSTALLED_APPS = (
        ...
        'price_monitor',
    )

### South

The app also supports [South](http://south.readthedocs.org/en/latest/).


### Settings

_The values of the following displayed settings are their default values. If the value is '...' then there is no default value._ 

#### Must have settings

The following settings are absolutely necessary to the price monitor running, please set them:

##### AWS and Product Advertising API credentials

```
# your Amazon Web Services access key id
PRICE_MONITOR_AWS_ACCESS_KEY_ID = '...'

# your Amazon Web Services secret access key
PRICE_MONITOR_AWS_SECRET_ACCESS_KEY = '...'

# the region endpoint you want to use.
# Typically the country you'll run the price monitor in.
# possible values: CA, CN, DE, ES, FR, IT, JP, UK, US
PRICE_MONITOR_AMAZON_PRODUCT_API_REGION = '...'

# the assoc tag of the Amazon Product Advertising API
PRICE_MONITOR_AMAZON_PRODUCT_API_ASSOC_TAG = '...'
```

##### Images protocol and domain

```
# if to use the HTTPS URLs for Amazon images.
# if you're running the monitor on SSL, set this to True
# INFO:
#  Product images are served directly from Amazon.
#  This is a restriction when using the Amazon Product Advertising API
PRICE_MONITOR_IMAGES_USE_SSL = True

# domain to use for image serving.
# typically analog to the api region following the URL pattern
#  https://images-<REGION>.ssl-images-amazon.com
PRICE_MONITOR_AMAZON_SSL_IMAGE_DOMAIN = 'https://images-eu.ssl-images-amazon.com'
```

#### Nice to have settings

The following settings can be adjusted but come with reasonable default values.

##### Product synchronization
 
```
# period of running the product synchronization task in minutes
PRICE_MONITOR_PRODUCTS_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES = 5

# number of products to synchronize on each run of the synchronize task.
# The maximum allowed value is 10 (as restriction when using the 
#  Amazon Product Advertising API)
PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT = 10

# time after which products shall be refreshed
# Amazon only allows caching up to 24 hours, so the maximum value is 1440!
PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES = 720  # 12 hours
```

##### Notifications

To be able to send out the notification emails, set up a proper email backend (see
[Django documentation](https://docs.djangoproject.com/en/1.5/topics/email/#topic-email-backends)).

```
# time after which to notify the user again about a price limit hit (in minutes)
PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES = 10080  # 7 days

# sender address of the notification email
PRICE_MONITOR_EMAIL_SENDER = 'noreply@localhost'

# currency name to use on notifications
PRICE_MONITOR_DEFAULT_CURRENCY = 'EUR'

# subject and body of the notification emails
gettext = lambda x: x
PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT = gettext(
    'Price limit for %(product)s reached'
)
PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY = gettext(
    'The price limit of %(price_limit)0.2f %(currency)s has been reached for the '
    'article "%(product_title)s" - the current price is %(price)0.2f %(currency)s.'
    '\n\nPlease support our platform by using this '
    'link for buying: %(link)s\n\n\nRegards,\nThe Team'
)

# name of the site in notifications
PRICE_MONITOR_SITENAME = 'Price Monitor'
```

##### Caching

```
# key of cache (according to project config) to use for graphs
# None disables caching.
PRICE_MONITOR_GRAPH_CACHE_NAME = None

# prefix for cache key used for graphs
PRICE_MONITOR_GRAPH_CACHE_KEY_PREFIX = 'graph_'
```

### Celery settings

To be able to run the required Celery tasks, Celery itself has to be set up. Please see the
[Celery Documentation](http://docs.celeryproject.org/en/latest/index.html) about how to setup the whole thing. You'll need a broker and a result backend
configured.


## Management Commands
There is a management command to batch create a number of products by providing their ASIN:

    python manage.py price_monitor_batch_create_products "<ASIN1>,<ASIN2>,<ASIN3>"


## Loggers

### price_monitor

The app uses the logger "price_monitor" to log all error and info messages that are not included within a dedicated other logger.
Please see the [Django logging documentation](https://docs.djangoproject.com/en/1.5/topics/logging/ "Django logging documentation") for how to setup loggers.

### price_monitor.product_advertising_api

Logger for everything related to the ProductAdvertisingAPI wrapper class that accesses the Amazon Product Advertising API through bottlenose.

### price_monitor.utils

Logger for the utils module.


## Models

![Model Graph](https://github.com/ponyriders/django-amazon-price-monitor/raw/master/models.png "Model Graph")
