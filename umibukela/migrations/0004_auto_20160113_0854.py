# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umibukela.models


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0003_auto_20160113_0709'),
    ]

    operations = [
        migrations.CreateModel(
            name='Province',
            fields=[
                ('code', models.CharField(max_length=2, serialize=False, primary_key=True)),
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
        migrations.AlterField(
            model_name='partner',
            name='context_image',
            field=models.ImageField(null=True, upload_to=umibukela.models.image_filename),
        ),
        migrations.AlterField(
            model_name='partner',
            name='intro_image',
            field=models.ImageField(null=True, upload_to=umibukela.models.image_filename),
        ),
        migrations.AddField(
            model_name='partner',
            name='province',
            field=models.ForeignKey(to='umibukela.Province', null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='sector',
            field=models.ForeignKey(to='umibukela.Sector', null=True),
        ),
    ]
