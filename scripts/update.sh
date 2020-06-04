#!/usr/bin/env bash

echo "Updating git repo..."
git pull git@github.com:zakhar-petukhov/DinnerTime.git

echo "Updating images..."
docker-compose pull

cd ..
docker build -f Dockerfile -t korolevich/DinnerTime  .

