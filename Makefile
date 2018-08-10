help:
	@echo "docker-build-base: - builds the base docker image (not necessary normally as image is on docker hub)"
	@echo "docker-build-web:  - builds the web docker image"

docker-build-base:
	docker build -t pricemonitor/base docker/base/

docker-build-web:
	cp setup.py docker/web/django-amazon-price-monitor/setup.py
	sed -i 's/readme = .*/readme = ""/g' docker/web/django-amazon-price-monitor/setup.py
	sed -i 's/history = .*/history = ""/g' docker/web/django-amazon-price-monitor/setup.py
	docker build -t pricemonitor/web docker/web/

