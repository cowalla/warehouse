import time

from django.core.management import call_command
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


def current_utc_timestamp():
    return int(time.time())


def get_kwargs(currency_data, pair, market):
    kwargs = currency_data.copy()
    kwargs['exchange'] = MARKETS[market]
    kwargs['currency_pair'] = pair

    if not kwargs.get('updated'):
        kwargs['updated'] = current_utc_timestamp()

    return kwargs


def get_ticker_objects(ticker_response, market):
    return [
        CurrencyTicker(**get_kwargs(currency_data, currency_pair, market))
        for currency_pair, currency_data in ticker_response.iteritems()
    ]


@task()
def update_product_tickers(market, products):
    for product in products:
        update_product_ticker(market, product)


@task()
def update_product_ticker(market, product):
    ticker_response = METACLIENT.product_ticker(market, product)
    product_tickers = get_ticker_objects({product: ticker_response}, market)

    with transaction.atomic():
        for ticker in product_tickers:
            ticker.save()


@task()
def update_ticker(market):
    tickers_response = METACLIENT.ticker(market)
    currency_tickers = get_ticker_objects(tickers_response, market)

    with transaction.atomic():
        for ticker in currency_tickers:
            ticker.save()


# TODO: Move to better location
@task()
def backup_db():
    call_command('dbbackup')


# TODO: make work properly
def restore_db():
    call_command('dbrestore')
