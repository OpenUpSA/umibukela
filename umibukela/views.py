from django.shortcuts import render
from django.shortcuts import get_object_or_404
import pandas
import analysis

from .models import (
    CycleResultSet,
    Partner,
    Site,
    Submission,
)


def home(request):
    return render(request, 'index.html', {
        'active_tab': 'home',
    })


def contact(request):
    return render(request, 'contact.html', {
        'active_tab': 'contact',
    })


def about(request):
    return render(request, 'about.html', {
        'active_tab': 'about',
    })


def sites(request):
    sites = Site.objects.all().prefetch_related('province', 'sector')

    return render(request, 'sites.html', {
        'active_tab': 'sites',
        'sites': sites,
    })


def site(request, site_slug):
    site = get_object_or_404(Site, slug=site_slug)
    submissions = Submission.objects.filter(cycle_result_set__site__exact=site)
    site_responses = [s.answers for s in submissions.all()]
    if site_responses:
        df = pandas.DataFrame(site_responses)
        site_totals = analysis.count_submissions(df)
    else:
        site_totals = {'male': 0, 'female': 0, 'total': 0}

    return render(request, 'site_detail.html', {
        'active_tab': 'sites',
        'site': site,
        'totals': site_totals,
    })


def site_result_hardcoded(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
        site__slug__exact=site_slug
    )
    return render(request, 'site_result_hardcoded.html', {
        'active_tab': 'sites',
        'result_set': result_set,
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
        questions = analysis.questions_dict_to_array(site_results)
    else:
        questions = []
        site_totals = {'male': 0, 'female': 0, 'total': 0}

    return render(request, 'site_result_detail.html', {
        'active_tab': 'sites',
        'result_set': result_set,
        'results': {
            'questions': questions,
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
