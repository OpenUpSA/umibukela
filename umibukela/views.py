from itertools import groupby
from datetime import datetime, timedelta

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect

from forms import CRSFromKoboForm
from itertools import groupby
from xform import XForm
from wkhtmltopdf.views import PDFResponse
from wkhtmltopdf.utils import wkhtmltopdf

import pandas
import requests

import umibukela.analysis as analysis
from .forms import CRSFromKoboForm
from .models import (
    CycleResultSet,
    KoboRefreshToken,
    Partner,
    Site,
    Sector,
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
        site__slug__exact=site_slug,
        published=True
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
    sector_name = result_set.site.sector.name
    site = result_set.site.name
    layout_class = '-'.join(sector_name.lower().split(' '))
    location = None
    template = 'posters/'
    site_responses = [s.answers for s in result_set.submissions.all()]
    totals = {'current': {'male': 0, 'female': 0, 'total': 0}, 'previous': {'male': 0, 'female': 0, 'total': 0}}
    site_results = None

    if site_responses:
        form = result_set.survey.form
        map_questions(form, site_responses)
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
                map_questions(prev_form, prev_responses)
                simplify_perf_group(prev_form, prev_responses)
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
    site_responses = [s.answers for s in result_set.submissions.all()]

    context = {
        'result_set': result_set,
        'partner': result_set.partner,
        'site': result_set.site.name,
        'prev_date': None,
        'totals': {'male': 0, 'female': 0, 'total': 0},
        'DEBUG': settings.DEBUG,
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
        'orientation': 'landscape',
    })
    filename = '%s-%s-handout.pdf' % (site_slug, result_id)
    return PDFResponse(pdf, filename=filename, show_content_in_browser=True)


