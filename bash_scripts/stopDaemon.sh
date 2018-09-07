#!/bin/bash

kill -9 `ps aux | grep gunicorn | grep 'ai' | awk '{ print $2 }'` > out.log 2> /dev/null