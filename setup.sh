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

# Ensure that default language locale is set to a sane default of UTF-8.

echo 'en_US.UTF-8 UTF-8' >> /etc/locale.gen
locale-gen
LANG=en_US.UTF-8

# Set the umask to be '002' so that any files/directories created from
# this point are group writable. This does rely on any applications or
# installation scripts honouring the umask setting, which unfortunately
# not all do.

# Create a special user account under which any application should be
# run. This has group of 'root' with gid of '0' as it appears to be
# safest bet to allow file system permisions for everything to work.

adduser --disabled-password --gecos "wsgi-user" --uid 1000 --gid 0 \
   --home /home/wsgi wsgi-user

# Set the umask to be '002' so that any files/directories created from
# this point are group writable. This does rely on any applications or
# installation scripts honouring the umask setting, which unfortunately
# not all do.

umask 002

# Set up the directory where Python and Apache installations will be put.

INSTALL_ROOT=/usr/local
export INSTALL_ROOT

BUILD_ROOT=/tmp/build
export BUILD_ROOT

mkdir -p $INSTALL_ROOT
mkdir -p $BUILD_ROOT

# Download source code for packages and unpack them.

curl -SL -o $BUILD_ROOT/mod_wsgi.tar.gz https://github.com/GrahamDumpleton/mod_wsgi/archive/$MOD_WSGI_VERSION.tar.gz

mkdir $BUILD_ROOT/mod_wsgi

tar -xC $BUILD_ROOT/mod_wsgi --strip-components=1 -f $BUILD_ROOT/mod_wsgi.tar.gz

# Build mod_wsgi from source code.

cd $BUILD_ROOT/mod_wsgi

./configure
make
make install
make clean

# Installing python virtualenv

python3 -m pip install --upgrade pip
python3 -m pip install --no-cache-dir virtualenv

# Because the recommendation is that the derived Docker image should run
# as a non root user, we enable the ability for Apache 'httpd'  when run
# as a non root user to bind privileged ports normally used by system
# services. This allows it to use port 80 and 443 as would normally be
# used for HTTP/HTTPS. Allowing use of 80/443 can avoid problems with
# some web applications that don't calculate properly what the web
# services public port is and instead wrongly use the ports that the
# Docker container exposes it as, which can be something different when
# a front end proxy or router is used.

setcap 'cap_net_bind_service=+ep' /usr/sbin/apache2

# Ensure home directory for 'whiskey' user is world writable but also
# has the sticky bit so only 'root' or the owner can unlink any files.
# Needs to be world writable as we cannot be certain what uid the
# application will run as.

chmod 1777 /home/wsgi

# Create empty directory to be used as application directory. Ensure it
# is world writable but also has the sticky bit so only root or the
# owner can unlink any files. Needs to be world writable as we cannot be
# certain what uid application will run as.

mkdir -p /app
chmod 1777 /app

# Create empty directory to be used as the data directory. Ensure it is
# world writable but also has the sticky bit so only root or the owner
# can unlink any files. Needs to be world writable as we cannot be
# certain what uid application will run as.

mkdir -p /data
chmod 1777 /data

# Generating and setting private and public keys from Mars AD *.psx CA certificate file.
# Password for .psx file should be provided as argument to docker build: --build-arg CERRTIFICATE_PASSWORD='password'
# Finally modifying permissions for resulting certificate files to be accessible to root only

openssl pkcs12 -in /tmp/$CERTIFICATE_NAME.pfx -nocerts -nodes -out /tmp/tmp.key -passin pass:$CERTIFICATE_PASSWORD
openssl rsa -in /tmp/tmp.key -out /etc/ssl/private/$CERTIFICATE_NAME.key #removs password from private key
openssl pkcs12 -in /tmp/$CERTIFICATE_NAME.pfx -clcerts -nokeys -out /etc/ssl/certs/$CERTIFICATE_NAME.crt -passin pass:$CERTIFICATE_PASSWORD

chmod 0600 /etc/ssl/certs/$CERTIFICATE_NAME.crt
chmod 0600 /etc/ssl/private/$CERTIFICATE_NAME.key

# Configure and enable mod_wsgi and ssl with apache2

echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so" > /etc/apache2/mods-available/mod_wsgi.load
a2enmod mod_wsgi
a2enmod ssl

# Setting admin user for basic authentication to applications

htpasswd -bc /etc/apache2/.htpasswd $BASIC_USER $BASIC_USER_PASSWORD

# Clean up the temporary build area and temporary configuration files

rm -rf $BUILD_ROOT
