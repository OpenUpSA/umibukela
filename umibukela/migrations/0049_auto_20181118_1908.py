# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0048_auto_20181118_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmeresources',
            name='link',
            field=models.URLField(help_text=b'An External http:// link', null=True, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='programmeresources',
            unique_together=set([('resource', 'order')]),
        ),
    ]
