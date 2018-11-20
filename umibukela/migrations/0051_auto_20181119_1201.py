# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0050_auto_20181119_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmeresources',
            name='order',
            field=models.IntegerField(help_text=b'The order in which the document or link should appear'),
        ),
        migrations.AlterField(
            model_name='programmeresources',
            name='resource',
            field=models.ForeignKey(related_name='resource_type', to='umibukela.ProgrammeResourceType'),
        ),
    ]
