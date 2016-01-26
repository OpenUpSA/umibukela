# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0004_auto_20160120_1403'),
    ]

    operations = [
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answers', jsonfield.fields.JSONField(default=dict)),
                ('cycle_result_set', models.ForeignKey(blank=True, to='umibukela.CycleResultSet', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
                ('form', jsonfield.fields.JSONField(default=dict)),
            ],
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='survey',
            field=models.ForeignKey(blank=True, to='umibukela.Survey', null=True),
        ),
    ]
