# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0013_auto_20161215_1252'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveysource',
            name='survey',
        ),
        migrations.DeleteModel(
            name='SurveySource',
        ),
    ]
