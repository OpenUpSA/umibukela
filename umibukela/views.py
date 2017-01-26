from collections import Counter
from datetime import datetime, timedelta
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from itertools import groupby
from wkhtmltopdf.utils import wkhtmltopdf
from wkhtmltopdf.views import PDFResponse
from xform import XForm, map_questions, field_per_SATA_option
import analysis
import pandas
import requests

from .forms import CRSFromKoboForm
from .models import (
    CycleResultSet,
    KoboRefreshToken,
    Partner,
    Site,
    Survey,
    SurveyKoboProject,
    Submission,
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
    if not (result_set.published or request.user.is_superuser):
        raise Http404("No such CycleResultSet found")
    form, responses = result_set.get_survey()
    if responses:
        df = pandas.DataFrame(responses)
        site_totals = analysis.count_submissions(df)
        site_results = analysis.count_options(df, form['children'])
        site_results = analysis.calc_q_percents(site_results)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_form, prev_responses = prev_result_set.get_survey()
            if prev_responses:
                site_totals = analysis.count_submissions(
                    pandas.DataFrame(responses + prev_responses))
                prev_df = pandas.DataFrame(prev_responses)
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
    sector_name = result_set.site.sector.name
    survey_type = result_set.survey_type.name
    site = result_set.site.name
    layout_class = '-'.join(' '.join([x.strip() for x in survey_type.split('-')]).lower().split(' '))
    location = None
    template = 'posters/'
    form, responses = result_set.get_survey()
    totals = {'current': {'male': 0, 'female': 0, 'total': 0}, 'previous': {'male': 0, 'female': 0, 'total': 0}}
    site_results = None

    if responses:
        df = pandas.DataFrame(responses)
        totals['current'] = analysis.count_submissions(df)
        site_results = analysis.count_options(df, form['children'])
        site_results = analysis.calc_q_percents(site_results)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_form, prev_responses = prev_result_set.get_survey()
            if prev_responses:
                totals['previous'] = analysis.count_submissions(
                    pandas.DataFrame(prev_responses))
                prev_df = pandas.DataFrame(prev_responses)
                prev_results = analysis.count_options(prev_df, prev_form['children'])
                prev_results = analysis.calc_q_percents(prev_results)
                prev_date = prev_result_set.cycle.start_date
            else:
                prev_results = None
                prev_date = None
        else:
            prev_results = None
            prev_date = None
        analysis.combine_curr_hist(site_results, prev_results)

    if 'pay point' in result_set.site.name.lower():
        template += 'paypoint_poster.html'
        sector_name = None
    elif 'local gov' in result_set.site.sector.name.lower():
        template += 'local_gov_poster.html'
        sector_name = 'Participatory Governance'
        location = result_set.site.name
        site = 'Western Cape'
    elif 'health' in result_set.site.sector.name.lower():
        template += 'health_clinic_poster.html'
        sector_name = None
    elif 'service office' in result_set.site.name.lower():
        template += 'service_office_poster.html'
        sector_name = None
    else:
        template += 'poster_layout.html'

    return render(request, template, {
        'result_set': result_set,
        'prev_date': prev_date,
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
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def handout(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
        site__slug__exact=site_slug
    )
    prev_result_set = result_set.get_previous()
    form, responses = result_set.get_survey()

    context = {
        'result_set': result_set,
        'questions_dict': [],
        'partner': result_set.partner,
        'site': result_set.site.name,
        'prev_date': None,
        'totals': {'male': 0, 'female': 0, 'total': 0},
        'DEBUG': settings.DEBUG,
    }

    if prev_result_set:
        context['prev_date'] = prev_result_set.cycle.start_date

    if responses:
        df = pandas.DataFrame(responses)
        context['questions_dict'] = analysis.count_options(df, form['children'])
        context['totals'] = analysis.count_submissions(pandas.DataFrame(responses))

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
        'orientation': 'landscape',
    })
    filename = '%s-%s-handout.pdf' % (site_slug, result_id)
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def comments(request, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
    )
    skip_questions = [
        'surveyor',
        'capturer',
    ]
    questions = []
    for child in result_set.survey.form.get('children'):
        if child.get('type', None) == 'text' and child.get('name') not in skip_questions:
            comments = Counter([s.answers.get(child['name'], None)
                                for s in result_set.submissions.all()])
            comments.pop(None, None)
            comments.pop('n/a', None)

            questions.append({
                'label': child.get('label'),
                'comments': comments,
            })
    return render(request, 'comments.html', {
        'result_set': result_set,
        'questions': questions,
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


def survey_from_kobo(request):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization': "Bearer %s" % request.session.get('kobo_access_token'),
        }
        if request.method == 'POST':
            form_id = request.POST['form_id']
            r = requests.get("https://kc.kobotoolbox.org/api/v1/forms/%s/form.json" % form_id,
                             headers=headers)
            r.raise_for_status()
            form = r.json()
            survey = Survey(name=form['title'], form=r.text)
            survey.save()
            survey_kobo_project = SurveyKoboProject(survey=survey, form_id=form_id)
            survey_kobo_project.save()
            return redirect('/admin/umibukela/survey/%d' % survey.id)
        else:
            r = requests.get("https://kc.kobotoolbox.org/api/v1/forms",
                             headers=headers)
            r.raise_for_status()
            available_surveys = r.json()
            return render(request, 'survey_from_kobo.html', {
                'forms': available_surveys,
            })


def survey_kobo_submissions(request, survey_id):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization': "Bearer %s" % request.session.get('kobo_access_token'),
        }
        survey = get_object_or_404(Survey, id=survey_id)
        form_id = survey.surveykoboproject.form_id
        r = requests.get("https://kc.kobotoolbox.org/api/v1/data/%s" % form_id, headers=headers)
        r.raise_for_status()
        submissions = r.json()
        facilities = []
        facility_labels = {}
        form = XForm(survey.form)
        if form.get_by_path('facility'):
            facility_q_name = 'facility'
        elif form.get_by_path('site'):
            facility_q_name = 'site'
        else:
            raise Exception('No facility/site/location question')
        for q in survey.form['children']:
            if q['name'] == facility_q_name:
                for o in q['children']:
                    facility_labels[o['name']] = o['label']
        facility_key = lambda r: r[facility_q_name]
        facility_sorted = sorted(submissions, key=facility_key, reverse=True)
        facilities = []
        for facility_name, facility_group in groupby(facility_sorted, facility_key):
            facilities.append({
                'name': facility_name,
                'label': facility_labels[facility_name],
                'count': len(list(facility_group)),
            })
        crs_form = CRSFromKoboForm(facilities=facilities)
        if request.method == 'POST':
            num_facilities = request.POST['num_facilities']
            facility_crs = {}
            for i in xrange(int(num_facilities)):
                facility_name = request.POST['facility_%d' % i]
                crs_id = int(request.POST['crs_%d' % i])
                facility_crs[facility_name] = CycleResultSet.objects.get(pk=crs_id)
            submissions = field_per_SATA_option(survey.form, submissions)
            for answers in submissions:
                facility_name = answers[facility_q_name]
                submission = Submission(
                    answers=answers,
                    cycle_result_set=facility_crs[facility_name]
                )
                submission.save()
            return HttpResponseRedirect('/admin/umibukela/cycleresultset', status=303)
        return render(request, 'survey_kobo_submissions.html', {
            'submissions': submissions,
            'survey': survey,
            'facilities': facilities,
            'crs_form': crs_form,
        })


def kobo_forms(request):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization': "Bearer %s" % request.session.get('kobo_access_token'),
        }
        r = requests.get("https://kc.kobotoolbox.org/api/v1/forms",
                         headers=headers)
        r.raise_for_status()
        available_surveys = r.json()
        surveys = []
        for survey_json in available_surveys:
            survey = {
                'title': survey_json['title'],
                'num_of_submissions': survey_json['num_of_submissions'],
            }
            if 'formid' in survey_json:
                survey['kobo_form_id'] = survey_json['formid']
                r = requests.get("https://kc.kobotoolbox.org/api/v1/forms/%d/form.json" % survey_json['formid'],
                                 headers=headers)
                r.raise_for_status()
                form = r.json()
                fields = form.get('children', [])
                facility_fields = [c for c in fields if c.get('name', None) in ('facility', 'site')]
                if facility_fields:
                    survey['facilities'] = facility_fields[0]['children']
            surveys.append(survey)

        return render(request, 'kobo_forms.html', {
            'forms': surveys,
        })


