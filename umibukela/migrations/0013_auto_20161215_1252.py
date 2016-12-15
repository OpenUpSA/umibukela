# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import jsonfield.fields
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0012_auto_20161215_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveysource',
            name='cache_date',
            field=models.DateField(default=datetime.datetime(2016, 12, 15, 12, 52, 35, 906317, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveysource',
            name='cached_form',
            field=jsonfield.fields.JSONField(default=dict),
        ),
    ]
