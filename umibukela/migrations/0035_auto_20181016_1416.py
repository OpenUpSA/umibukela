# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0034_auto_20181016_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='slug',
            field=models.SlugField(unique=True, max_length=200),
        ),
    ]
