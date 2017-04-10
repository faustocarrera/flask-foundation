#!/bin/bash

ACTION=$1

if [ -z "$ACTION" ]; then
    echo "===================================================================="
    echo "Usage            : /bin/bash $0 [option]"
    echo -e "\033[1mOptions\033[0m"
    echo "env              : create a development environment using virtualenv"
    echo "dependencies     : install requirements"
    echo "clean            : remove unwanted files like .pyc's"
    echo "lint             : check style with flake8"
    echo "test             : run tests using nose"
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

# install dependencies
if [ "$ACTION" == "dependencies" ]; then
    echo "Installing required libraries"
    ./env/bin/pip install -r requirements
fi

# clean
if [ "$ACTION" == "delete" ]; then
	./env/bin/python manage.py clean
fi

# lint
if [ "$ACTION" == "lint" ]; then
	flake8 --exclude=env .
fi

# test
if [ "$ACTION" == "test" ]; then
	nosetests --verbose
fi

# test
if [ "$ACTION" == "run" ]; then
	export APPNAME_ENV=dev
	export FLASK_DEBUG=1
	./env/bin/python manage.py server
fi