def simplify_perf_group(form, responses):
    """Raise exception if the assumptions about the categories are wrong"""
    label_to_simple = {
        'very poor': 'negative',
        'very poorly': 'negative',
        'not at all': 'negative',
        'mostly not': 'negative',
        'poor': 'negative',
        'not good, not bad': 'neutral',
        'not sure': 'neutral',
        'yes, sometimes': 'positive',
        'yes, definitely': 'positive',
        'well': 'positive',
        'good': 'positive',
        'mostly well': 'positive',
        'excellent': 'positive',
        'very well': 'positive',
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
                        orig_name_to_simple[name] = label_to_simple[label.lower()]
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
        for q in survey.form['children']:
            if q['name'] == 'facility':
                for o in q['children']:
                    facility_labels[o['name']] = o['label']
        facility_key = lambda r: r['facility']
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
                facility_name = answers['facility']
                submission = Submission(
                    answers=answers,
                    cycle_result_set=facility_crs[facility_name]
                )
                submission.save()
            return HttpResponseRedirect('/admin/umibukela/cycleresultset', status=303)
        return render(request, 'survey_kobo_submissions.html', {
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
        site_responses = [s for s in submissions if s.get('facility', s.get('site', None)) == site_name]
        site_responses = field_per_SATA_option(form, site_responses)
        map_questions(form, site_responses)

        if site_responses:
            df = pandas.DataFrame(site_responses)
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


def map_questions(form, submissions):
    form = XForm(form)
    mappings = [
        {
            'wrong_path': 'Select_your_gender',
            'right_path': 'demographics_group/gender',
        },
        {
            'wrong_path': 'Did_you_get_all_the_medication',
            'right_path': 'yes_no_group/all_medication',
        },
        {
            'wrong_path': 'How_would_you_rate_the_perform/how_good_are_the_ambulance_services_',
            'right_path': 'performance_group/ambulance',
        },
        {
            'wrong_path': 'How_would_you_rate_the_perform/does_the_clinic_have_the_necessary_equipment_in_good_working_condition_to_provide_the_services_you_need_',
            'right_path': 'performance_group/equipment',
        },
        {
            'wrong_path': 'Does_this_clinic_have_a_Clinic',
            'right_path': 'clinic_committee',
        },
        {
            'wrong_path': 'Do_you_know_what_the_Clinic_Co',
            'right_path': 'clinic_committee_function',
        },
        {
            'wrong_path': 'Do_you_think_that_this_clinic_',
            'right_path': 'clinic_feedback',
        },
        {
            'wrong_path': 'How_far_did_you_travel_to_get_',
            'right_path': 'travel_distance',
        },
        {
            'wrong_path': 'Waiting_Times/get_registered_at_reception',
            'right_path': 'waiting_group/register_time',
        },
        {
            'wrong_path': 'Waiting_Times/see_a_professional_nurse_or_doctor_',
            'right_path': 'waiting_group/professional_time',
        },
        {
            'wrong_path': 'Waiting_Times/collect_your_medication',
            'right_path': 'waiting_group/medicine_time',
        },
        {
            'wrong_path': 'Did_you_feel_safe_in_and_aroun',
            'right_path': 'yes_no_group/safety',
        },
        {
            'wrong_path': 'Did_the_staff_respect_your_rig',
            'right_path': 'yes_no_group/examined_private',
        },
        {
            'wrong_path': 'Did_the_nurse_or_doctor_explai',
            'right_path': 'yes_no_group/consent',
        },
        {
            'wrong_path': 'Do_you_know_how_to_make_a_comp',
            'right_path': 'yes_no_group/complaint',
        },
        {
            'wrong_path': 'Do_you_think_that_the_clinic_w',
            'right_path': 'yes_no_group/complaint_response',
        },
        {
            'wrong_path': 'How_would_you_rate_the_perform/was_the_clinic_clean_',
            'right_path': 'performance_group/clean',
        },
        {
            'wrong_path': 'How_would_you_rate_the_perform/did_the_clinic_manage_queues_well_',
            'right_path': 'performance_group/queues',
        },
        {
            'wrong_path': 'How_would_you_rate_the_perform/did_the_administrative_staff_treat_you_respectfully_',
            'right_path': 'performance_group/respect_admin',
        },
        {
            'wrong_path': 'How_would_you_rate_the_perform/did_the_health_professionals_doctors_and_nurses_treat_you_respectfully_',
            'right_path': 'performance_group/respect_professionals',
        },
    ]
    groups = {
        'demographics_group': {
            'label': 'Some questions about you',
        },
        'yes_no_group': {
            'label': 'Please answer yes or no to the following questions',
        },
        'performance_group': {
            'label': 'How would you rate the performance of the clinic staff in the following areas?',
        },
    }
    for mapping in mappings:
        q = form.get_by_path(mapping['wrong_path'])
        if q:
            print "found", mapping['wrong_path']
            path = mapping['right_path'].split('/')
            right_name = path[-1]
            group_path = path[:-1]
            if group_path:
                group = form.get_by_path('/'.join(group_path))
                if not group:
                    group = {
                        "label": 'fake label',
                        "type": "group",
                        "children": [],
                    }
                    form.set_by_path('/'.join(group_path), group)
            form.del_by_path(mapping['wrong_path'])
            form.set_by_path(mapping['right_path'], q)
            for s in submissions:
                s[mapping['right_path']] = s[mapping['wrong_path']]
                del s[mapping['wrong_path']]


def field_per_SATA_option(form, submissions):
    SATAs = [q for q in form['children'] if q['type'] == 'select all that apply']
    for SATA in SATAs:
        vals = [o['name'] for o in SATA['children']]
        submissions = map(
            lambda x: set_select_all_that_apply_fields(x, SATA['name'], vals),
            submissions
        )
    return submissions


def set_select_all_that_apply_fields(dict, q_key, possible_vals):
    if q_key not in dict:
        dict[q_key] = 'False'
    for val in possible_vals:
        dict['/'.join([q_key, val])] = 'False'
    for val in dict[q_key].split(' '):
        dict['/'.join([q_key, val])] = 'True'
    del dict[q_key]
    return dict


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
