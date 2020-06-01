#!/usr/bin/env bash

# Record everything that is run from this script so appears in logs.

set -x

# Ensure that any failure within this script causes this script to fail
# immediately. This eliminates the need to check individual statuses for
# anything which is run and prematurely exit. Note that the feature of
# bash to exit in this way isn't foolproof. Ensure that you heed any
# advice in:
#
#   http://mywiki.wooledge.org/BashFAQ/105
#   http://fvue.nl/wiki/Bash:_Error_handling
#
# and use best practices to ensure that failures are always detected.
# Any user supplied scripts should also use this failure mode.

set -eo pipefail

# Generating and setting private and public keys from Mars AD *.psx CA certificate file.
# Password for .psx file should be provided as argument to docker build: --build-arg CERRTIFICATE_PASSWORD='password'
# Finally modifying permissions for resulting certificate files to be accessible to root only

openssl pkcs12 -in /tmp/$CERTIFICATE_NAME.pfx -nocerts -nodes -out /tmp/tmp.key -passin pass:$CERTIFICATE_PASSWORD
openssl rsa -in /tmp/tmp.key -out /etc/ssl/private/$CERTIFICATE_NAME.key #removs password from private key
openssl pkcs12 -in /tmp/$CERTIFICATE_NAME.pfx -clcerts -nokeys -out /etc/ssl/certs/$CERTIFICATE_NAME.crt -passin pass:$CERTIFICATE_PASSWORD

chmod 0600 /etc/ssl/certs/$CERTIFICATE_NAME.crt
chmod 0600 /etc/ssl/private/$CERTIFICATE_NAME.key

# Configure and enable mod_wsgi and ssl with apache2

a2enmod ssl

# Disable default virtual hosts configurations and enabling only relevant configurations

cd /etc/apache2/sites-enabled/
a2dissite *

cd /etc/apache2/sites-available/
find . -type f -and -name "*.apps.wsgi.conf" -exec a2ensite {} \;

# Clean up the temporary files

rm -r /tmp/*
