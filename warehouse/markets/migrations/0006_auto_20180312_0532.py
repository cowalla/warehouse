# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0005_auto_20180311_0431'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyticker',
            name='currency_pair',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='currencyticker',
            name='exchange',
            field=models.CharField(max_length=2, choices=[(b'3', b'poloniex'), (b'1', b'liqui'), (b'2', b'gdax')]),
        ),
    ]
