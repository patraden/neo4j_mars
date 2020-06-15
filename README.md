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

Temporary notes:
```
docker exec -ti -u wsgi-user MOD_WSGI_SSL /bin/bash -c 'mysql -h mariadbs -u root -p'
docker exec -ti -u wsgi-user MOD_WSGI_SSL /bin/bash -c 'python3 ./pythonstudy/heap_class.py'
mysql -h 0 -u pi -p
```

```sql
CREATE DATABASE `mydb`;
CREATE USER 'user' IDENTIFIED BY 'password';
GRANT USAGE ON *.* TO 'user'@'%' IDENTIFIED BY 'password';
GRANT ALL privileges ON `mydb`.* TO 'myuser'@'%';
FLUSH PRIVILEGES;
SHOW GRANTS FOR 'pi'@'%';
```
