# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0031_remodel-cycle-survey-type-crs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='surveykoboproject',
            options={'ordering': ('survey__name',)},
        ),
    ]
