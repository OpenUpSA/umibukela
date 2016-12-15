# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0010_auto_20160530_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveySource',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('project_url', models.TextField(unique=True)),
                ('project_name', models.TextField()),
                ('survey', models.ForeignKey(to='umibukela.Survey')),
            ],
        ),
    ]
