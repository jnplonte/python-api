# PYTHON API
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

## Version
**v1.0.0**

## Dependencies
* python: [https://www.python.org/](https://www.python.org/)
* falconframework: [https://falconframework.org/](https://falconframework.org/)
* mongodb: [https://www.mongodb.com/](https://www.mongodb.com/)


## Installation
* create virtualenv `virtualenv -p python3 api-env`
* work on virtualenv `source api-env/bin/activate`
* install python dependencies by running `pip install -r requirements.txt`
* update the following configurations and database credentials on {root}/dev.py.ini
* generate documentation `./bash_scripts/docs.sh`


## How to Use
* run `./bash_scripts/start.sh` it will listen to http://localhost:8686 with header token


## Testing
* start all test by running `nosetests -v`


## Running Server
* run `./bash_scripts/startDaemon.sh dev`
* run `./bash_scripts/startDaemon.sh prod`
