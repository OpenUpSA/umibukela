# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from umibukela.models import Programme, Funder


def noop(apps, schema_editor):
    pass


def create_funders(apps, schema_editor):
    mavc = Funder(name="MAVC")
    mavc.save()
    sash_funder = Funder(name="Brot fur die Welt; Constitutionalism Fund; ELMA Philanthropies SA; National Lotteries Commission; CS Mott Foundation; Open Society Foundation")
    sash_funder.save()

    # backfill funders for all cycle result sets
    programme = Programme.objects.filter(short_name="MAVC").first()
    if programme:
        for cycle in programme.cycle_set.all():
            for cycle_result_set in cycle.cycleresultset_set.all():
                cycle_result_set.funder = mavc
                cycle_result_set.save()

    mavc_cycle_3 = programme.cycle_set.filter(name="Cycle 3").get()
    programme = Programme.objects.filter(short_name="Black Sash").first()
    if programme:
        for cycle in programme.cycle_set.all():
            for cycle_result_set in cycle.cycleresultset_set.all():
                cycle_result_set.funder = sash_funder
                # move all the old "black sash" programme sets back to MAVC
                cycle_result_set.cycle = mavc_cycle_3

                cycle_result_set.save()


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
        migrations.RunPython(create_funders, noop),
    ]
