from django.http import HttpResponsePermanentRedirect


class RedirectsMiddleware(object):
    """ Always redirect cbm.code4sa.org to cbm.blacksash.org.za
    """
    def process_request(self, request):
        if request.get_host() == 'cbm.code4sa.org':
            return HttpResponsePermanentRedirect("https://cbm.blacksash.org.za%s" % request.get_full_path())
