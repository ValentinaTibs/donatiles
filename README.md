# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/heroku/python-getting-started.git
$ cd python-getting-started

$ python3 -m venv getting-started
$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku
###nightly push
```sh
$ git push heroku master
```


###freshly made repo
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

```
heroku local web -f Procfile.windows
```

or 

```
heroku local web 
```



##3 Gunicorn let Connecion opened on 5000

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
pg_restore --verbose --clean --no-acl --no-owner -h localhost -U vale -d vale latest.dump
```

# Translations - Microcopy text

```sh

python3 manage.py makemessages -l 'en'
python3 manage.py compilemessages
RESTART SERVER and dynos

heroku run python manage.py compilemessages

```




