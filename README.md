UmiBukela
=========

This is [Black Sash's](http://www.blacksash.org.za/) Community Based Monitoring (CBM) advocacy and reporting platform, built by Code for South Africa.

Local Development
-----------------

1. Clone the repo
2. Setup a virtualenv: `virtualenv --no-site-packages env; source env/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Setup the database:

```
python manage.py migrate
python manage.py createsuperuser
```

5. Run a local server
```
python manage.py runserver
```

6. If you need to run background tasks, run the following. Remember that unlike `runserver`, `process_tasks` won't reload on code changes so you have to restart this process.

```
python manage.py process_tasks
```

Deploying Changes
-----------------

Umibukela runs on dokku, a Heroku-like environment. To deploy changes, just push to dokku: ``git push dokku``.

A new production deployment
---------------------------

Umibukela runs on dokku, a Heroku-like environment, or Heroku itself.

You will need:

* a django secret key
* a New Relic license key
* a cool app name

```bash
heroku create
heroku addons:add heroku-postgresql
heroku config:set DJANGO_DEBUG=false \
                  DISABLE_COLLECTSTATIC=1 \
                  DJANGO_SECRET_KEY=some-secret-key \
                  NEW_RELIC_APP_NAME=cool app name \
                  NEW_RELIC_LICENSE_KEY=new relic license key \
                  HEALTHE_KOBO_USERNAME=...\
                  HEALTHE_KOBO_PASSWORD=...\
                  KOBO_CLIENT_ID=...\
                  KOBO_CLIENT_SECRET=...
git push heroku master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

Background Tasks in production
------------------------------

We currently only run `manage.py process_tasks` to execute background tasks as needed. They won't execute unless this is running but nothing keeps it running automatically as it's not a priority yet.

```
dokku run umibukela python manage.py process_tasks
```

License
-------

MIT License
