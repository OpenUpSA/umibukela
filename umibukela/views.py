from django.shortcuts import render
from django.shortcuts import get_object_or_404
import pandas
import analysis

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

def poster(request, site_slug, result_id):
    result_set = get_object_or_404(
        CycleResultSet,
        id=result_id,
        site__slug__exact=site_slug
    )
    site_responses = [s.answers for s in result_set.submissions.all()]
    participants = { 'current': { 'male': 0, 'female': 0, 'total': 0 }, 'previous': { 'male': 0, 'female': 0, 'total': 0 } }
    site_results = None
    if site_responses:
        df = pandas.DataFrame(site_responses)
        form = result_set.survey.form
        participants['current'] = analysis.count_submissions(df)
        site_results = analysis.count_options(df, form['children'])
        site_results = analysis.calc_q_percents(site_results)
        prev_result_set = result_set.get_previous()
        if prev_result_set:
            prev_responses = [s.answers for s in prev_result_set.submissions.all()]
            if prev_responses:
                participants['previous'] = analysis.count_submissions(
                    pandas.DataFrame(prev_responses))
                prev_df = pandas.DataFrame(prev_responses)
                prev_form = prev_result_set.survey.form
                prev_results = analysis.count_options(prev_df, prev_form['children'])
                prev_results = analysis.calc_q_percents(prev_results)
            else:
                prev_results = None
        else:
            prev_results = None
        analysis.combine_curr_hist(site_results, prev_results)

    return render(request, 'poster_layout.html', {
        'active_tab': 'poster',
        'result_set': result_set,
        'prev_date': prev_result_set.cycle.start_date,
        'results': {
            'questions_dict': site_results,
            'participants': participants,
        }
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
