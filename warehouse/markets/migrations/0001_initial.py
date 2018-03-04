# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ticker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('exchange', models.CharField(max_length=1, choices=[(b'1', b'liqui')])),
                ('average', models.FloatField(null=True, blank=True)),
                ('base_volume', models.FloatField(null=True, blank=True)),
                ('current_volume', models.FloatField(null=True, blank=True)),
                ('high', models.FloatField(null=True, blank=True)),
                ('highest_bid', models.FloatField(null=True, blank=True)),
                ('is_frozen', models.IntegerField(null=True, blank=True)),
                ('last', models.FloatField(null=True, blank=True)),
                ('low', models.FloatField(null=True, blank=True)),
                ('lowest_ask', models.FloatField(null=True, blank=True)),
                ('percent_change', models.FloatField(null=True, blank=True)),
                ('price', models.FloatField(null=True, blank=True)),
                ('quote_volume', models.FloatField(null=True, blank=True)),
                ('updated', models.PositiveIntegerField(null=True, blank=True)),
            ],
        ),
    ]
