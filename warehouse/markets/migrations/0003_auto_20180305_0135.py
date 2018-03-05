# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0002_auto_20180304_1749'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='currencyticker',
            name='currency',
        ),
        migrations.AddField(
            model_name='currencyticker',
            name='currency_pair',
            field=models.CharField(default='NONE', max_length=7),
            preserve_default=False,
        ),
    ]
