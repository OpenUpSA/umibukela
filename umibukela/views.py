from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
import pandas
import analysis
import requests
import settings
from datetime import datetime, timedelta
from deep_eq import deep_eq
from copy import deepcopy

from .models import (
    CycleResultSet,
    Partner,
    Site,
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
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        survey = Survey.objects.get(pk=survey_id)
        headers = {
            'Authorization': "Bearer %s" % request.session.get('kobo_access_token'),
        }
        r = requests.get("https://kc.kobotoolbox.org/api/v1/forms",
                         headers=headers)
        r.raise_for_status()
        available_forms = r.json()

        if request.method == 'POST':
            if request.POST['action'] == 'add':
                formid = request.POST['form_id']
                r = requests.get(
                    "https://kc.kobotoolbox.org/api/v1/forms/%s/form.json" % formid,
                    headers=headers)
                r.raise_for_status()
                form = r.json()
                source = SurveySource(
                    survey=survey,
                    form_id=formid,
                    name=form['title'],
                    cached_form=form,
                    cache_date=datetime.utcnow()
                )
                source.save()
            elif request.POST['action'] == 'delete':
                source_id = request.POST['source_id']
                source = SurveySource.objects.get(pk=source_id).delete()
            else:
                raise Exception()

        current_sources = survey.surveysource_set.all()
        current_form_ids = [x.form_id for x in current_sources]
        other_forms = [x for x in available_forms if int(x['formid']) not in current_form_ids]

        return render(request, 'survey_sources.html', {
            'survey_name': survey.name,
            'survey_id': survey_id,
            'kobo_access_token_expiry': request.session.get('kobo_access_token_expiry'),
            'other_forms': other_forms,
            'current_sources': current_sources,
        })


def survey_sources_preview(request, survey_id):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        survey = Survey.objects.get(pk=survey_id)
        current_sources = list(survey.surveysource_set.all())
        first_form = current_sources[0].cached_form
        siteless_first = deepcopy(first_form)
        for source in current_sources[1:]:
            siteless_n = deepcopy(source.cached_form)
            deep_eq(siteless_first, siteless_n, _assert=True)

        return render(request, 'survey_preview.html', {
            'survey_name': survey.name,
            'survey_id': survey_id,
            'kobo_access_token_expiry': request.session.get('kobo_access_token_expiry'),
            'current_sources': current_sources,
            'form': first_form,
        })


def is_kobo_authed(request):
    kobo_expiry = request.session.get('kobo_access_token_expiry', None)
    return kobo_expiry and kobo_expiry > datetime.utcnow().isoformat()


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
