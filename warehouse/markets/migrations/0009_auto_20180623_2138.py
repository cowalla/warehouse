# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0008_celery_intervals'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyticker',
            name='exchange',
            field=models.CharField(max_length=2, choices=[(b'3', b'poloniex'), (b'1', b'liqui'), (b'2', b'gdax'), (b'4', b'bittrex')]),
        ),
        migrations.AlterField(
            model_name='currencyticker',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, unique=True, editable=False),
        ),
    ]
