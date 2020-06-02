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

# Generating virtual host conf file for multiple applications

cat << EOF > /etc/apache2/sites-available/$CERTIFICATE_NAME.wsgi.conf
<VirtualHost *:443>
	# The ServerName directive sets the request scheme, hostname and port that
	# the server uses to identify itself. This is used when creating
	# redirection URLs. In the context of virtual hosts, the ServerName
	# specifies what hostname must appear in the request's Host: header to
	# match this virtual host. For the default virtual host (this file) this
	# value is not decisive as it is used as a last resort host regardless.
	# However, you must set it for any further virtual host explicitly.
	
	ServerName $CERTIFICATE_NAME
	
	SSLEngine on
	SSLCertificateFile /etc/ssl/certs/$CERTIFICATE_NAME.crt
	SSLCertificateKeyFile /etc/ssl/private/$CERTIFICATE_NAME.key
EOF

sed -n '/^[^#]/p' /tmp/apps.list | while IFS=':' read -r FILE DIRECTORY URI
do 
cat << EOF >> /etc/apache2/sites-available/$CERTIFICATE_NAME.wsgi.conf
	WSGIScriptAlias $URI /app/$DIRECTORY/$FILE.wsgi
	<Directory /app/$DIRECTORY>
		AuthType Basic
		AuthName "Restricted Content"
		AuthUserFile /etc/apache2/.htpasswd
		Require valid-user
	</Directory>
EOF
done

cat << EOF >> /etc/apache2/sites-available/$CERTIFICATE_NAME.wsgi.conf
	DocumentRoot /app
	ServerAdmin webmaster@localhost
	# Available loglevels: trace8, ..., trace1, debug, info, notice, warn,
	# error, crit, alert, emerg.
	# It is also possible to configure the loglevel for particular
	# modules, e.g.
	LogLevel info ssl:info
	
	ErrorLog \${APACHE_LOG_DIR}/error.log
	CustomLog \${APACHE_LOG_DIR}/access.log combined
	
	# For most configuration files from conf-available/, which are
	# enabled or disabled at a global level, it is possible to
	# include a line for only one particular virtual host. For example the
	# following line enables the CGI configuration for this host only
	# after it has been globally disabled with "a2disconf".
	#Include conf-available/serve-cgi-bin.conf
</VirtualHost>

# vim: syntax=apache ts=4 sw=4 sts=4 sr noet
EOF
