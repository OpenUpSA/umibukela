from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.conf import settings
import pandas
import analysis
import requests
import settings
from datetime import datetime, timedelta

from .models import (
    CycleResultSet,
    Partner,
    Site,
    Sector,
    Survey,
    SurveySource,
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
    site = result_set.site.name.split(' ',1)[0]
    layout_class = '-'.join(sector_name.lower().split(' '))
    location = None
    template = 'posters/'
    site_responses = [s.answers for s in result_set.submissions.all()]
    totals = { 'current': { 'male': 0, 'female': 0, 'total': 0 }, 'previous': { 'male': 0, 'female': 0, 'total': 0 } }
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


def brochure(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
        site__slug__exact=site_slug
    )
    prev_result_set = result_set.get_previous()
    site = Site.objects.get(id=result_set.site_id)
    partner = Partner.objects.get(id=result_set.partner_id)
    site_responses = [s.answers for s in result_set.submissions.all()]

    context = {
        'result_set': result_set,
        'partner': result_set.partner,
        'site': result_set.site.name,
        'prev_date': None,
        'totals': { 'male': 0, 'female': 0, 'total': 0 }
    }

    if prev_result_set:
        context['prev_date'] = prev_result_set.cycle.start_date

    if site_responses:
        context['totals'] = analysis.count_submissions(pandas.DataFrame(site_responses))

    return render(request, 'brochure_layout.html', context)


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


def survey_sources(request, survey_id):
    survey = Survey.objects.get(pk=survey_id)
    kobo_expiry = request.session.get('kobo_access_token_expiry', None)
    if not kobo_expiry or kobo_expiry <= datetime.utcnow().isoformat():
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization': "Bearer %s" % request.session.get('kobo_access_token'),
        }
        r = requests.get("https://kc.kobotoolbox.org/api/v1/forms",
                         headers=headers)
        r.raise_for_status()
        forms = r.json()

        if request.method == 'POST':
            if request.POST['action'] == 'add':
                formid = request.POST['form_id']
                r = requests.get(
                    "https://kc.kobotoolbox.org/api/v1/forms/%s" % formid,
                    headers=headers)
                r.raise_for_status()
                form = r.json()
                source = SurveySource(
                    survey=survey,
                    form_id=formid,
                    name=form['description'],
                    cached_form=form,
                    cache_date=datetime.utcnow()
                )
                source.save()

        return render(request, 'survey_sources.html', {
            'survey_name': survey.name,
            'survey_id': survey_id,
            'kobo_access_token_expiry': kobo_expiry,
            'other_forms': forms,
        })


def start_kobo_oauth(request):
    state = request.path
    return redirect("https://kc.kobotoolbox.org/o/authorize?client_id=%s&response_type=code&scope=read&state=%s" % (settings.KOBO_CLIENT_ID, state))


def kobo_oauth_return(request):
    state = request.GET.get('state')
    code = request.GET.get('code')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': 'http://localhost:8000/admin/kobo-oauth'
    }
    r = requests.post("https://kc.kobotoolbox.org/o/token/",
                     params=payload,
                     auth=(settings.KOBO_CLIENT_ID, settings.KOBO_CLIENT_SECRET))
    r.raise_for_status()
    request.session['kobo_access_token'] = r.json()['access_token']
    expiry_datetime = datetime.utcnow() + timedelta(seconds=r.json()['expires_in'])
    request.session['kobo_access_token_expiry'] = expiry_datetime.isoformat()
    return redirect(state)
