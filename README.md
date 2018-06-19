UmiBukela
=========

This is [Black Sash's](http://www.blacksash.org.za/) Community Based Monitoring (CBM) advocacy and reporting platform, built by Code for South Africa.

Open Data Kit / Kobo Toolbox form compatibility
-------------------------------

For CBM to be able to automatically generate summaries of Kobo Toolbox/ODK forms, the following assumptions are made about the forms, which means forms must comply with these to be supported:

- All multiple-choice questions must be _required_ - any optional questions resulting in blanks in responses will result in errors on the site.
- There must be field named `gender` (lower caps) in a group named `demographics_group`. It's values are allowed to be `male` or `female`. The labels for these fields and values may be different.
- There must be a field named `facility`. Each option in this field will be mapped to a Site in CBM.


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
0 * * * * /usr/local/bin/dokku --rm  run umibukela newrelic-admin run-program python manage.py import_submissions  2>&1 | tee -a /var/log/umibukela/import-submissions.log | grep -i -B10 error
```

If cron mail is set up on the server, it should email us errors.

Background Tasks in production
------------------------------

We currently only run `manage.py process_tasks` to execute background tasks as needed. They won't execute unless this is running but nothing keeps it running automatically as it's not a priority yet.

```
dokku run umibukela python manage.py process_tasks
```

Generating an entity relationship diagram
-----------------------------------------

Install GraphViz, then `pygraphviz` if you haven't already

```
pip install pygraphviz
```

Then use the `graph_models` manage command to generate a diagram

```
python manage.py graph_models umibukela -o umibukela.png
```

License
-------

MIT License
