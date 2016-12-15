from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import pandas
import analysis
import requests
import settings
from datetime import datetime, timedelta

from .models import (
    CycleResultSet,
    Partner,
    Site,
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
    kobo_expiry = request.session.get('kobo_access_token_expiry', None)
    if not kobo_expiry or kobo_expiry <= datetime.utcnow().isoformat():
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization': "Bearer %s" % request.session.get('kobo_access_token'),
        }
        r = requests.get("https://kc.kobotoolbox.org/api/v1/forms",
                         headers=headers)
        print r.text
        r.raise_for_status()
        forms = r.json()

        if request.method == 'GET':
            pass
        else:
            pass

        return render(request, 'survey_sources.html', {
            'survey_id': survey_id,
            'kobo_access_token_expiry': kobo_expiry,
            'forms': forms,
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
    print r.text
    r.raise_for_status()
    request.session['kobo_access_token'] = r.json()['access_token']
    expiry_datetime = datetime.utcnow() + timedelta(seconds=r.json()['expires_in'])
    request.session['kobo_access_token_expiry'] = expiry_datetime.isoformat()
    return redirect(state)
