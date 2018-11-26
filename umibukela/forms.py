from django import forms
from django.contrib.gis.geos import Point
from widgets import AddAnotherWidgetWrapper
from django.core.exceptions import ValidationError

from .models import (Site, CycleResultSet, Monitor, ProgrammeResources,
                     ProgrammeImage)


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
        if args:  # If args exist
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


class CycleResultSetForm(forms.ModelForm):
    site_option_name = forms.CharField(widget=forms.TextInput)

    class Meta(object):
        model = CycleResultSet
        exclude = []

    def __init__(self, *args, **kwargs):
        super(CycleResultSetForm, self).__init__(*args, **kwargs)
        crs = kwargs.get('instance', None)
        if crs:
            partner = crs.partner
        else:
            partner = None
        self.fields['monitors'].queryset = Monitor.objects.filter(
            partner=partner)
        self.fields[
            'site_option_name'].help_text = "This is the name of the option for this site in the form, e.g. for 'Folweni clinic' it's probably 'folweni' (without the single quotes). You can find the names of options in the relevant Survey admin page."


class CRSFromKoboForm(forms.Form):
    def __init__(self, *args, **kwargs):
        facilities = kwargs.pop('facilities')
        super(CRSFromKoboForm, self).__init__(*args, **kwargs)

        for i, facility in enumerate(facilities):
            crs_field = forms.ModelChoiceField(
                queryset=CycleResultSet.objects.order_by('site__name').all(),
                label=facility['label'])
            crs_field.widget = AddAnotherWidgetWrapper(crs_field.widget,
                                                       CycleResultSet)
            self.fields['crs_%d' % i] = crs_field
            self.fields['facility_%d' % i] = forms.CharField(
                widget=forms.HiddenInput(), initial=facility['name'])
        self.fields['num_facilities'] = forms.CharField(
            widget=forms.HiddenInput(), initial=len(facilities))


class ProgrammeResourcesForm(forms.ModelForm):
    class Meta:
        model = ProgrammeResources
        exclude = ('document_extension', )

    def clean(self):
        link = self.cleaned_data.get('link')
        document = self.cleaned_data.get('document')
        order_no = self.cleaned_data.get('order')
        resource = self.cleaned_data.get('resource')
        programme = self.cleaned_data.get('programme')
        if link and document:
            raise ValidationError(
                "You cant have an External link and a Document")
        if ProgrammeResources.objects.filter(
                order=order_no, resource=resource,
                programme=programme).exists():
            raise ValidationError(
                'A Resource already exists for this order number')

        return self.cleaned_data


class ProgrammeImageForm(forms.ModelForm):
    class Meta:
        model = ProgrammeImage
        fields = '__all__'

    def clean(self):
        featured = self.cleaned_data.get('featured')
        programme = self.cleaned_data.get('programme')
        if featured:
            if ProgrammeImage\
               .objects\
               .filter(programme=programme, featured=True):
                raise ValidationError(
                    "An image in this programme is already marked as a featured image"
                )
        return self.cleaned_data
