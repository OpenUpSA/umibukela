# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0002_auto_20160120_1337'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='cycleresultset',
            unique_together=set([('cycle', 'site', 'survey_type')]),
        ),
    ]
