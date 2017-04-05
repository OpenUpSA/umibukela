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

### Importing Kobo Toolbox responses into CBM automatically

We automatically import survey responses from Kobo for Cycles where Auto-import is enabled. This relies on the Facility option name being specified on each Cycle Result Set in each Survey of that Cycle.

We use a Manage command to actually do the import. In production this is called periodically by a Cron job so to use it in development, run:

```
python manage.py import_submissions
```

or to run it manually in production, run


```
dokku run umibukela python manage.py import_submissions
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
                  KOBO_CLIENT_SECRET=...\
                  BLACKSASH_KOBO_USERNAME=... \
                  BLACKSASH_KOBO_PASSWORD=...

git push heroku master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

Configure a cron job to auto-import survey responses:

```bash
mkdir /var/log/umibukela
sudo chown -R ubuntu: /var/log/umibukela
```

```cron
0 * * * * /usr/local/bin/dokku --rm  run umibukela newrelic-admin run-program python manage.py import_submissions  2>&1 >> /var/log/umibukela/import-submissions.log
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
