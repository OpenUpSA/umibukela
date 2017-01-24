# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('umibukela', '0017_koborefreshtoken'),
    ]

    operations = [
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('partner', models.ForeignKey(to='umibukela.Partner')),
            ],
        ),
        migrations.AlterModelOptions(
            name='cycle',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='cycleresultset',
            options={'ordering': ('site__name', 'partner__short_name')},
        ),
        migrations.AlterModelOptions(
            name='province',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='sector',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='survey',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='cycleresultset',
            name='published',
            field=models.BooleanField(default=False, help_text=b"Whether the results may be listed publicly with the assumption that it's somewhat validated"),
        ),
        migrations.AddField(
            model_name='cycleresultset',
            name='monitors',
            field=models.ManyToManyField(to='umibukela.Monitor'),
        ),
    ]
