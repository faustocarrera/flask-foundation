Flask Foundation
================

The source and documentation is located at are located at [https://jackstouffer.github.io/Flask-Foundation/](https://jackstouffer.github.io/Flask-Foundation/)

## About

Flask Foundation is a solid foundation for flask applications, built with best practices, that you can easily construct your website/webapp off of. Flask Foundation is different from most Flask frameworks as it does not assume anything about your development or production environments. Flask Foundation is platform agnostic in this respect.

## Links

* [The Flask Mega-Tutorial](https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world)
* [How I structure my Flask applications](http://mattupstate.com/blog/how-i-structure-my-flask-applications/)
* [Creating Websites With Flask](http://maximebf.com/blog/2012/10/building-websites-in-python-with-flask/)
* [Getting Bigger With Flask](http://maximebf.com/blog/2012/11/getting-bigger-with-flask/)
* [Larger Applications With Flask](http://flask.pocoo.org/docs/patterns/packages/)


## Books

* [Mastering flask](https://www.packtpub.com/web-development/mastering-flask)
* [Flask web development](http://shop.oreilly.com/product/0636920031116.do?cmp=af-webplatform-books-videos-product_cj_9781449372620_%25zp)

## Install

```
sudo apt-get install libmariadbclient-dev
sudo apt-get install python-dev
sudo apt-get isntall libssl-dev
```

## Make file

```
====================================================================
Usage            : /bin/bash ./makefile.sh [option]
Options
env              : create a development environment using virtualenv
requirements     : install requirements
clean            : remove unwanted files like .pyc's
lint             : check style with flake8
test             : run tests using nose
run              : run application
====================================================================
```

## Migrations

* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Alembic](http://alembic.zzzcomputing.com/en/latest/index.html)

```
# help
$ python manage.py db --help
# init migrations repository
$ python manage.py db init
# autogenerate first migration
$ python manage.py db migrate -m 'init migration'
# generate migration script
$ python manage.py db revision -m 'create user table'
# apply migrations
$ python manage.py migrate
```

## Todo

* ~~update makefile~~
* update nose tests
* ~~create sqlalchemy migrations documentation~~