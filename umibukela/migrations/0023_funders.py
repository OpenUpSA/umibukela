# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0022_auto_20170127_1006'),
    ]

    operations = [
        migrations.CreateModel(
            name='Funder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='funder',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='umibukela.Funder', null=True),
        ),
    ]
