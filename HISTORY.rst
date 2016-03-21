Change Log
==========

TO_BE_ANNOUNCED
---------------
**Features:**

- removed ``urlpatterns`` to please Django 1.10 deprecation
- added docker setup for development (`PR#101 <https://github.com/ponyriders/django-amazon-price-monitor/pull/101>`__)
- list products with audience rating 18+ in notification mail if region is Germany and product is also 18+ `#92 <https://github.com/ponyriders/django-amazon-price-monitor/issues/92>`__ (`PR#93 <https://github.com/ponyriders/django-amazon-price-monitor/pull/93>`__)

**Bugfixes:**

- now catching parsing errors of returned XML from Amazon API `#96 <https://github.com/ponyriders/django-amazon-price-monitor/issues/96>`__
- fixed date range of displayed prices in price graph `#90 <https://github.com/ponyriders/django-amazon-price-monitor/issues/90>`__
- fixed display of old prices of price graph `#97 <https://github.com/ponyriders/django-amazon-price-monitor/issues/97>`__
- updated to latest ``python-dateutil`` version, somehow refs `#95 <https://github.com/ponyriders/django-amazon-price-monitor/issues/95>`__

`0.6.1 <https://pypi.python.org/pypi/django-amazon-price-monitor/0.6.1>`__
--------------------------------------------------------------------------
**Bugfixes:**

- StartupTask fails with exception `#94 <https://github.com/ponyriders/django-amazon-price-monitor/issues/94>`__
- Tests fail if today is the last day of November `#95 <https://github.com/ponyriders/django-amazon-price-monitor/issues/95>`__

`0.6 <https://pypi.python.org/pypi/django-amazon-price-monitor/0.6>`__
----------------------------------------------------------------------
**Features:**

- djangorestframework 3.2 compatibility `#86 <https://github.com/ponyriders/django-amazon-price-monitor/issues/86>`__ (`PR#88 <https://github.com/ponyriders/django-amazon-price-monitor/pull/88>`__)

**Bugfixes:**

- FindProductsToSynchronizeTask is rescheduled twice or more `#89 <https://github.com/ponyriders/django-amazon-price-monitor/issues/89>`__ (`PR#91 <https://github.com/ponyriders/django-amazon-price-monitor/pull/91>`__)
- Unable to parse 2015-02 to a datetime `#57 <https://github.com/ponyriders/django-amazon-price-monitor/issues/57>`__
- lots of codestyle
- minor bugfixes

`0.5 <https://pypi.python.org/pypi/django-amazon-price-monitor/0.5>`__
----------------------------------------------------------------------
**Features:**

- Add link to PM frontend in notification email `#76 <https://github.com/ponyriders/django-amazon-price-monitor/issues/76>`__
- Django 1.9 support (see `pull request #80 <https://github.com/ponyriders/django-amazon-price-monitor/pull/80>`__)

**Bugfixes:**

- FindProductsToSynchronizeTask is not always rescheduled `#61 <https://github.com/ponyriders/django-amazon-price-monitor/issues/61>`__
- Font files not included in package `#75 <https://github.com/ponyriders/django-amazon-price-monitor/issues/75>`__
- Identify as Amazon associate `#77 <https://github.com/ponyriders/django-amazon-price-monitor/issues/77>`__

**Pull requests:**

- Ensured that FindProductsToSynchronizeTask will be scheduled `#78 <https://github.com/ponyriders/django-amazon-price-monitor/pull/78>`__ (`dArignac <https://github.com/dArignac>`__)
- Django 1.9 support `#80 <https://github.com/ponyriders/django-amazon-price-monitor/pull/80>`__ (`dArignac <https://github.com/dArignac>`__)

`0.4 <https://pypi.python.org/pypi/django-amazon-price-monitor/0.4>`__
----------------------------------------------------------------------
**Features:**

- Deprecate old frontend `#73 <https://github.com/ponyriders/django-amazon-price-monitor/issues/73>`__
- Make angular the default frontend `#70 <https://github.com/ponyriders/django-amazon-price-monitor/issues/70>`__

**Bugfixes:**

- Products with the same price over graph timespae have an empty graph `#67 <https://github.com/ponyriders/django-amazon-price-monitor/issues/67>`__
- Notification of music albums `#33 <https://github.com/ponyriders/django-amazon-price-monitor/issues/33>`__
- Add artist for audio products `#71 <https://github.com/ponyriders/django-amazon-price-monitor/pull/71>`__

**Pull requests:**

- Remove old frontend `#74 <https://github.com/ponyriders/django-amazon-price-monitor/pull/74>`__ (`dArignac <https://github.com/dArignac>`__)
- Fix for empty graphs is packaged now #67 `#72 <https://github.com/ponyriders/django-amazon-price-monitor/pull/72>`__ (`mmrose <https://github.com/mmrose>`__)

`0.3b2 <https://pypi.python.org/pypi/django-amazon-price-monitor/0.3b2>`__
--------------------------------------------------------------------------
**Features:**

