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

# Configure and enable mod_wsgi with apache2

echo "LoadModule wsgi_module /usr/lib/apache2/modules/mod_wsgi.so" > /etc/apache2/mods-available/mod_wsgi.load

a2enmod mod_wsgi
