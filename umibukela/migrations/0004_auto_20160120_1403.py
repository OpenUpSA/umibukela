# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0003_auto_20160120_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cyclefrequency',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='partner',
            name='full_name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='partner',
            name='short_name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='programme',
            name='long_name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='programme',
            name='short_name',
            field=models.CharField(unique=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='province',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='sector',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='site',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='surveytype',
            name='name',
            field=models.CharField(unique=True, max_length=200),
        ),
        migrations.AlterUniqueTogether(
            name='cycle',
            unique_together=set([('name', 'programme')]),
        ),
    ]
