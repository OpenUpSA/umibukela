from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings

import pandas
import analysis
from wkhtmltopdf.views import PDFResponse
from wkhtmltopdf.utils import wkhtmltopdf

from .models import (
    CycleResultSet,
    Partner,
    Site,
    Sector
)


def home(request):
    return render(request, 'index.html', {
        'active_tab': 'home',
    })


def about(request):
    return render(request, 'about.html', {
        'active_tab': 'about',
    })


def learn(request):
    return render(request, 'learn.html', {
        'active_tab': 'learn',
    })


def resources(request):
    return render(request, 'resources.html', {
        'active_tab': 'resources',
    })


def sites(request):
    sites = Site.objects.all().prefetch_related('province', 'sector')

    return render(request, 'sites.html', {
        'active_tab': 'sites',
        'sites': sites,
    })


def site(request, site_slug):
    site = get_object_or_404(Site, slug=site_slug)
    return render(request, 'site_detail.html', {
        'active_tab': 'sites',
        'site': site,
    })


def site_result(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
        site__slug__exact=site_slug
    )
    site_responses = [s.answers for s in result_set.submissions.all()]
    if site_responses:
        df = pandas.DataFrame(site_responses)
        form = result_set.survey.form
        site_totals = analysis.count_submissions(df)
        site_results = analysis.count_options(df, form['children'])
        site_results = analysis.calc_q_percents(site_results)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_responses = [s.answers for s in prev_result_set.submissions.all()]
            if prev_responses:
                site_totals = analysis.count_submissions(
                    pandas.DataFrame(site_responses + prev_responses))
                prev_df = pandas.DataFrame(prev_responses)
                prev_form = prev_result_set.survey.form
                prev_results = analysis.count_options(prev_df, prev_form['children'])
                prev_results = analysis.calc_q_percents(prev_results)
            else:
                prev_results = None
        else:
            prev_results = None
        analysis.combine_curr_hist(site_results, prev_results)
    else:
        site_totals = {'male': 0, 'female': 0, 'total': 0}
        site_results = None

    return render(request, 'site_result_detail.html', {
        'active_tab': 'sites',
        'result_set': result_set,
        'results': {
            'questions_dict': site_results,
            'totals': site_totals,
        }
    })


def poster(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
        site__slug__exact=site_slug
    )
    sector_id = result_set.site.sector.id
    sector_name = Sector.objects.get(id=sector_id).name
    site = result_set.site.name.split(' ', 1)[0]
    layout_class = '-'.join(sector_name.lower().split(' '))
    location = None
    template = 'posters/'
    site_responses = [s.answers for s in result_set.submissions.all()]
    totals = {'current': {'male': 0, 'female': 0, 'total': 0}, 'previous': {'male': 0, 'female': 0, 'total': 0}}
    site_results = None

    if site_responses:
        form = result_set.survey.form
        simplify_perf_group(form, site_responses)
        df = pandas.DataFrame(site_responses)
        totals['current'] = analysis.count_submissions(df)
        site_results = analysis.count_options(df, form['children'])
        site_results = analysis.calc_q_percents(site_results)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_responses = [s.answers for s in prev_result_set.submissions.all()]
            if prev_responses:
                prev_form = prev_result_set.survey.form
                simplify_perf_group(prev_form, prev_responses)
                totals['previous'] = analysis.count_submissions(
                    pandas.DataFrame(prev_responses))
                prev_df = pandas.DataFrame(prev_responses)
                prev_results = analysis.count_options(prev_df, prev_form['children'])
                prev_results = analysis.calc_q_percents(prev_results)
            else:
                prev_results = None
        else:
            prev_results = None
        analysis.combine_curr_hist(site_results, prev_results)

    if sector_id == Sector.SASSA_PAYPOINT:
        template += 'paypoint_poster.html'
    elif sector_id == Sector.LOCAL_GOV:
        template += 'local_gov_poster.html'
        sector_name = 'Participatory Governance'
        location = result_set.site.name
        site = 'Western Cape'
    elif sector_id == Sector.HEALTH_CLINIC:
        template += 'health_clinic_poster.html'
        sector_name += ' Clinic'
    elif sector_id == Sector.SASSA_SERVICE_OFFICE:
        template += 'service_office_poster.html'
        sector_name = 'SASSA Service Office'
    else:
        template += 'poster_layout.html'

    return render(request, template, {
        'result_set': result_set,
        'prev_date': prev_result_set.cycle.start_date,
        'totals': totals,
        'site': site,
        'sector': sector_name,
        'location': location,
        'questions_dict': site_results,
        'layout_class': layout_class,
        'DEBUG': settings.DEBUG,
    })


