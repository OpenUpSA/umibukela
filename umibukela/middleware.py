from django.http import HttpResponsePermanentRedirect


class RedirectsMiddleware(object):
    """ Always redirect cbm.code4sa.org to cbm.blacksash.org.za
    """
    def process_request(self, request):
        if request.get_host() == 'cbm.code4sa.org':
            return HttpResponsePermanentRedirect("https://%s%s" % ('cbm.blacksash.org.za', request.get_full_path()))
