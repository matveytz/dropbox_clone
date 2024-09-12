#!/bin/bash

# Compose DOWN APP
echo "Compose DOWN APP"
docker rm app_dropbox_clone 

# Compose BUILD
echo "Compose BUILD"
docker compose build

# Compose UP
echo "Compose UP"
docker compose up
