from django.conf import settings


def general(request):
    """ Add some useful settings into the template helpers.
    """
    info = {
        'SITE_NAME': 'Community-Based Monitoring',
    }

    ga_tracking_id = getattr(settings, 'GOOGLE_TAG_MANAGER', False)
    if not settings.DEBUG and ga_tracking_id:
        info['GOOGLE_TAG_MANAGER'] = ga_tracking_id

    return info
