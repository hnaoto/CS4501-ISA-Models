# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0008_auto_20151112_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=24, unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='seller',
            name='company',
            field=models.ForeignKey(to='stuff.Company'),
            preserve_default=True,
        ),
    ]
