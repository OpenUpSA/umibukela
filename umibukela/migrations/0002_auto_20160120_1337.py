# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SurveyType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='partner',
            name='context_statement',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='partner',
            name='intro_statement',
            field=models.TextField(),
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='survey_type',
            field=models.ForeignKey(blank=True, to='umibukela.SurveyType', null=True),
        ),
    ]
