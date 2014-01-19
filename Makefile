testenv:
    pip install -e .
    pip install -r requirements_tests.txt

test:
    flake8 price_monitor --ignore=E501,E128 --exclude=migrations
    coverage run --branch --source=price_monitor `which django-admin.py` test --settings=price_monitor.test_settings price_monitor
    coverage report --omit=price_monitor/migrations/*

.PHONY: test