# basic setup
FROM philcryer/min-jessie
MAINTAINER Alexander Herrmann <darignac@gmail.com>

# install basic packages: lxml dependencies, python3 and git
# see recommendation https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#apt-get
RUN apt-get update && apt-get install -y \
    git \
    libffi-dev \
    libjpeg-dev \
    libpq-dev \
    libxml2-dev \
    libxslt1-dev \
    postgresql-client-9.4 \
    python3-cairo \
    python3-minimal \
    python3-pip \
&& rm -rf /tmp/* /var/tmp/* \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

# install lxml and psycopg2 - they take the most amount of time compiling
RUN pip3 install lxml psycopg2 setuptools