# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0028_cycle_materials'),
    ]

    operations = [
        migrations.RenameField(
            model_name='surveytype',
            old_name='description',
            new_name='short_description',
        ),
        migrations.AddField(
            model_name='surveytype',
            name='full_description',
            field=models.TextField(default='', help_text=b'This is a thorough description used to fully explain the purpose behind the surveys of this type.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveytype',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cycleresultset',
            name='cycle',
            field=models.ForeignKey(related_name='cycle_result_sets', to='umibukela.Cycle'),
        ),
    ]
