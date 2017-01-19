# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('umibukela', '0016_auto_20170116_1216'),
    ]

    operations = [
        migrations.CreateModel(
            name='KoboRefreshToken',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('token', models.TextField()),
            ],
        ),
    ]
