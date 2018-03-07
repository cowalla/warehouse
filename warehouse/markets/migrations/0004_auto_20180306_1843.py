# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0003_auto_20180305_0135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyticker',
            name='currency_pair',
            field=models.CharField(max_length=120),
        ),
        migrations.AlterField(
            model_name='currencyticker',
            name='exchange',
            field=models.CharField(max_length=120, choices=[(b'1', b'liqui')]),
        ),
    ]
