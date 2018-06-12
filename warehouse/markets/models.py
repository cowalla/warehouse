import uuid

from django.db import models
from django.contrib import admin

from warehouse.utilities import ChoiceEnum


MARKETS_LIST = {
    'liqui': '1',
    'gdax': '2',
    'poloniex': '3',
}
MARKETS_FULL_NAME_MAP = {v: k for k, v in MARKETS_LIST.iteritems()}
MARKETS = ChoiceEnum(MARKETS_LIST)


class CurrencyTicker(models.Model):
    currency_pair = models.CharField(max_length=20)
    exchange = models.CharField(max_length=2, choices=MARKETS.as_choices())

    average = models.FloatField(null=True, blank=True)
    base_volume = models.FloatField(null=True, blank=True)   # float,
    current_volume = models.FloatField(null=True, blank=True)   # float,
    high = models.FloatField(null=True, blank=True)   # float,
    highest_bid = models.FloatField(null=True, blank=True)   # float,
    is_frozen = models.IntegerField(null=True, blank=True)   # int,
    last = models.FloatField(null=True, blank=True)   # float,
    low = models.FloatField(null=True, blank=True)   # float,
    lowest_ask = models.FloatField(null=True, blank=True)   # float,
    percent_change = models.FloatField(null=True, blank=True)   # float,
    price = models.FloatField(null=True, blank=True)   # float,
    quote_volume = models.FloatField(null=True, blank=True)   # float,
    updated = models.PositiveIntegerField(null=True, blank=True)   # timestamp,

    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    def as_dict(self):
        return {
            'currency_pair': self.currency_pair,
            'exchange': MARKETS_FULL_NAME_MAP[self.exchange], # full name
            'average': self.average,
            'base_volume': self.base_volume,
            'current_volume': self.current_volume,
            'high': self.high,
            'highest_bid': self.highest_bid,
            'is_frozen': self.is_frozen,
            'last': self.last,
            'low': self.low,
            'lowest_ask': self.lowest_ask,
            'percent_change': self.percent_change,
            'price': self.price,
            'quote_volume': self.quote_volume,
            'updated': self.updated,
        }


admin.site.register(CurrencyTicker)