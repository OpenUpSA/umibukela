# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0061_auto_20181126_0854'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='programmeresources',
            unique_together=set([('resource', 'order', 'programme')]),
        ),
    ]
