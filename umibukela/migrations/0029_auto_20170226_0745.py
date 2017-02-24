# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umibukela.models


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0028_cycle_materials'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeKoboRefreshToken',
            fields=[
                ('programme', models.OneToOneField(related_name='kobo_refresh_token', primary_key=True, serialize=False, to='umibukela.Programme')),
                ('token', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='KoboRefreshToken',
            new_name='UserKoboRefreshToken',
        ),
        migrations.AddField(
            model_name='cycle',
            name='auto_import',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='site_option_name',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cycle',
            name='materials',
            field=models.FileField(null=True, upload_to=umibukela.models.cycle_materials_filename, blank=True),
        ),
        migrations.AlterField(
            model_name='cycleresultset',
            name='cycle',
            field=models.ForeignKey(related_name='cycle_result_sets', to='umibukela.Cycle'),
        ),
        migrations.AlterField(
            model_name='cycleresultset',
            name='survey',
            field=models.ForeignKey(related_name='cycle_result_sets', blank=True, to='umibukela.Survey', null=True),
        ),
    ]
