#!/bin/bash

docker run --name postgrestest -e POSTGRES_PASSWORD=postgresmaster -e POSTGRES_USER=testuser -p 5432:5432 -d postgres:16
docker run --name pgadmintest -e PGADMIN_DEFAULT_EMAIL=teekzaur@gmail.com -e PGADMIN_DEFAULT_PASSWORD=postgresmaster -p 82:80 -d dpage/pgadmin4