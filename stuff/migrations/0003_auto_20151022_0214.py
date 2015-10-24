# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0002_authenticator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authenticator',
            name='user_id',
            field=models.IntegerField(unique=True),
            preserve_default=True,
        ),
    ]
