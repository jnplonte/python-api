# PYTHON API
[![license](https://img.shields.io/github/license/mashape/apistatus.svg)]()

## Version
**v1.0.0**


## Dependencies
* python: [https://www.python.org/](https://www.python.org/)
* mongodb: [https://www.mongodb.com/](https://www.mongodb.com/)
* falconframework: [https://falconframework.org/](https://falconframework.org/)
* pip: [https://pypi.python.org/pypi/pip](https://pypi.python.org/pypi/pip)


## Installation
- create virtualenv `virtualenv -p python3 api-env`
- work on virtualenv `source api-env/bin/activate`
- install python dependencies by running `pip install -r requirements.txt`
- create database and update database settings on `{root}\app\config.py`


## How to Use
- run `./bash_scripts/start.sh` it will listen to default http://localhost:8686


## Documentation
- run `./bash_scripts/docs.sh`


## Testing
- run `nosetests -v`


## Building Development
- run `./bash_scripts/startDaemon.sh dev`


## Building Production
- run `./bash_scripts/startDaemon.sh prod`
