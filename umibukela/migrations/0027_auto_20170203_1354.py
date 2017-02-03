# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0026_survey_map_to_form'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveytype',
            name='description',
            field=models.TextField(help_text=b'This is a short line to indicate who is being surveyed to what degree, e.g. "Light-touch survey completed by users of facility X"'),
        ),
    ]
