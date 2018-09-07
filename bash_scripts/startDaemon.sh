#!/bin/bash

NAME=$1
FILENAME=$NAME'.py.ini'

gunicorn -c $FILENAME start:application --name=ai