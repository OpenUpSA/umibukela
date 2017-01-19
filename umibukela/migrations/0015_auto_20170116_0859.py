# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0014_auto_20170116_0845'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveykoboproject',
            name='url',
        ),
        migrations.AddField(
            model_name='surveykoboproject',
            name='form_id',
            field=models.IntegerField(default=1337, unique=True),
            preserve_default=False,
        ),
    ]
