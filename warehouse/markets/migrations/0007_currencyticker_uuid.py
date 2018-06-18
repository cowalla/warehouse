# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, transaction
import uuid


CHUNK_SIZE = 10000

def create_uuid(apps, schema_editor):
    CurrencyTicker = apps.get_model('markets', 'CurrencyTicker')
    num_tickers = CurrencyTicker.objects.count()

    for offset in range(CHUNK_SIZE, num_tickers + CHUNK_SIZE, CHUNK_SIZE):
        tickers = CurrencyTicker.objects.filter(id__lte=offset, id__gt=offset - CHUNK_SIZE)

        with transaction.atomic():
            for ticker in tickers:
                ticker.uuid = uuid.uuid4()
                ticker.save()


class Migration(migrations.Migration):
    dependencies = [
        ('markets', '0006_auto_20180312_0532'),
    ]

    operations = [
        migrations.AddField(
            model_name='currencyticker',
            name='uuid',
            field=models.UUIDField(blank=True, null=True),
        ),
        migrations.RunPython(create_uuid),
        migrations.AlterField(
            model_name='currencyticker',
            name='uuid',
            field=models.UUIDField(unique=True)
        )
    ]
