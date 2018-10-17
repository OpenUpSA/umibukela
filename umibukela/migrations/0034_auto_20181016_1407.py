# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify


def slugify_programme(apps, schema_editor):
    Programme = apps.get_model('umibukela', 'Programme')
    for programme in Programme.objects.all():
        programme.slug = slugify(programme.short_name)
        programme.save()


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0033_programme_slug'),
    ]

    operations = [migrations.RunPython(slugify_programme)]
