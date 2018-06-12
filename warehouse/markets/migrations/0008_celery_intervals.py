# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations

from djcelery.models import PeriodicTask, IntervalSchedule


def add_basic_intervals(apps, schema_editor):
    every_minute, _ = IntervalSchedule.objects.get_or_create(every=1, period='minutes')
    every_hour, _ = IntervalSchedule.objects.get_or_create(every=1, period='hours')
    every_day, _ = IntervalSchedule.objects.get_or_create(every=1, period='days')
    every_three_days, _ = IntervalSchedule.objects.get_or_create(every=3, period='days')

    PeriodicTask.objects.get_or_create(
        name='Update all enabled tickers',
        task='warehouse.markets.tasks.update_all_enabled_market_tickers',
        interval=every_minute
    )
    PeriodicTask.objects.get_or_create(
        name='Backup new tickers to txt',
        task='warehouse.markets.tasks.small_backup_tickers',
        interval=every_minute
    )


class Migration(migrations.Migration):

    dependencies = [
        ('markets', '0007_currencyticker_uuid'),
    ]

    operations = [
        migrations.RunPython(add_basic_intervals),
    ]
