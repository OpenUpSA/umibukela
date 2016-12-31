# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umibukela.models


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0010_auto_20160530_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycleresultsetattachment',
            name='file',
            field=umibukela.models.FileField(upload_to=umibukela.models.attachment_filename),
        ),
    ]
