# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0018_auto_20170124_1245'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycleresultset',
            name='monitors',
            field=models.ManyToManyField(to='umibukela.Monitor', blank=True),
        ),
    ]
