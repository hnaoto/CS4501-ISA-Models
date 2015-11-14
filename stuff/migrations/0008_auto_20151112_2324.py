# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stuff', '0007_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobapplication',
            name='buyer',
            field=models.ForeignKey(to='stuff.Buyer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jobapplication',
            name='company',
            field=models.ForeignKey(to='stuff.Company'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='buyer',
            field=models.ForeignKey(to='stuff.Buyer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='transaction',
            name='seller',
            field=models.ForeignKey(to='stuff.Seller'),
            preserve_default=True,
        ),
    ]
