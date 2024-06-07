#!/bin/bash

# Apply database migrations
status=1
while [ $status != 0 ]; do
    echo "Try apply database migrations"
    python3 src/manage.py migrate
    status=$?
    sleep 0.1
done

# Start server
echo "Starting server"
python3 src/manage.py runserver 0.0.0.0:8000