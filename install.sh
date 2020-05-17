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

# Ensure we have an up to date package index.

rm -rf /var/lib/apt/lists/*

apt-get update

# Validate that package version details are set in the Dockerfile.

test ! -z "$APACHE_VERSION" || exit 1
test ! -z "$MOD_WSGI_VERSION" || exit 1

# Install apache2 and all the dependencies that we need in order to be able to build
# mod_wsgi from source code

apt-get install -y apache2=$APACHE_VERSION apache2-dev=$APACHE_VERSION locales mariadb-client \
    curl --no-install-recommends

# Clean up the package index.

rm -r /var/lib/apt/lists/*
