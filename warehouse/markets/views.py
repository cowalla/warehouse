from django.http import JsonResponse, Http404

from warehouse.markets.models import CurrencyTicker, MARKETS


def currency_ticker(request):
    exchange = request.GET.get('exchange')
    before = request.GET.get('before')
    after = request.GET.get('after')
    currency_pair = request.GET.get('currency_pair')
    tickers = CurrencyTicker.objects.filter(exchange=MARKETS[exchange])

    if currency_pair:
        tickers = tickers.filter(currency_pair=currency_pair)
    if before:
        tickers = tickers.filter(updated__lte=before)
    if after:
        tickers = tickers.filter(updated__gte=after)

    data = [
        t.as_dict()
        for t in tickers
    ]

    return JsonResponse(data, safe=False)
