# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0059_auto_20181120_1504'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmestory',
            name='summary',
            field=models.TextField(default=b'', help_text=b'Markdown is not supported'),
        ),
        migrations.AlterField(
            model_name='programmestory',
            name='description',
            field=models.TextField(help_text=b'Field is markdown supported'),
        ),
    ]
