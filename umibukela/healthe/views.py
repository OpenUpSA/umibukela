from __future__ import division
from datetime import date, timedelta
import math

import arrow
from django.shortcuts import render
from django.http import HttpResponseBadRequest, HttpResponse

from umibukela.healthe.reports import build_stockout_xlsx


STOCKOUTS_COLLECTION_START = date(2015, 11, 30)


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
