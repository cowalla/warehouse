from django.db import transaction

from warehouse.settings import METACLIENT
from warehouse.markets.models import CurrencyTicker, MARKETS


class ChoiceEnum(object):
    def __init__(self, names_enums):
        self.names_enums = names_enums

    def as_choices(self):
        return tuple(
            (enum, name)
            for name, enum in self.names_enums.iteritems()
        )

    def names(self):
        return self.names_enums.keys()

    def __getitem__(self, item):
        return self.names_enums[item]


def update_tickers():
    currency_tickers = []

    for market in MARKETS.names():
        market_ticker = METACLIENT.ticker(market)

        for currency_pair, currency_data in market_ticker:
            kwargs = currency_data.copy()
            kwargs['currency_pair'] = currency_pair
            currency_tickers += CurrencyTicker(**kwargs)

    with transaction.atomic():
        for ticker in currency_tickers:
            ticker.save()