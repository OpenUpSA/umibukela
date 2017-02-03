# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0027_auto_20170203_1354'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveytype',
            name='ignore_paths',
            field=models.TextField(default=b'', help_text=b'Paths that should not be presented on summaries. Separate by space, e.g. each path on a new line.'),
        ),
    ]
