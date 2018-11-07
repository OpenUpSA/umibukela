# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0039_programmeimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmeimage',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='programmestoryimage',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
