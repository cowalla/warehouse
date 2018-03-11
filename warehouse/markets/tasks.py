from django.db import transaction

from celery import task

from warehouse.settings import METACLIENT
from warehouse.markets.models import CurrencyTicker, MARKETS


ENABLED_MARKETS = ['liqui', 'poloniex']
ENABLED_MARKETS_PRODUCTS = {
    'gdax': [
        'usd_btc',
        'usd_eth',
        'usd_ltc',
        'usd_bch',
        'btc_eth',
        'btc_ltc',
        'btc_bch',
    ],
}


@task()
def update_tickers():
    currency_tickers = []

    for market in ENABLED_MARKETS:
        market_ticker = METACLIENT.ticker(market)

        for currency_pair, currency_data in market_ticker.iteritems():
            kwargs = currency_data.copy()
            kwargs['exchange'] = MARKETS[market]
            kwargs['currency_pair'] = currency_pair
            currency_tickers.append(CurrencyTicker(**kwargs))

    with transaction.atomic():
        for ticker in currency_tickers:
            ticker.save()


@task()
def update_product_tickers():
    currency_tickers = []

    for market, products in ENABLED_MARKETS_PRODUCTS.iteritems():
        for product in products:
            currency_data = METACLIENT.product_ticker(market, product)

            kwargs = currency_data.copy()
            kwargs['exchange'] = MARKETS[market]
            kwargs['currency_pair'] = product
            currency_tickers.append(CurrencyTicker(**kwargs))

    with transaction.atomic():
        for ticker in currency_tickers:
            ticker.save()
