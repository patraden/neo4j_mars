# docker build --build-args that must be used while building container image
# CERTIFICATE_NAME - full name of certificate file from Mars CA
# CERTIFICATE_PASSWORD - password for Mars CA certificate

FROM python:3.8-slim-buster
ARG CERTIFICATE_PASSWORD
ARG CERTIFICATE_NAME
ARG BASIC_USER
ARG BASIC_USER_PASSWORD
MAINTAINER denis.patrakhin@gmail.com

ENV APACHE_VERSION=2.4.38-3+deb10u3 \
    MOD_WSGI_VERSION=4.7.1

COPY install.sh /usr/local/bin/mod_wsgi-docker-install
RUN /usr/local/bin/mod_wsgi-docker-install

COPY setup.sh /usr/local/bin/mod_wsgi-docker-setup
RUN /usr/local/bin/mod_wsgi-docker-setup

COPY setup_ssl.sh /usr/local/bin/mod_wsgi-docker-setup-ssl
COPY *.apps.wsgi.conf /etc/apache2/sites-available/
COPY ${CERTIFICATE_NAME}.pfx /tmp
RUN /usr/local/bin/mod_wsgi-docker-setup-ssl

ENV MOD_WSGI_USER=wsgi-user MOD_WSGI_GROUP=root

CMD apachectl -D FOREGROUND
WORKDIR /app
