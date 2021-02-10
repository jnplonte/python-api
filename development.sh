#!/bin/bash

git reset --hard HEAD
git pull origin development

docker-compose stop
docker-compose start
