# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umibukela.models
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cycle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='CycleFrequency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CycleResultSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cycle', models.ForeignKey(to='umibukela.Cycle')),
            ],
        ),
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('full_name', models.CharField(max_length=200)),
                ('physical_address', models.CharField(max_length=200, null=True, blank=True)),
                ('contact_person', models.CharField(max_length=200, null=True, blank=True)),
                ('telephone', models.CharField(max_length=200)),
                ('email_address', models.EmailField(max_length=200)),
                ('intro_title', models.CharField(max_length=200)),
                ('intro_statement', models.TextField(max_length=200)),
                ('intro_image', models.ImageField(null=True, upload_to=umibukela.models.image_filename, blank=True)),
                ('context_quote', models.CharField(max_length=200)),
                ('context_statement', models.TextField(max_length=200)),
                ('context_image', models.ImageField(null=True, upload_to=umibukela.models.image_filename, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Programme',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=100)),
                ('long_name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('frequency', models.ForeignKey(blank=True, to='umibukela.CycleFrequency', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Sector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Site',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.CharField(unique=True, max_length=200)),
                ('address_1', models.CharField(max_length=200, null=True, blank=True)),
                ('address_2', models.CharField(max_length=200, null=True, blank=True)),
                ('address_3', models.CharField(max_length=200, null=True, blank=True)),
                ('telephone', models.CharField(max_length=200)),
                ('coordinates', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, blank=True)),
                ('province', models.ForeignKey(blank=True, to='umibukela.Province', null=True)),
                ('sector', models.ForeignKey(blank=True, to='umibukela.Sector', null=True)),
            ],
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='partner',
            field=models.ForeignKey(to='umibukela.Partner'),
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='site',
            field=models.ForeignKey(to='umibukela.Site'),
        ),
        migrations.AddField(
            model_name='cycle',
            name='programme',
            field=models.ForeignKey(to='umibukela.Programme'),
        ),
    ]
