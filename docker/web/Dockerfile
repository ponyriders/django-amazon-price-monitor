# basic setup, use base image of treasury project
FROM treasury/base:latest
MAINTAINER Alexander Herrmann <darignac@gmail.com>

# system package dependencies
RUN apt-get update && apt-get install -y \
    libffi-dev \
&& rm -rf /tmp/* /var/tmp/* \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# django setup, create default folder and volumes
WORKDIR /srv/
RUN mkdir static
VOLUME ["/srv/media", "/srv/logs", "/srv/pricemonitor", "/srv/project"]

# copy the django project files
COPY project /srv/project

# install python dependencies for the django project
RUN pip3 install -r /srv/project/requirements.pip

# copy the treasury package and install - will be mounted later through data container (and thus overwritten with the host files)
ADD django-amazon-price-monitor /srv/pricemonitor
RUN pip3 install -e /srv/pricemonitor

# ports
EXPOSE 8000

# entrypoint
WORKDIR /srv/project