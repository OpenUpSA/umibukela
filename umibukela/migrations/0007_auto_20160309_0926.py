# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0006_auto_20160309_0823'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partner',
            options={'ordering': ('short_name',)},
        ),
        migrations.AlterModelOptions(
            name='site',
            options={'ordering': ('name',)},
        ),
    ]
