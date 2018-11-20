# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0055_programmeimage_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='summary',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
