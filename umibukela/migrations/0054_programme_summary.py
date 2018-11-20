# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0053_auto_20181119_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='summary',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
