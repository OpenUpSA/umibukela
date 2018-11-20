# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0056_auto_20181120_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='summary',
            field=models.TextField(null=True),
        ),
    ]
