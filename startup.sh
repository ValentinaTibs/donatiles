export DJANGO_SETTINGS_MODULE=gettingstarted.local_settings
rm db.sqlite3
python3 manage.py migrate
heroku run python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.permission --indent 2 > data.json
python3 manage.py loaddata data.json
