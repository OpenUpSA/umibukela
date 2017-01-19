# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0015_auto_20170116_0859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='surveykoboproject',
            name='id',
        ),
        migrations.AlterField(
            model_name='surveykoboproject',
            name='survey',
            field=models.OneToOneField(primary_key=True, serialize=False, to='umibukela.Survey'),
        ),
    ]
