#!/bin/sh
set -e

eval $(minikube docker-env)
docker build -t flask-app:12.0.0 --no-cache ./app
