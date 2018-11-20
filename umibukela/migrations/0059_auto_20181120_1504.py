# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0058_surveytypedata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveytypedata',
            name='datastudio',
            field=models.URLField(help_text=b'Embed Url to the datastudio chart'),
        ),
    ]
