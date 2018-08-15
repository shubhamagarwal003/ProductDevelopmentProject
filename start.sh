#!/bin/bash

# Start Gunicorn processes
echo Starting Gunicorn.
cd /home/docker/code
npm install
rollup -c
nohup gunicorn risk_management.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 &

service nginx start