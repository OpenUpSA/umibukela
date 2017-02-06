# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0027_auto_20170203_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycle',
            name='materials',
            field=models.FileField(null=True, upload_to=b'', blank=True),
        ),
    ]
