# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Authenticator',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('user_id', models.IntegerField()),
                ('authenticator', models.CharField(max_length=256)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
