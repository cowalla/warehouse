import json
import os
import time

from django.core.management import call_command
from django.db import transaction

from celery import task

from warehouse.settings import METACLIENT, BASE_DIR, BACKUP_DIR
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


def backup_tickers(tickers, filename, append=False, backup_to_s3=True):
    BACKUP_PATH = os.path.join(BASE_DIR, 'backups/txt')

    write_mode = 'a' if append else 'w'
    backup_filename = '%s.txt' % filename
    file_path = os.path.join(BACKUP_PATH, backup_filename)

    with open(file_path, write_mode) as backup:
        backup.writelines([json.dumps(t.as_dict()) for t in tickers])

    if backup_to_s3:
        from warehouse.utilities import upload_backup_to_s3

        upload_backup_to_s3(backup_filename)


# TODO: Move to better location
@task()
def small_backup_tickers():
    # get all tickers younger than an hour
    current_time = time.time()
    one_hour_ago_timestamp = current_time - 1 * (60 * 60)
    young_tickers = CurrencyTicker.objects.filter(updated__gte=one_hour_ago_timestamp)
    filename = str(int(current_time))

    backup_tickers(young_tickers, filename)


@task()
def backup_all_tickers():
    CHUNK_SIZE = 10000
    filename = 'big-%s' % str(int(time.time()))
    num_tickers = CurrencyTicker.objects.count()

    for offset in range(CHUNK_SIZE, num_tickers + CHUNK_SIZE, CHUNK_SIZE):
        tickers = CurrencyTicker.objects.filter(id__lte=offset, id__gt=offset - CHUNK_SIZE)
        backup_tickers(tickers, filename, append=True)


@task()
def sync_all_backups_to_s3():
    import os
    from warehouse.settings import BACKUP_DIR
    from warehouse.utilities import list_s3_file_names, upload_backup_to_s3

    s3_backups = list_s3_file_names()
    local_backups = os.listdir(BACKUP_DIR)
    missing_backups = list(set(local_backups) - set(s3_backups))

    for backup in missing_backups:
        upload_backup_to_s3(backup)


@task()
def backup_db():
    call_command('dbbackup')


# TODO: make work properly
def restore_db():
    call_command('dbrestore')
