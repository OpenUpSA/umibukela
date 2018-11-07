# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0037_auto_20181106_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeStoryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=255)),
                ('image', models.ImageField(upload_to=b'story/images')),
                ('story', models.ForeignKey(to='umibukela.ProgrammeStory')),
            ],
        ),
        migrations.RemoveField(
            model_name='programmeimage',
            name='story',
        ),
        migrations.DeleteModel(
            name='ProgrammeImage',
        ),
    ]
