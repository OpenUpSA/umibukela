# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0011_cycleresultset_published'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyKoboProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.TextField(unique=True)),
                ('survey', models.ForeignKey(to='umibukela.Survey')),
            ],
        ),
    ]
