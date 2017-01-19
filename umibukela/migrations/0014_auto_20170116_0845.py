# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0013_submission_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 16, 8, 45, 12, 842490, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 16, 8, 45, 19, 20628, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
    ]
