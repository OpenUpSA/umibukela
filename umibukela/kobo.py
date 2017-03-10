import requests
from django.conf import settings
from datetime import datetime, timedelta


class Kobo(object):
    def __init__(self, acces_token, expiry_datetime, refresh_token):
        self.access_token = acces_token
        self.expiry_datetime = expiry_datetime
        self.refresh_token = refresh_token

    @classmethod
    def from_refresh_token(cls, refresh_token):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
        }
        r = requests.post("https://kc.kobotoolbox.org/o/token/",
                          params=payload,
                          auth=(settings.KOBO_CLIENT_ID, settings.KOBO_CLIENT_SECRET))
        r.raise_for_status()
        expiry_datetime = datetime.utcnow() + timedelta(seconds=r.json()['expires_in'])
        return cls(r.json()['access_token'], expiry_datetime, r.json()['refresh_token'])

    @classmethod
    def from_auth_code(cls, auth_code, redirect_uri):
        payload = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'redirect_uri': redirect_uri,
        }
        r = requests.post("https://kc.kobotoolbox.org/o/token/",
                          params=payload,
                          auth=(settings.KOBO_CLIENT_ID, settings.KOBO_CLIENT_SECRET))
        r.raise_for_status()
        expiry_datetime = datetime.utcnow() + timedelta(seconds=r.json()['expires_in'])
        return cls(r.json()['access_token'], expiry_datetime, r.json()['refresh_token'])

    def get_responses(self, form_id):
        headers = {
            'Authorization': "Bearer %s" % self.access_token,
        }
        r = requests.get("https://kc.kobotoolbox.org/api/v1/data/%s" % form_id, headers=headers)
        r.raise_for_status()
        return r.json()
