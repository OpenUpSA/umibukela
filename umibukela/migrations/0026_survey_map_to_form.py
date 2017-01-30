# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0025_fix-cycle-1-cycle-2-format-mapping'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='map_to_form',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
