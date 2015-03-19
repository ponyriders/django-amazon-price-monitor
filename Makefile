STAGE = TravisCI

test:
	STAGE=$(STAGE) `which django-admin.py` test --settings=price_monitor.test_settings price_monitor
