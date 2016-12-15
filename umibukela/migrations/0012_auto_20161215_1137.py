# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0011_surveysource'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveysource',
            old_name='project_name',
            new_name='name',
        ),
        migrations.RemoveField(
            model_name='surveysource',
            name='project_url',
        ),
        migrations.AddField(
            model_name='surveysource',
            name='form_id',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
