# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0005_auto_20160126_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cycleresultset',
            name='partner',
            field=models.ForeignKey(related_name='cycle_result_sets', to='umibukela.Partner'),
        ),
        migrations.AlterField(
            model_name='cycleresultset',
            name='site',
            field=models.ForeignKey(related_name='cycle_result_sets', to='umibukela.Site'),
        ),
        migrations.AlterField(
            model_name='partner',
            name='context_quote',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='context_statement',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='email_address',
            field=models.EmailField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='intro_statement',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='intro_title',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='partner',
            name='telephone',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='cycle_result_set',
            field=models.ForeignKey(related_name='submissions', blank=True, to='umibukela.CycleResultSet', null=True),
        ),
    ]
