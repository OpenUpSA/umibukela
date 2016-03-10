# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import umibukela.models


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0008_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttachmentNature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CycleResultSetAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', models.FileField(upload_to=umibukela.models.attachment_filename)),
                ('cycle_result_set', models.ForeignKey(related_name='attachments', to='umibukela.CycleResultSet')),
                ('nature', models.ForeignKey(to='umibukela.AttachmentNature')),
            ],
        ),
    ]
