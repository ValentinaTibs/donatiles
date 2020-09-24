# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/ValentinaTibs/donatiles.git
$ cd donatiles

$ python3 -m venv donatiles
$ pip3 install -r requirements.txt

$ createdb vale

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

### nightly push
```sh
$ git push heroku master
```

### freshly made repo
```sh
$ heroku create
$ git push heroku master
```

```
in case you want to 
$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
_______________________________________________________________________________


# SERVER RUN 

on Windows

```
heroku local web -f Procfile.windows
```

otherwise

```
heroku local web 
```


## Gunicorn let Connecion opened on 5000

```
kill -9 $(lsof -i:5000 -t) 2> /dev/null
```

# DATABASE

## local run 

```
$ brew services start postgresql
$ psql postgres

```

## remote check and deploy of migrations

```
heroku run python manage.py showmigrations
python manage.py migrate --fake taleoftiles zero

```

## Fixin messed up remote databases

heroku restart
heroku pg:reset DATABASE
heroku run python manage.py migrate

## Reset local Migrations

```sh
python3 manage.py makemigrations
python3 manage.py showmigrations
python3 manage.py migrate --fake taleoftiles zero

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete

python3 manage.py showmigrations
python3 manage.py migrate --fake-initial

```

## Download and test remote database

```sh
heroku pg:backups:capture
heroku pg:backups:download
pg_dump vale
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U vale -d vale latest.dump
```

## start a new DB

```sh
pip3 install gunicorn
postgres=# CREATE ROLE vale superuser;
postgres=# ALTER ROLE vale WITH LOGIN;

```


### pg_admin url
http://127.0.0.1:58993/browser/#

# Translations - Microcopy text

```sh

python3 manage.py makemessages 
python3 manage.py compilemessages
heroku restart

```







