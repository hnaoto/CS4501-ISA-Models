# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('resume_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=24)),
                ('description', models.TextField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='JobApplication',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('greeting', models.CharField(max_length=256)),
                ('detail', models.TextField(max_length=1000)),
                ('buyer', models.OneToOneField(to='stuff.Buyer')),
                ('company', models.OneToOneField(to='stuff.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Seller',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('company', models.OneToOneField(to='stuff.Company')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('negotiation', models.TextField(max_length=1000)),
                ('buyer', models.OneToOneField(to='stuff.Buyer')),
                ('seller', models.OneToOneField(to='stuff.Seller')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('password', models.CharField(max_length=96)),
                ('usertype', models.CharField(max_length=6)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='seller',
            name='user_account',
            field=models.ForeignKey(to='stuff.User', unique=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='buyer',
            name='user_account',
            field=models.ForeignKey(to='stuff.User', unique=True),
            preserve_default=True,
        ),
    ]
