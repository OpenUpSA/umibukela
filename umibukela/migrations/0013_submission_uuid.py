# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0012_surveykoboproject'),
    ]

    operations = [
        migrations.AddField(
            model_name='submission',
            name='uuid',
            field=models.TextField(null=True,),
            preserve_default=False,
        ),
        migrations.RunSQL("DELETE FROM umibukela_submission where id in (2238, 19746, 19765, 2666)"),
        migrations.RunSQL("UPDATE umibukela_submission SET uuid = answers->'_uuid'"),
        migrations.AlterField(
            model_name='submission',
            name='uuid',
            field=models.TextField(unique=True),
            preserve_default=False,
        ),
    ]
