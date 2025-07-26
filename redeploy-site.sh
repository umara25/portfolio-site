#!/bin/bash

cd ~/portfolio-site

git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml dow

docker compose -f docker-compose.prod.yml up -d --build