def poster_pdf(request, site_slug, result_id):
    # render poster as pdf
    url = reverse('site-result-poster', kwargs={'site_slug': site_slug, 'result_id': result_id})
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(url, **{
        'margin-top': '0.5cm',
        'margin-right': '0.5cm',
        'margin-bottom': '0.5cm',
        'margin-left': '0.5cm',
    })
    filename = '%s-%s-poster.pdf' % (site_slug, result_id)
    return PDFResponse(pdf, filename=filename)


def handout(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
        site__slug__exact=site_slug
    )
    prev_result_set = result_set.get_previous()
    site_responses = [s.answers for s in result_set.submissions.all()]

    context = {
        'result_set': result_set,
        'partner': result_set.partner,
        'site': result_set.site.name,
        'prev_date': None,
        'totals': {'male': 0, 'female': 0, 'total': 0}
    }

    if prev_result_set:
        context['prev_date'] = prev_result_set.cycle.start_date

    if site_responses:
        context['totals'] = analysis.count_submissions(pandas.DataFrame(site_responses))

    return render(request, 'handout_layout.html', context)


def handout_pdf(request, site_slug, result_id):
    # render handout as pdf
    url = reverse('site-result-handout', kwargs={'site_slug': site_slug, 'result_id': result_id})
    url = request.build_absolute_uri(url)
    pdf = wkhtmltopdf(url, **{
        'margin-top': '0.5cm',
        'margin-right': '0.5cm',
        'margin-bottom': '0.5cm',
        'margin-left': '0.5cm',
    })
    filename = '%s-%s-handout.pdf' % (site_slug, result_id)
    return PDFResponse(pdf, filename=filename)


def simplify_perf_group(form, responses):
    """Raise exception if the assumptions about the categories are wrong"""
    label_to_simple = {
        'Very Poor': 'negative',
        'Very poorly': 'negative',
        'Not at all': 'negative',
        'Mostly not': 'negative',
        'Poor': 'negative',
        'Not good, not bad': 'neutral',
        'Not sure': 'neutral',
        'Yes, sometimes': 'positive',
        'Yes, definitely': 'positive',
        'Well': 'positive',
        'Good': 'positive',
        'Mostly well': 'positive',
        'Excellent': 'positive',
        'Very well': 'positive',
    }
    orig_name_to_simple = {'n/a': 'n/a'}
    perf_questions = []
    for child in form['children']:
        if child.get('type', None) == 'group' and child.get('name', None) == 'performance_group':
            for q in child.get('children'):
                if q.get('type') == 'select one':
                    perf_questions.append('performance_group/%s' % q.get('name'))
                    for o in q.get('children'):
                        name = o['name']
                        label = o['label']
                        orig_name_to_simple[name] = label_to_simple[label]
                    q['children'] = [
                        {
                            "name": "negative",
                            "label": "Negative",
                        },
                        {
                            "name": "neutral",
                            "label": "Neutral",
                        },
                        {
                            "name": "positive",
                            "label": "Positive",
                        },
                    ]

    for response in responses:
        for key, val in response.iteritems():
            if key in perf_questions:
                response[key] = orig_name_to_simple[val]


def partners(request):
    partners = Partner.objects.all()
    return render(request, 'partners.html', {
        'active_tab': 'partners',
        'partners': partners,
    })


def partner(request, partner_slug):
    partner = get_object_or_404(Partner, slug=partner_slug)
    return render(request, 'partner_detail.html', {
        'active_tab': 'partners',
        'partner': partner,
    })
