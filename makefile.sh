#!/bin/bash

ACTION=$1
APPNAME="appname"
VIRTUALENVDIR="env"

if [ -z "$ACTION" ]; then
    echo "===================================================================="
    echo "Usage            : /bin/bash $0 [option]"
    echo -e "\033[1mOptions\033[0m"
    echo "env              : create a development environment using virtualenv"
    echo "requirements     : install requirements"
    echo "clean            : remove unwanted files like .pyc's"
    echo "lint:flake       : check style with flake8"
    echo "lint:pylint      : check style with pylint"
    echo "tests            : run tests using nose"
    echo "run              : run application"
    echo "===================================================================="
    exit 0
fi

# virutalenv
if [ "$ACTION" == "env" ]; then
    echo "Generating virtual environment."
    if [ ! -d "./$VIRTUALENVDIR" ]; then
        virtualenv $VIRTUALENVDIR -p python2.7
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
    echo "Cleaning"
    find . -name '*.pyc' | xargs rm -f
fi

# lint with flake8
if [ "$ACTION" == "lint:flake" ]; then
    echo "Lint: flake8"
    ./env/bin/flake8 --exclude="$VIRTUALENVDIR" "$APPNAME"
fi

# lint with pylint
if [ "$ACTION" == "lint:pylint" ]; then
    echo "Lint: pylint"
    ./env/bin/pylint "$APPNAME"
fi

# test
if [ "$ACTION" == "test" ] || [ "$ACTION" == "tests" ]; then
    echo "Running tests"
    env/bin/nosetests --with-coverage --cover-erase --cover-package="$APPNAME" --tests=tests/
fi

# test
if [ "$ACTION" == "run" ]; then
    echo "Starting app..."
    export APPNAME_ENV=dev
    export FLASK_DEBUG=1
    ./env/bin/python manage.py server
fi
