# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0033_allow_multiple_surveys_per_kobo_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='koboproject',
            name='name',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
