# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umibukela.models


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partner',
            name='context_image',
            field=models.ImageField(upload_to=umibukela.models.image_filename),
        ),
        migrations.AlterField(
            model_name='partner',
            name='intro_image',
            field=models.ImageField(upload_to=umibukela.models.image_filename),
        ),
    ]
