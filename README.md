# mod_wsgi_docker

configurations for my custom apache2 container supporting multiple python web apps

```bash
export CERTIFICATE_PASSWORD=<PASSWORD> # password
export CERTIFICATE_NAME=<PFX_FILE_NAME> # applications.testservice.mars
export BASIC_USER=<ADMIN_USER_NAME> # automation_user
export BASIC_USER_PASSWORD=<ADMIN_USER_PASSWORD> # password
export MYSQL_ROOT_PASSWORD=<MYSQL_ROOT_PASSWORD> # password
docker-compose up -d
```

Temporary notes:
```bash
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
## Snow data analytics

```sql
select sys_class_name,count(number) as count, count(case when automation_flag='M' then number end) as M, count(case when automation_flag='A' then number end) as A from tasks group by sys_class_name order by count desc;

select sys_class_name,assignment_group,count(number) as count, count(case when automation_flag='M' then number end) as M, count(case when automation_flag='A' then number end) as A from tasks where sys_class_name='Change task' group by sys_class_name,assignment_group order by count desc limit 10;
```
