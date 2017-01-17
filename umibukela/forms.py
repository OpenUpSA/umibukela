from django import forms
from django.contrib.gis.geos import Point
from widgets import AddAnotherWidgetWrapper

from .models import (
    Site,
    CycleResultSet,
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


class CRSFromKoboForm(forms.Form):

    def __init__(self, *args, **kwargs):
        facilities = kwargs.pop('facilities')
        super(CRSFromKoboForm, self).__init__(*args, **kwargs)

        for i, facility in enumerate(facilities):
            crs_field = forms.ModelChoiceField(
                queryset=CycleResultSet.objects.all(),
                label=facility['label']
            )
            crs_field.widget = AddAnotherWidgetWrapper(crs_field.widget, CycleResultSet)
            self.fields['crs_%d' % i] = crs_field
            self.fields['facility_%d' % i] = forms.CharField(
                widget=forms.HiddenInput(),
                initial=facility['name']
            )
        self.fields['num_facilities'] = forms.CharField(
            widget=forms.HiddenInput(),
            initial=len(facilities)
        )
