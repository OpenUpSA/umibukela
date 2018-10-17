# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0032_auto_20180511_1315'),
    ]

    operations = [
        migrations.AddField(
            model_name='programme',
            name='slug',
            field=models.SlugField(max_length=200, unique=True, null=True),
        ),
    ]
