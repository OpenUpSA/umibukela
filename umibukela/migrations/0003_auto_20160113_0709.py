# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0002_auto_20160112_1427'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partner',
            name='id',
        ),
        migrations.AddField(
            model_name='partner',
            name='slug',
            field=models.CharField(default='fail', max_length=200, serialize=False, primary_key=True),
            preserve_default=False,
        ),
    ]
