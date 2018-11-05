# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0035_auto_20181016_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='funder',
            name='logo',
            field=models.FileField(null=True, upload_to=b'funder/logo/'),
        ),
        migrations.AddField(
            model_name='funder',
            name='website',
            field=models.URLField(null=True),
        ),
    ]
