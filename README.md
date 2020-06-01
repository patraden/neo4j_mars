# mod_wsgi_docker

configurations for my custom apache2 container supporting multiple python web apps

```
>export CERTIFICATE_PASSWORD=<PASSWORD> # password
>export CERTIFICATE_NAME=<PFX_FILE_NAME> # applications.testservice.mars
>export CONTAINER_IMAGE_NAME=<NAME> # mod_wsgi_ssl_image
>export CONTAINER_NAME=<NAME> # MOD_WSGI_SSL
>export BASIC_USER=<ADMIN_USER_NAME> # automation_user
>export BASIC_USER_PASSWORD=<ADMIN_USER_PASSWORD> # password
>docker build --build-arg CERTIFICATE_PASSWORD --build-arg CERTIFICATE_NAME --build-arg·BASIC_USER --build-arg·BASIC_USER_PASSWORD -t $CONTAINER_IMAGE_NAME -f ./MOD_WSGI_SSL.Dockerfile .
>docker run -tid -p 443:443 -v ~/mod_wsgi_docker:/app --name $CONTAINER_NAME $CONTAINER_IMAGE_NAME
```
