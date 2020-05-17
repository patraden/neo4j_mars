FROM python:3.8-slim-buster
MAINTAINER denis.patrakhin@gmail.com
ENV APACHE_VERSION=2.4.38-3+deb10u3 \
    MOD_WSGI_VERSION=4.7.1
COPY install.sh /usr/local/bin/mod_wsgi-docker-install
RUN /usr/local/bin/mod_wsgi-docker-install
COPY setup.sh /usr/local/bin/mod_wsgi-docker-setup
RUN /usr/local/bin/mod_wsgi-docker-setup