def kobo_form_site_preview(request, kobo_form_id, site_name):
    if not is_kobo_authed(request):
        return start_kobo_oauth(request)
    else:
        headers = {
            'Authorization': "Bearer %s" % request.session.get('kobo_access_token'),
        }
        r = requests.get("https://kc.kobotoolbox.org/api/v1/forms/%s/form.json" % kobo_form_id, headers=headers)
        r.raise_for_status()
        form = r.json()
        r = requests.get("https://kc.kobotoolbox.org/api/v1/data/%s" % kobo_form_id, headers=headers)
        r.raise_for_status()
        submissions = r.json()
        responses = [s for s in submissions if s.get('facility', s.get('site', None)) == site_name]
        responses = field_per_SATA_option(form, responses)
        map_questions(form, responses)

        if responses:
            df = pandas.DataFrame(responses)
            site_totals = analysis.count_submissions(df)
            site_results = analysis.count_options(df, form['children'])
            site_results = analysis.calc_q_percents(site_results)
            prev_results = None
            analysis.combine_curr_hist(site_results, prev_results)
        else:
            site_totals = {'male': 0, 'female': 0, 'total': 0}
            site_results = None

        for q in form['children']:
            for option in q.get('children', []):
                if option['name'] == site_name:
                    site_label = option['label']
        return render(request, 'survey_preview.html', {
            'site_name': site_label,
            'form_title': form['title'],
            'results': {
                'questions_dict': site_results,
                'totals': site_totals,
            }
        })


