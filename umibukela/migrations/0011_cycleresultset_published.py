# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0010_auto_20160530_1512'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycleresultset',
            name='published',
            field=models.BooleanField(default=True, help_text=b"Whether the results may be listed publicly with the assumption that it's somewhat validated"),
            preserve_default=False
        ),
    ]
