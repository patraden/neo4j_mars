FROM python:3.8-slim-buster
ARG CERTIFICATE_PASSWORD
MAINTAINER denis.patrakhin@gmail.com
ENV APACHE_VERSION=2.4.38-3+deb10u3 \
    MOD_WSGI_VERSION=4.7.1 \
    CERTIFICATE_NAME=applications.testservice.mars

COPY install.sh /usr/local/bin/mod_wsgi-docker-install
RUN /usr/local/bin/mod_wsgi-docker-install

COPY setup.sh /usr/local/bin/mod_wsgi-docker-setup
RUN /usr/local/bin/mod_wsgi-docker-setup

COPY setup_ssl.sh /usr/local/bin/mod_wsgi-docker-setup-ssl
COPY *.apps.wsgi.conf /etc/apache2/sites-available/
COPY *.pfx /tmp
RUN /usr/local/bin/mod_wsgi-docker-setup-ssl

ENV MOD_WSGI_USER=wsgi-user MOD_WSGI_GROUP=root

CMD apachectl -D FOREGROUND
WORKDIR /app
