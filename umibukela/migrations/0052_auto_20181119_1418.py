# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0051_auto_20181119_1201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmeresources',
            name='document_extension',
            field=models.CharField(max_length=50, null=True, blank=True),
        ),
    ]