def is_kobo_authed(request):
    kobo_expiry = request.session.get('kobo_access_token_expiry', None)
    return kobo_expiry and kobo_expiry > datetime.utcnow().isoformat()


def start_kobo_oauth(request):
    user_refresh_token = KoboRefreshToken.objects.filter(pk=request.user)
    if user_refresh_token.count():
        user_refresh_token = user_refresh_token.get()
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': user_refresh_token.token,
            'redirect_uri': 'http://localhost:8000/admin/kobo-oauth'
        }
        r = requests.post("https://kc.kobotoolbox.org/o/token/",
                          params=payload,
                          auth=(settings.KOBO_CLIENT_ID, settings.KOBO_CLIENT_SECRET))
        r.raise_for_status()
        request.session['kobo_access_token'] = r.json()['access_token']
        expiry_datetime = datetime.utcnow() + timedelta(seconds=r.json()['expires_in'])
        request.session['kobo_access_token_expiry'] = expiry_datetime.isoformat()
        user_refresh_token.token = r.json()['refresh_token']
        user_refresh_token.save()
        state = request.path
        return redirect(state)
    else:
        state = request.path
        return redirect("https://kc.kobotoolbox.org/o/authorize?client_id=%s&response_type=code&scope=read&state=%s" % (settings.KOBO_CLIENT_ID, state))


def kobo_oauth_return(request):
    state = request.GET.get('state')
    code = request.GET.get('code')
    payload = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': request.build_absolute_uri('/admin/kobo-oauth')
    }
    r = requests.post("https://kc.kobotoolbox.org/o/token/",
                      params=payload,
                      auth=(settings.KOBO_CLIENT_ID, settings.KOBO_CLIENT_SECRET))
    r.raise_for_status()
    request.session['kobo_access_token'] = r.json()['access_token']
    expiry_datetime = datetime.utcnow() + timedelta(seconds=r.json()['expires_in'])
    request.session['kobo_access_token_expiry'] = expiry_datetime.isoformat()

    user_refresh_token, created = KoboRefreshToken.objects.get_or_create(user=request.user)
    user_refresh_token.token = r.json()['refresh_token']
    user_refresh_token.save()
    return redirect(state)
