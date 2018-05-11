# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

from umibukela.models import SurveyType


def poster_template(survey_type):
    template = 'print-materials/posters/'
    if 'paypoint' in survey_type.name.lower():
        template += 'paypoint_poster.html'
    elif 'health' in survey_type.name.lower():
        template += 'health_clinic_poster.html'
    elif 'service office' in survey_type.name.lower():
        template += 'service_office_poster.html'
    else:
        template += 'poster_layout.html'
    return template


def set_template_fields(apps, schema_editor):
    for survey_type in SurveyType.objects.filter(id__lt=8).all():
        survey_type.poster_template = poster_template(survey_type)
        survey_type.has_handout = True
        survey_type.save()


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0031_remodel-cycle-survey-type-crs'),
    ]

    operations = [
        migrations.AddField(
            model_name='surveytype',
            name='has_handout',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='surveytype',
            name='poster_template',
            field=models.CharField(help_text=b"Path of template from the application root. If it's blank, poster links won't be generated for this survey type.", max_length=1000, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='survey',
            name='cycle',
            field=models.ForeignKey(related_name='surveys', to='umibukela.Cycle'),
        ),
        migrations.RunPython(set_template_fields),
    ]
