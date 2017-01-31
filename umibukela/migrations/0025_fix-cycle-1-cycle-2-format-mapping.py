# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from umibukela.models import Submission


def fix_option(apps, schema_editor):
    for s in Submission.objects.all():
        if s.answers.get('visit_frequency', None) == 'third_mode':
            s.answers['visit_frequency'] = 'third_more'
            s.save()


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0024_funder-fill'),
    ]

    operations = [
        migrations.RunPython(fix_option),
    ]
