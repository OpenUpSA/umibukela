# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0042_auto_20181107_0027'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='slug',
            field=models.SlugField(unique=True, max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='programmestory',
            name='programme',
            field=models.ForeignKey(related_name='programme', to='umibukela.Programme'),
        ),
    ]
