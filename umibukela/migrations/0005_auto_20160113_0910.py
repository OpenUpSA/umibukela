# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0004_auto_20160113_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='slug',
            field=models.SlugField(max_length=200, serialize=False, primary_key=True),
        ),
    ]
