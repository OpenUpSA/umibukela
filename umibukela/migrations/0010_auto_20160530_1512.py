# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0009_attachmentnature_cycleresultsetattachment'),
    ]

    operations = [
        migrations.AddField(
            model_name='cycleresultset',
            name='action_items',
            field=models.TextField(help_text=b'Key challenges identified for improvement', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='follow_up',
            field=models.TextField(help_text=b'Follow ups to key challenges', null=True, blank=True),
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='follow_up_date',
            field=models.DateField(help_text=b'Date when follow up check was performed', null=True, blank=True),
        ),
    ]
