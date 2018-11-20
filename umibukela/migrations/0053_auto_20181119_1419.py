# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0052_auto_20181119_1418'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmeresources',
            name='document_extension',
            field=models.CharField(max_length=150, null=True, blank=True),
        ),
    ]
