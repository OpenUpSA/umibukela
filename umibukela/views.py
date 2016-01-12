from django.shortcuts import render
from .models import Partner


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
    return render(request, 'sites.html', {
        'active_tab': 'sites',
    })


def site(request, site_name):
    return render(request, 'site_detail.html', {
        'active_tab': 'sites',
    })


def site_result(request, site_name, result_id):
    return render(request, 'site_result_detail.html', {
        'active_tab': 'sites',
    })


def sectors(request):
    return render(request, 'sectors.html', {
        'active_tab': 'sectors',
    })


def sector(request, sector_name):
    return render(request, 'sector_detail.html', {
        'active_tab': 'sectors',
    })


def partners(request):
    return render(request, 'partners.html', {
        'active_tab': 'partners',
    })


def partner(request, partner_name):
    return render(request, 'partner_detail.html', {
        'active_tab': 'partners',
    })


def partner_by_id(request, partner_id):
    partner = Partner.objects.get(pk=partner_id)
    return render(request, 'partner_detail.html', {
        'active_tab': 'partners',
        'partner': partner
    })
