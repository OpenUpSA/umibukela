# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0020_auto_20170124_1443'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='monitor',
            options={'ordering': ('name',)},
        ),
    ]
