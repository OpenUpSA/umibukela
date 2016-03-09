# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0006_auto_20160309_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='site',
            name='telephone',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
