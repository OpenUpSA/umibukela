from django.shortcuts import render
import pandas
import results

from .models import (
    Partner,
    Site,
    CycleResultSet,
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
    site = Site.objects.get(slug=site_slug)
    return render(request, 'site_detail.html', {
        'active_tab': 'sites',
        'site': site,
    })


def site_result_hardcoded(request, site_slug, result_id):
    result_set = CycleResultSet.objects.get(
        id=result_id,
        site__slug__exact=site_slug
    )
    return render(request, 'site_result_hardcoded.html', {
        'active_tab': 'sites',
        'result_set': result_set,
    })


def site_result(request, site_slug, result_id):
    result_set = CycleResultSet.objects.get(
        id=result_id,
        site__slug__exact=site_slug
    )
    site_submissions = Submission.objects.filter(cycle_result_set=result_set)
    site_responses = [submission.answers for submission in site_submissions]
    site_totals = results.count_submissions(pandas.DataFrame(site_responses))
    form = result_set.survey.form
    site_results = results.count_options(
        pandas.DataFrame(site_responses),
        form['children']
    )
    site_results = results.calc_q_percents(site_results, site_totals)
    questions = results.questions_dict_to_array(site_results)

    return render(request, 'site_result_detail.html', {
        'active_tab': 'sites',
        'result_set': result_set,
        'results': {
            'questions': questions,
            'totals': site_totals
        }
    })


def partners(request):
    partners = Partner.objects.all().prefetch_related()
    return render(request, 'partners.html', {
        'active_tab': 'partners',
        'partners': partners,
    })


def partner(request, partner_slug):
    partner = Partner.objects.get(slug=partner_slug)
    return render(request, 'partner_detail.html', {
        'active_tab': 'partners',
        'partner': partner,
    })
