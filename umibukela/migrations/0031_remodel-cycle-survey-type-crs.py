# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

from umibukela.models import Survey


def print_stuff(apps, schema_editor):
    print Survey.objects.filter(cycle=None).values("id")


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0030_pub_priv_survey_types'),
    ]

    operations = [
        migrations.RunSQL('SET CONSTRAINTS ALL IMMEDIATE',
                          reverse_sql=migrations.RunSQL.noop),
        migrations.AddField(
            model_name='survey',
            name='cycle',
            field=models.ForeignKey(related_name='cycle_result_sets', to='umibukela.Cycle', null=True),
        ),
        migrations.AddField(
            model_name='survey',
            name='type',
            field=models.ForeignKey(to='umibukela.SurveyType', null=True),
        ),
        migrations.RunSQL("""
        update umibukela_survey
        set cycle_id = crs.cycle_id,
        type_id = crs.survey_type_id
        from (select cycle_id, survey_id, survey_type_id
              from umibukela_cycleresultset
              group by cycle_id, survey_id, survey_type_id
        ) as crs
         where umibukela_survey.id = crs.survey_id;
        """),
        # delete a couple of surveys that don't make sense to have in the platform anyway
        # because they didn't have results. This doesn't mean we can't have survyes without
        # results, it's just that this migration doesn't handle that and doesn't need to.
        migrations.RunSQL("delete from umibukela_surveykoboproject where survey_id in (9, 25, 29)"),
        migrations.RunSQL("delete from umibukela_survey where id in (9, 25, 29)"),
        migrations.RunPython(print_stuff),
        migrations.AlterField(
            model_name='survey',
            name='cycle',
            field=models.ForeignKey(related_name='cycle_result_sets', to='umibukela.Cycle'),
        ),
        migrations.AlterField(
            model_name='survey',
            name='type',
            field=models.ForeignKey(to='umibukela.SurveyType'),
        ),
        migrations.AlterUniqueTogether(
            name='cycleresultset',
            unique_together=set([('site', 'survey')]),
        ),
        migrations.RemoveField(
            model_name='cycleresultset',
            name='cycle',
        ),
        migrations.RemoveField(
            model_name='cycleresultset',
            name='survey_type',
        ),
    ]
