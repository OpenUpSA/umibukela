# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0019_auto_20170124_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycleresultset',
            name='monitors',
            field=models.ManyToManyField(help_text=b"Only monitors for the current partner are shown. If you update the Partner you'll have to save and edit this Cycle Result Set again to see the available monitors.", to='umibukela.Monitor', blank=True),
        ),
    ]
