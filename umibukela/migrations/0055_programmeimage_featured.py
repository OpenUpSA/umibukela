# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0054_programme_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmeimage',
            name='featured',
            field=models.BooleanField(default=False),
        ),
    ]
