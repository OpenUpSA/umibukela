# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0006_auto_20160126_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='cycle_result_set',
            field=models.ForeignKey(blank=True, to='umibukela.CycleResultSet', null=True),
        ),
    ]