- Prepare for automatic releases `#68 <https://github.com/ponyriders/django-amazon-price-monitor/issues/68>`__
- Increase performance of Amazon calls `#41 <https://github.com/ponyriders/django-amazon-price-monitor/issues/41>`__
- Django 1.8 compatibility `#32 <https://github.com/ponyriders/django-amazon-price-monitor/issues/32>`__
- Data reduction and clean up `#27 <https://github.com/ponyriders/django-amazon-price-monitor/issues/27>`__
- Limit graphs `#26 <https://github.com/ponyriders/django-amazon-price-monitor/issues/26>`__
- Show highest and lowest price ever `#25 <https://github.com/ponyriders/django-amazon-price-monitor/issues/25>`__
- Implement a full-usable frontend`#8 <https://github.com/ponyriders/django-amazon-price-monitor/issues/8>`__
- Add more tests `#2 <https://github.com/ponyriders/django-amazon-price-monitor/issues/2>`__

**Bugfixes:**

- Graphs empty for some products `#65 <https://github.com/ponyriders/django-amazon-price-monitor/issues/65>`__
- Don't show other peoples price limits `#63 <https://github.com/ponyriders/django-amazon-price-monitor/issues/63>`__
- Graphs do not render correct values `#60 <https://github.com/ponyriders/django-amazon-price-monitor/issues/60>`__
- 'NoneType' object has no attribute 'url' `#59 <https://github.com/ponyriders/django-amazon-price-monitor/issues/59>`__
- Rename SynchronizeSingleProductTask `#56 <https://github.com/ponyriders/django-amazon-price-monitor/issues/56>`__
- Sync on product creation not working `#55 <https://github.com/ponyriders/django-amazon-price-monitor/issues/55>`__
- Clear old products and prices `#47 <https://github.com/ponyriders/django-amazon-price-monitor/issues/47>`__
- Deleting a product subscription does not remove it from list view `#42 <https://github.com/ponyriders/django-amazon-price-monitor/issues/42>`__
- Endless synchronization queue `#38 <https://github.com/ponyriders/django-amazon-price-monitor/issues/38>`__
- Mark unavailable products `#14 <https://github.com/ponyriders/django-amazon-price-monitor/issues/14>`__

**Closed issues:**

- Unpin beautifulsoup4==4.3.2 `#50 <https://github.com/ponyriders/django-amazon-price-monitor/issues/50>`__

**Pull requests:**

- fixed access of unavilable image urls #59 `#66 <https://github.com/ponyriders/django-amazon-price-monitor/pull/66>`__ (`dArignac <https://github.com/dArignac>`__)
- 63 subscriptions of other users `#64 <https://github.com/ponyriders/django-amazon-price-monitor/pull/64>`__ (`mmrose <https://github.com/mmrose>`__)
- Mark unavailable products `#62 <https://github.com/ponyriders/django-amazon-price-monitor/pull/62>`__ (`mmrose <https://github.com/mmrose>`__)
- Sync on product creation not working `#58 <https://github.com/ponyriders/django-amazon-price-monitor/pull/58>`__ (`dArignac <https://github.com/dArignac>`__)
- Products are now requeried after deletion in list view #42 `#54 <https://github.com/ponyriders/django-amazon-price-monitor/pull/54>`__ (`mmrose <https://github.com/mmrose>`__)
- Show highest and lowest price (#25) `#53 <https://github.com/ponyriders/django-amazon-price-monitor/pull/53>`__ (`mmrose <https://github.com/mmrose>`__)
- Now the new FKs are also set during sync #25 `#52 <https://github.com/ponyriders/django-amazon-price-monitor/pull/52>`__ (`mmrose <https://github.com/mmrose>`__)
- Adding datamigration for new min, max and current price FKs #25 `#51 <https://github.com/ponyriders/django-amazon-price-monitor/pull/51>`__ (`mmrose <https://github.com/mmrose>`__)
- Performance improvements on product API view `#49 <https://github.com/ponyriders/django-amazon-price-monitor/pull/49>`__ (`mmrose <https://github.com/mmrose>`__)
- Remove unused data`#48 <https://github.com/ponyriders/django-amazon-price-monitor/pull/48>`__ (`dArignac <https://github.com/dArignac>`__)
- Amazon query performance increase `#46 <https://github.com/ponyriders/django-amazon-price-monitor/pull/46>`__ (`dArignac <https://github.com/dArignac>`__)
- Django 1.8 compatibility `#45 <https://github.com/ponyriders/django-amazon-price-monitor/pull/45>`__ (`dArignac <https://github.com/dArignac>`__)
- Bugfix: Endless queue `#40 <https://github.com/ponyriders/django-amazon-price-monitor/pull/40>`__ (`dArignac <https://github.com/dArignac>`__)
- waffle.io Badge `#37 <https://github.com/ponyriders/django-amazon-price-monitor/pull/37>`__ (`waffle-iron <https://github.com/waffle-iron>`__)

Pre-Releases
------------
- unfortunately everything before was not packaged and released nor tracked.