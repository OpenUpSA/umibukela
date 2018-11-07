# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0040_auto_20181106_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='programmestory',
            name='slug',
            field=models.SlugField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='programmeimage',
            name='programme',
            field=models.ForeignKey(related_name='program_image', to='umibukela.Programme'),
        ),
        migrations.AlterField(
            model_name='programmestoryimage',
            name='story',
            field=models.ForeignKey(related_name='story_image', to='umibukela.ProgrammeStory'),
        ),
    ]
