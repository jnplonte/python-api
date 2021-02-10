#!/bin/bash

git reset --hard HEAD
git pull origin master

docker-compose stop
docker-compose start
