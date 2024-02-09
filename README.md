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
