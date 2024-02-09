# Flask on Docker

## Overview
This repository provides Docker setup for deploying a Flask application with Postgres for both development and production environments. The repository has a configuration of Flask to run on Docker, integration with Postgres, and the addition of Nginx and Gunicorn for production deployment. The setup includes handling static and media files, making it a robust solution for containerized Flask applications.

Here is a short animated gif of uploading a file at http://localhost:1121/uploads:

![Animated GIF](ezgif-8-42fefedb1c.gif)

## Build Instructions

Here is how to get Flask on Docker up and running from the root directory.

### Development

1. Build the image and run the containers.
```
$ docker-compose up -d --build
```
2. Create the table.
```
$ docker-compose exec web python manage.py create_db
```
3. Test out to see whether the webpage is working.
```
$ curl http://localhost:1121
```
You should receive output similar to
```
{
  "hello": "world"
}
```
4. When done, be sure to bring down the development containers (an    d the associated volumes with the `-v` flag):
```
$ docker-compose down -v
```

## Production

1. Build the image and run the containers.
```
$ docker-compose -f docker-compose.prod.yml up -d --build
```
2. Create the table.
```
$ docker-compose -f docker-compose.prod.yml exec web python manage.py create_db
```
3. Test out to see whether the webpage is working.
```
$ curl http://localhost:1121
```
You should receive output similar to
```
{"hello": "world"}
```
4. When done, be sure to bring down the development containers (an    d the associated volumes with the `-v` flag):
```
$ docker-compose down -v
```
When you run the above command, you will likely get an error similar to below.
```
ERROR: error while removing network: network flask-on-docker_default id bd73326ef19618410267332030f0e06f130c236acfb48a593121001015602d17 has active endpoints
```
This means that you will have to run `docker ps` to determine which containers are still running. You should get output similar to below:
```
$ docker ps
CONTAINER ID   IMAGE                   COMMAND                  CREATED          STATUS          PORTS                                   NAMES
6b2daeb5a992   flask-on-docker_nginx   "/docker-entrypoint.…"   59 seconds ago   Up 58 seconds   0.0.0.0:1121->80/tcp, :::1121->80/tcp   flask-on-docker_nginx_1
```
At this point, you will want to run the following command with the container ID to stop and remove the active container.
```
$ docker stop 6b2daeb5a992; docker rm 6b2daeb5a992
```

