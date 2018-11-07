# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from django.utils.text import slugify


def slugify_programme_story(apps, schema_editor):
    ProgrammeStory = apps.get_model('umibukela', 'ProgrammeStory')
    for story in ProgrammeStory.objects.all():
        story.slug = slugify(story.title)
        story.save()


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0041_auto_20181107_0024'),
    ]

    operations = [migrations.RunPython(slugify_programme_story)]
