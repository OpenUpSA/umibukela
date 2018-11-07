# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0036_auto_20181105_1350'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=b'story/images/')),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammeStory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('programme', models.ForeignKey(to='umibukela.Programme')),
            ],
        ),
        migrations.AddField(
            model_name='programmeimage',
            name='story',
            field=models.ForeignKey(to='umibukela.ProgrammeStory'),
        ),
    ]
