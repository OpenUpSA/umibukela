# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0060_auto_20181126_0852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='description',
            field=models.TextField(help_text=b'Field is markdown supported'),
        ),
        migrations.AlterField(
            model_name='programme',
            name='summary',
            field=models.TextField(help_text=b'Field is not supported by markdown', null=True),
        ),
    ]
