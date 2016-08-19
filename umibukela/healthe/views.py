from __future__ import division
from datetime import date, timedelta
import math

import arrow
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.cache import cache_page

from umibukela.healthe.reports import build_stockout_xlsx, get_submissions, stockout_stats


STOCKOUTS_COLLECTION_START = date(2015, 11, 30)


def healthe_user(user):
    return settings.DEBUG or user.is_superuser or user.username == 'healthe'


@user_passes_test(healthe_user, login_url='/login/')
def home(request):
    # weeks for which stockout reports are available
    today = date.today()
    n = int(math.ceil((today - STOCKOUTS_COLLECTION_START).days / 7.0))
    weeks = [STOCKOUTS_COLLECTION_START + timedelta(7 * i) for i in xrange(n)]
    weeks.reverse()
    weeks = [[w, w + timedelta(days=6)] for w in weeks]

    return render(request, 'healthe/index.html', {
        'weeks': weeks,
    })


@user_passes_test(healthe_user, login_url='/login/')
@cache_page(3600)
def report_download(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    try:
        start_date = arrow.get(start_date).date()
    except arrow.ParserError:
        raise HttpResponseBadRequest("Date %s isn't valid: %s" % start_date)

    try:
        end_date = arrow.get(end_date).date()
    except arrow.ParserError:
        raise HttpResponseBadRequest("Date %s isn't valid: %s" % end_date)

    report = build_stockout_xlsx(start_date, end_date)

    response = HttpResponse(report, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    filename = 'Stockout Report - %s to %s' % (start_date.isoformat(), end_date.isoformat()) + ".xlsx"
    response['Content-Disposition'] = 'attachment; filename="' + filename + '"'
    return response


@cache_page(3600)
def stats(request):
    """ Return a bunch of historical stats in JSON,
    for use in the https://www.health-e.org.za/medicine-stockouts/ page.
    """
    # TODO: what about start of next year?
    start = date(2016, 1, 1)
    end = date.today() - timedelta(weeks=4)
    rows = get_submissions(start, end, 'json', 'start')
    return JsonResponse(stockout_stats(start, end, rows))
