# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0043_auto_20181107_0252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmestory',
            name='slug',
            field=models.SlugField(default='slug', max_length=200, blank=True),
            preserve_default=False,
        ),
    ]
