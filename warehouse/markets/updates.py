from django.db import transaction

from warehouse.settings import METACLIENT
from warehouse.markets.models import CurrencyTicker, MARKETS


def update_tickers():
    currency_tickers = []

    for market in MARKETS.names():
        market_ticker = METACLIENT.ticker(market)

        for currency_pair, currency_data in market_ticker.iteritems():
            kwargs = currency_data.copy()
            kwargs['exchange'] = market
            kwargs['currency_pair'] = currency_pair
            currency_tickers.append(CurrencyTicker(**kwargs))

    with transaction.atomic():
        for ticker in currency_tickers:
            ticker.save()

