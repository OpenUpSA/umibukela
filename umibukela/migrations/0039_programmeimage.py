# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0038_auto_20181106_1251'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=b'programme/images/')),
                ('programme', models.ForeignKey(to='umibukela.Programme')),
            ],
        ),
    ]
