# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0057_auto_20181120_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyTypeData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datastudio', models.URLField()),
                ('cycle', models.ForeignKey(blank=True, to='umibukela.Cycle', null=True)),
                ('survey', models.ForeignKey(to='umibukela.SurveyType')),
            ],
        ),
    ]
