# django-amazon-price-monitor

Monitors prices of Amazon products via Product Advertising API.
Relies on python-amazon-simple-product-api under the hood.

| Branch  | Build status |
| --------| ------------ |
| master  | [![Build Status](https://travis-ci.org/ponyriders/django-amazon-price-monitor.svg?branch=master)](https://travis-ci.org/ponyriders/django-amazon-price-monitor) |
| angular  | [![Build Status](https://travis-ci.org/ponyriders/django-amazon-price-monitor.svg?branch=angular-frontend)](https://travis-ci.org/ponyriders/django-amazon-price-monitor) |

## Setup

### Prerequisites

- Python 2.7, 3.2, 3.3, 3.4
- Django >= 1.5
- Celery >= 3
- six
- redis

### Included angular libraries

- angular-django-rest-resource [commit: 81d752b363668d674201c09d7a2ce6f418a44f13](https://github.com/blacklocus/angular-django-rest-resource/tree/81d752b363668d674201c09d7a2ce6f418a44f13)

### Basic setup

Add the app "price_monitor" and the to apps for websockets to *INSTALLED_APPS*:

    INSTALLED_APPS = (
        ...
        'djangular',
        'ws4redis',
        'price_monitor',
    )

### South

The app also supports [South](http://south.readthedocs.org/en/latest/).

### Amazon account details
*You can get these values from the accounts area of your Amazon account.*

Add the following settings to your settings file:

    AWS_ACCESS_KEY_ID = '<your-aws-access-key>'
    AWS_SECRET_ACCESS_KEY = '<your-aws-secret-key>'

Set the setting for selecting the Amazon region store and your associate handle:

     # possible values: ['US', 'FR', 'CN', 'UK', 'CA', 'DE', 'JP', 'IT', 'ES']
     AMAZON_PRODUCT_API_REGION = 'DE'

     # can be found in your Amazon associate account
     AMAZON_PRODUCT_API_ASSOC_TAG = '<your-assoc-tag>'

### Celery settings

To be able to run the required Celery tasks, Celery itself has to be set up. Please see the
[Celery Documentation](http://docs.celeryproject.org/en/latest/index.html) about how to setup the whole thing. You'll need a broker and a result backend
configured.

The following tasks are consumed:

#### ProductsSynchronizeTask (PeriodicTask)

This is the Celery task responsible for the synchronization of products:

Syncs the products initially created with only the ASIN and updates products with a last synchronization date older than
settings.PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES (number of minutes). Prices for these products are created, too.
Runs by default every 5 minutes, overwrite the run time by setting the PRICE_MONITOR_PRODUCTS_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES setting.

#### ProductSynchronizeTask (Task)

A task for synchronizing a single product. Is called after the creation of new product.

#### NotifySubscriberTask (Task)
Sends out an email to a single subscriber of a product that has reached the price limit. Is called through ProductSynchronizeTask.

### Email notifications
To be able to send out the notification emails, set up a proper email backend (see
[Django documentation](https://docs.djangoproject.com/en/1.5/topics/email/#topic-email-backends)) and set the PRICE_MONITOR_EMAIL_SENDER setting to the email
the mails are sent from.

### All settings listed
This is a list of all settings that can be overwritten:

<table>
<tr>
    <th>Name</th>
    <th>Description</th>
    <th>Default value</th>
    <th>Required?</th>
</tr>
<tr>
    <td>AWS_ACCESS_KEY_ID</td>
    <td>Access key to use Amazon Product Advertising API. Can be found in AWS Management Console.</td>
    <td>(empty)</td>
    <td>yes</td>
</tr>
<tr>
    <td>AWS_SECRET_ACCESS_KEY</td>
    <td>Secret access key to use Amazon Product Advertising API. Can be found in AWS Management Console.</td>
    <td>(empty)</td>
    <td>yes</td>
</tr>
<tr>
    <td>AMAZON_PRODUCT_API_REGION</td>
    <td>Region code to use for monitoring products. Set to your country id.</td>
    <td>(empty)</td>
    <td>yes</td>
</tr>
<tr>
    <td>AMAZON_PRODUCT_API_ASSOC_TAG</td>
    <td>Tracking id enable for use with Product Advertising API. Can be found in Amazon PartnerNet account.</td>
    <td>(empty)</td>
    <td>yes</td>
</tr>
<tr>
    <td>PRICE_MONITOR_EMAIL_SENDER</td>
    <td>Email sender address of notification emails.</td>
    <td>noreply@localhost</td>
    <td>yes</td>
</tr>
<tr>
    <td>PRICE_MONITOR_DEFAULT_CURRENCY</td>
    <td>The default currency - used for display in frontend.</td>
    <td>EUR</td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_PRODUCT_SYNCHRONIZE_TASK_RUN_EVERY_MINUTES</td>
    <td>Run the ProductSynchronizeTask every this minutes.</td>
    <td>5</td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_AMAZON_PRODUCT_SYNCHRONIZE_COUNT</td>
    <td>Number of products to query with one call to Product Advertising API. Maximum allowed value is 10.</td>
    <td>10</td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_AMAZON_PRODUCT_REFRESH_THRESHOLD_MINUTES</td>
    <td>Time after which products shall be refreshed (in minutes).</td>
    <td>12 * 60</td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_SUBSCRIPTION_RENOTIFICATION_MINUTES</td>
    <td>Time after when to notify a user about an already notified subscription again (in minutes).</td>
    <td>60 * 24 * 7</td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_SUBJECT</td>
    <td>Notification email subject.</td>
    <td>'Price limit for %(product)s reached'</td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_I18N_EMAIL_NOTIFICATION_BODY</td>
    <td>Notification email body.</td>
    <td>
        'The price limit of %(price_limit)0.2f %(currency)s has been reached for the article "%(product_title)s" - the current price is %(price)0.2f
        %(currency)s.\n\nPlease support our platform by using this link for buying: %(link)s\n\n\nRegards,\nThe Team'
    </td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_SITENAME</td>
    <td>The name of your site. Used in price tooltips.</td>
    <td>'Price Monitor'</td>
    <td>no</td>
</tr>
<tr>
    <td>PRICE_MONITOR_ASIN_REGEX</td>
    <td>Regular expression for validating ASINs</td>
    <td>'[A-Z0-9]+'</td>
    <td>no</td>
</tr>
</table>


## Management Commands
There is a management command to batch create a number of products by providing their ASIN:

    python manage.py price_monitor_batch_create_products "<ASIN1>,<ASIN2>,<ASIN3>"


## Logger

The app uses the logger "price_monitor" to log error and info messages.
Please see the [Django logging documentation](https://docs.djangoproject.com/en/1.5/topics/logging/ "Django logging documentation") for how to setup loggers.


## Models

![Model Graph](https://github.com/ponyriders/django-amazon-price-monitor/raw/master/models.png "Model Graph")
