from django.shortcuts import render

from .models import (
    Partner,
    Province,
    Sector,
    Site,
    CycleResultSet,
    Cycle,
    Programme,
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


def site_result(request, site_slug, result_id):
    result_set = CycleResultSet.objects.get(id=result_id, site__slug__exact=site_slug)
    return render(request, 'site_result_detail.html', {
        'active_tab': 'sites',
        'result_set': result_set,
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
