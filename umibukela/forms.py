from django import forms
from django.contrib.gis.geos import Point
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from jsonfield.widgets import JSONWidget
import json

from .models import (
    Site,
)


class SiteForm(forms.ModelForm):
    latitude = forms.DecimalField(
        min_value=-90,
        max_value=90,
        required=False,
    )
    longitude = forms.DecimalField(
        min_value=-180,
        max_value=180,
        required=False,
    )

    class Meta(object):
        model = Site
        exclude = []
        widgets = {'coordinates': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        if args:    # If args exist
            data = args[0]
            if data['latitude'] and data['longitude']:
                latitude = float(data['latitude'])
                longitude = float(data['longitude'])
                data['coordinates'] = Point(longitude, latitude)

        if 'instance' in kwargs and kwargs['instance'] is not None and kwargs['instance'].coordinates:
            coordinates = kwargs['instance'].coordinates.tuple
            initial = kwargs.get('initial', {})
            initial['longitude'] = coordinates[0]
            initial['latitude'] = coordinates[1]
            kwargs['initial'] = initial
        super(SiteForm, self).__init__(*args, **kwargs)


class SurveyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SurveyForm, self).__init__(*args, **kwargs)
        self.fields['form'].widget = SurveyFormWidget()


class SurveyFormWidget(JSONWidget):
    class Media:
        css = {
            'all': ('stylesheets/survey-form.css',)
        }
        js = ('javascript/survey-form.js',)

    def __init__(self, *args, **kwargs):
        super(SurveyFormWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        return mark_safe(render_to_string('survey-form.html', {
            'name': name,
            'formatted_json': json.dumps(
                value,
                sort_keys=True,
                indent=4,
                separators=(',', ': ')),
        }))
