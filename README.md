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
python manage.py runserver
```

Deploying Changes
-----------------

Umibukela runs on dokku, a Heroku-like environment. To deploy changes, just push to dokku: ``git push dokku``.

A new production deployment
---------------------------

Umibukela runs on dokku, a Heroku-like environment. 

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
                  NEW_RELIC_LICENSE_KEY=new relic license key
git push heroku master
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

License
-------

MIT License
