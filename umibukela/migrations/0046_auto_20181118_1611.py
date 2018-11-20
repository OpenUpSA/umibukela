# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def default_resource_types(apps, schema_editor):
    ProgrammeResourceType = apps.get_model('umibukela',
                                           'ProgrammeResourceType')
    ProgrammeResourceType.objects.bulk_create([
        ProgrammeResourceType(name='Legislation'),
        ProgrammeResourceType(name='Reports'),
        ProgrammeResourceType(name='Downloads')
    ])


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0045_programmeresourcetype'),
    ]

    operations = [migrations.RunPython(default_resource_types)]
