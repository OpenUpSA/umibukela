from django.shortcuts import render


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
