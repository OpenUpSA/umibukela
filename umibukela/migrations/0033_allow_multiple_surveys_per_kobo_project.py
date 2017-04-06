# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0032_ordered-kobo-projects'),
    ]

    operations = [
        migrations.RenameModel('SurveyKoboProject', 'KoboProject'),
        migrations.AlterField(
            model_name='koboproject',
            name='survey',
            field=models.ForeignKey(to='umibukela.Survey', primary_key=False),
        ),
        migrations.AddField(
            model_name='koboproject',
            name='id',
            field=models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='kobo_project',
            field=models.ForeignKey(to='umibukela.KoboProject', null=True),
        ),
        migrations.RunSQL("""
        update umibukela_survey
        set kobo_project_id = project_id
        from (select p.id as project_id, s.id as survey_id
              from umibukela_koboproject p, umibukela_survey s
              where p.survey_id = s.id) as survey_projects
        where id = survey_id;
        """),
        migrations.RemoveField(
            model_name='KoboProject',
            name='survey',
        ),
        # Unrelated small fix
        migrations.AlterField(
            model_name='survey',
            name='cycle',
            field=models.ForeignKey(to='umibukela.Cycle'),
        ),
    ]
