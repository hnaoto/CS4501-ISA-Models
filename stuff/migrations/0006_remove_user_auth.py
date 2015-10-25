# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0005_user_auth'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='auth',
        ),
    ]
