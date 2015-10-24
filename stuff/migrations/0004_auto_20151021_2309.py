# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0003_auto_20151022_0214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='authenticator',
            name='id',
        ),
        migrations.AlterField(
            model_name='authenticator',
            name='authenticator',
            field=models.CharField(serialize=False, max_length=255, primary_key=True),
            preserve_default=True,
        ),
    ]
