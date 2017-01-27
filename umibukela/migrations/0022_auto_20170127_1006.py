# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.text import slugify
from umibukela.models import Province, SurveyType


def backfill_slugs(apps, schema_editor):
    for p in Province.objects.all():
        p.slug = slugify(p.name)
        p.save()
    for s in SurveyType.objects.all():
        s.slug = slugify(s.name)
        s.save()


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0021_auto_20170124_1557'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='surveytype',
            options={'ordering': ('name',)},
        ),
        migrations.AddField(
            model_name='province',
            name='slug',
            field=models.SlugField(unique=False, max_length=200, null=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='surveytype',
            name='slug',
            field=models.SlugField(unique=False, max_length=200, null=True),
            preserve_default=False,
        ),
        migrations.RunPython(backfill_slugs),
        migrations.AlterField(
            model_name='province',
            name='slug',
            field=models.SlugField(unique=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='surveytype',
            name='slug',
            field=models.SlugField(unique=True, max_length=200),
        ),
    ]
