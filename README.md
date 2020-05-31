# mod_wsgi_docker
configurations for my custom apache2 container supporting multiple python web apps

```
>EXPORT CERTIFICATE_PASSWORD=<PASSWORD>
>EXPORT CONTAINER_IMAGE_NAME=<NAME>
>EXPORT CONTAINER_NAME=<NAME>
>docker build --build-arg CERTIFICATE_PASSWORD -t $CONTAINER_IMAGE_NAME -f ./MOD_WSGI.Dockerfile .
>docker run -tid -p 443:443 -v ~/mod_wsgi_docker:/app --name $CONTAINER_NAME $CONTAINER_IMAGE_NAME
```
