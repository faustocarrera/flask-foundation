#!/bin/bash

ACTION=$1
APPNAME="appname"
VIRTUALENVDIR="./env"

if [ -z "$ACTION" ]; then
    echo "===================================================================="
    echo "Usage            : /bin/bash $0 [option]"
    echo -e "\033[1mOptions\033[0m"
    echo "env              : create a development environment using virtualenv"
    echo "requirements     : install requirements"
    echo "clean            : remove unwanted files like .pyc's"
    echo "lint             : check style with flake8"
    echo "tests            : run tests using nose"
    echo "run              : run application"
    echo "===================================================================="
    exit 0
fi

# virutalenv
if [ "$ACTION" == "env" ]; then
    echo "Generating virtual environment."
    if [ ! -d "$VIRTUALENVDIR" ]; then
        virtualenv env -p python2.7
    else
        echo "Virtualenv already present."
    fi
fi

# check if we have a virtualenv
if [ ! -d "$VIRTUALENVDIR" ]; then
    echo "You have to create a virtualenv"
    echo "/bin/bash $0 env"
    exit 1
fi

# install dependencies
if [ "$ACTION" == "requirements" ]; then
    echo "Installing required libraries"
    ./env/bin/pip install -r requirements.txt
fi

# clean
if [ "$ACTION" == "clean" ]; then
	./env/bin/python manage.py clean
fi

# lint
if [ "$ACTION" == "lint" ]; then
	flake8 --exclude=env .
fi

# test
if [ "$ACTION" == "test" ] || [ "$ACTION" == "tests" ]; then
    env/bin/nosetests --with-coverage --cover-erase --cover-package="$APPNAME" --tests=tests/
fi

# test
if [ "$ACTION" == "run" ]; then
	export APPNAME_ENV=dev
	export FLASK_DEBUG=1
	./env/bin/python manage.py server
fi