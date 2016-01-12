# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umibukela.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Partner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('short_name', models.CharField(max_length=200)),
                ('full_name', models.CharField(max_length=200)),
                ('physical_address', models.CharField(max_length=200)),
                ('contact_person', models.CharField(max_length=200)),
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
    ]
