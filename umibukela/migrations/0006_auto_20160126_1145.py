# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0005_auto_20160121_1049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='survey',
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='survey',
            field=models.ForeignKey(blank=True, to='umibukela.Survey', null=True),
        ),
    ]
