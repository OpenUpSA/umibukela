# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0046_auto_20181118_1611'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeResources',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.IntegerField()),
                ('title', models.CharField(max_length=50)),
                ('link', models.URLField(null=True, blank=True)),
                ('document', models.FileField(null=True, upload_to=b'programme/resources/', blank=True)),
                ('document_extenstion', models.CharField(max_length=15, null=True, blank=True)),
                ('programme', models.ForeignKey(to='umibukela.Programme')),
                ('resource', models.ForeignKey(to='umibukela.ProgrammeResourceType')),
            ],
        ),
    ]
