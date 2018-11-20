# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def change_resource_name(apps, schema_editor):
    ProgrammeResourceType = apps.get_model('umibukela',
                                           'ProgrammeResourceType')
    resource = ProgrammeResourceType.objects.get(name='Legislation')
    resource.name = 'Links'
    resource.save()


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0049_auto_20181118_1908'),
    ]

    operations = [migrations.RunPython(change_resource_name)]
