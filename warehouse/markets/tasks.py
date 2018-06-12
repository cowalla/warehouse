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


def get_product_tickers(market, product):
    ticker_response = METACLIENT.product_ticker(market, product)

    return get_ticker_objects({product: ticker_response}, market)


def get_exchange_tickers(market):
    tickers_response = METACLIENT.ticker(market)

    return get_ticker_objects(tickers_response, market)


def save_tickers(tickers):
    with transaction.atomic():
        for ticker in tickers:
            ticker.save()


@task()
def update_all_enabled_market_tickers():
    tickers = []

    for market in ENABLED_MARKETS:
        try:
            tickers += get_exchange_tickers(market)
        except:
            print 'Could not get tickers for %s' % market
            pass
    for market, products in ENABLED_MARKETS_PRODUCTS.iteritems():
        for product in products:
            try:
                tickers += get_product_tickers(market, product)
            except:
                print 'Could not get product tickers for %s, for product "%s"' % (market, product)
                pass

    save_tickers(tickers)


@task()
def update_ticker(market):
    exchange_tickers = get_exchange_tickers(market)

    save_tickers(exchange_tickers)


@task()
def update_product_tickers(market, products):
    product_tickers = []

    for product in products:
        product_tickers += get_product_tickers(market, product)

    save_tickers(product_tickers)

@task()
def update_product_ticker(market, product):
    update_product_tickers(market, [product])


# TODO: Move to better location
@task()
def backup_db():
    call_command('dbbackup')


# TODO: make work properly
def restore_db():
    call_command('dbrestore')
