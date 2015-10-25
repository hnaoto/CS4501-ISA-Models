# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0004_auto_20151021_2309'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='auth',
            field=models.ForeignKey(unique=True, null=True, to='stuff.Authenticator', blank=True),
            preserve_default=True,
        ),
    ]
