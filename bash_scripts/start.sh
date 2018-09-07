#!/bin/bash

gunicorn -c local.py.ini start:application --reload