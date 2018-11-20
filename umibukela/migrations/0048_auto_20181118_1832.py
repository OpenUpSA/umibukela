# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0047_programmeresources'),
    ]

    operations = [
        migrations.RenameField(
            model_name='programmeresources',
            old_name='document_extenstion',
            new_name='document_extension',
        ),
        migrations.AlterField(
            model_name='programmeresources',
            name='order',
            field=models.IntegerField(help_text=b'The order in which the document should appear'),
        ),
    ]
