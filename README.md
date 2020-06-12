# mod_wsgi_docker

configurations for my custom apache2 container supporting multiple python web apps

```
export CERTIFICATE_PASSWORD=<PASSWORD> # password
export CERTIFICATE_NAME=<PFX_FILE_NAME> # applications.testservice.mars
export BASIC_USER=<ADMIN_USER_NAME> # automation_user
export BASIC_USER_PASSWORD=<ADMIN_USER_PASSWORD> # password
export MYSQL_ROOT_PASSWORD=<MYSQL_ROOT_PASSWORD> # password
docker-compose up -d
```
