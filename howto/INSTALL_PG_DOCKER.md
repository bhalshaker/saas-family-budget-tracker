# How to run PostgreSQL in a Docker Container on your machine

* Make sure that you have internet connection available on your local machine.
* Make sure that docker engine is installed on your local machine.

Download docker image
```sh
docker pull postgres
```

Create and run docker container change postgresql password with your password
```sh
docker run -d --name mypostgres -p 5432:5432 -e POSTGRES_PASSWORD=postgres postgres
```

## How to access psql inside the postgresql container

Assuming that the name of the running container is mypostgres
```sh
docker exec -it mypostgres psql -h localhost -U postgres
```