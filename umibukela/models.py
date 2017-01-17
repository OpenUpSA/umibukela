
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
import analysis
import jsonfield
import os
import pandas
import uuid

# ------------------------------------------------------------------------------
# General utilities
# ------------------------------------------------------------------------------


def image_filename(instance, filename):
    """ Make image filenames
    """
    return 'images/%s_%s' % (uuid.uuid4(), os.path.basename(filename))


def attachment_filename(instance, filename):
    """ Make attachment filenames
    """
    return 'attachments/%s/%s' % (uuid.uuid4(), os.path.basename(filename))

# ------------------------------------------------------------------------------
# Models
# ------------------------------------------------------------------------------


class Sector(models.Model):
    name = models.CharField(max_length=200, unique=True)

    SASSA_PAYPOINT = 1
    LOCAL_GOV = 2
    HEALTH_CLINIC = 3
    SASSA_SERVICE_OFFICE = 4

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Partner(models.Model):
    short_name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    full_name = models.CharField(max_length=200, unique=True)
    physical_address = models.CharField(max_length=200, null=True, blank=True)
    contact_person = models.CharField(max_length=200, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    email_address = models.EmailField(max_length=200, null=True, blank=True)
    intro_title = models.CharField(max_length=200, null=True, blank=True)
    intro_statement = models.TextField(null=True, blank=True)
    intro_image = models.ImageField(upload_to=image_filename, null=True, blank=True)
    context_quote = models.CharField(max_length=200, null=True, blank=True)
    context_statement = models.TextField(null=True, blank=True)
    context_image = models.ImageField(upload_to=image_filename, null=True, blank=True)

    class Meta:
        ordering = ('short_name',)

    def __str__(self):
        return "[ID: %s] %s" % (self.id, self.short_name)

    def completed_result_sets(self):
        result_sets = list(self.cycle_result_sets.filter(cycle__end_date__lte=timezone.now()).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp, reverse=True)
        return result_sets

    def latest_complete_result(self):
        """Return the latest ended CycleResultSet, otherwise None"""
        result_sets = self.completed_result_sets()
        return result_sets[0] if result_sets else None

    def get_absolute_url(self):
        return reverse('partner', args=[self.slug])

    def sites(self):
        sites = list(set(Site.objects.filter(cycle_result_sets__partner=self).all()))
        sites.sort(key=lambda p: p.name)
        return sites


class Site(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    address_3 = models.CharField(max_length=200, null=True, blank=True)
    province = models.ForeignKey(Province, null=True, blank=True)
    telephone = models.CharField(max_length=200, null=True, blank=True)
    sector = models.ForeignKey(Sector, null=True, blank=True)
    coordinates = gis_models.PointField(null=True, blank=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return "[ID: %s] %s" % (self.id, self.name)

    def latest_complete_result(self):
        """Return the latest ended CycleResultSet, otherwise None"""
        result_sets = self.completed_result_sets()
        return result_sets[0] if result_sets else None

    def completed_result_sets(self):
        result_sets = list(self.cycle_result_sets.filter(
            cycle__end_date__lte=timezone.now(),
            published=True
        ).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp, reverse=True)
        return result_sets

    def result_sets(self):
        result_sets = list(CycleResultSet.objects.filter(site=self).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp, reverse=True)
        return result_sets

    def address_str(self):
        parts = [self.address_1, self.address_2, self.address_3]
        if self.province:
            parts.append(self.province.name)
        return ', '.join([p for p in parts if p])

    def partners(self):
        partners = list(set(Partner.objects.filter(cycle_result_sets__site=self).all()))
        partners.sort(key=lambda p: p.short_name)
        return partners

    def get_absolute_url(self):
        return reverse('site', args=[self.slug])


class CycleFrequency(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class Programme(models.Model):
    short_name = models.CharField(max_length=100, unique=True)
    long_name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    frequency = models.ForeignKey(CycleFrequency, null=True, blank=True)

    def __str__(self):
        return self.long_name


class Cycle(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    programme = models.ForeignKey(Programme)

    class Meta:
        unique_together = ('name', 'programme')

    def __str__(self):
        return "%s - %s [%s to %s]" % (
            self.name, self.programme.short_name, self.start_date, self.end_date
        )

    def end_date_cmp(a, b):
        if a.end_date > b.end_date:
            return 1
        elif a.end_date == b.end_date:
            return 0
        else:
            return -1


class SurveyType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()

    def __str__(self):
        return self.name


class Survey(models.Model):
    name = models.CharField(max_length=200, unique=True)
    form = jsonfield.JSONField()

    def __str__(self):
        return self.name


class SurveyKoboProject(models.Model):
    survey = models.OneToOneField(Survey, on_delete=models.CASCADE, primary_key=True)
    # Kobo is deprecating projects so from this point on,
    # when we refer to a kobo project (a form and its submissions),
    # the formid field is the unique reference for the URLs
    # https://kc.kobotoolbox.org/api/v1/forms/69399?format=json (project)
    # https://kc.kobotoolbox.org/api/v1/forms/69399/form.json (the xform as json)
    # https://kc.kobotoolbox.org/api/v1/data/69399?format=json (the submissions)
    form_id = models.IntegerField(unique=True, null=False)


class KoboRefreshToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    token = models.TextField(null=False, blank=False)


class CycleResultSet(models.Model):
    """
    An entity representing the data collection cycle for a given site
    and survey type, by the partner that collected the data for that site in
    the given cycle.

    This entity would be implicit if all resource and submissions relating to
    a given combination of cycle, site, partner and survey type referred to
    each of those individually, but that would be quite redundant, and since
    this is a first-class thing from the user's perspective (/site/x/results/y)
    it's nice to have this object to refer to. If there was instead a unique
    Cycle per site, the cycle start and end dates and name would be repeated
    for each site.
    """
    cycle = models.ForeignKey(Cycle)
    site = models.ForeignKey(Site, related_name='cycle_result_sets')
    partner = models.ForeignKey(Partner, related_name='cycle_result_sets')
    # This is meant to allow identifying comparable CycleResultSets
    # which don't necessarily have exactly the same survey
    survey_type = models.ForeignKey(SurveyType, null=True, blank=True)
    survey = models.ForeignKey(Survey, null=True, blank=True)

    action_items = models.TextField(null=True, blank=True, help_text="Key challenges identified for improvement. Markdown allowed.")
    follow_up_date = models.DateField(null=True, blank=True, help_text="Date when follow up check was performed")
    follow_up = models.TextField(null=True, blank=True, help_text="Follow ups to key challenges. Markdown allowed.")
    published = models.BooleanField(null=False, blank=False, help_text="Whether the results may be listed publicly with the assumption that it's somewhat validated", default=False)

    class Meta:
        unique_together = ('cycle', 'site', 'survey_type')

    def __str__(self):
        return "%s <- %s (%s)" % (
            self.site.name, self.partner.short_name, self.cycle
        )

    def end_date_cmp(a, b):
        return Cycle.end_date_cmp(a.cycle, b.cycle)

    def get_previous(self):
        result_sets = list(CycleResultSet.objects.filter(
            cycle__end_date__lte=self.cycle.start_date,
            site__exact=self.site,
            survey_type=self.survey_type,
            published=True
        ).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp)
        result_sets.reverse()
        if result_sets:
            return result_sets[0]
        else:
            return None

    def get_absolute_url(self):
        return reverse('site-result', args=[self.site.slug, str(self.id)])

    def summary(self):
        if getattr(self, '_summary', None) is None:
            answers = [s.answers for s in self.submissions.all()]
            if answers:
                df = pandas.DataFrame(answers)
                self._summary = analysis.count_submissions(df)
            else:
                self._summary = {'male': 0, 'female': 0, 'total': 0}
        return self._summary


class AttachmentNature(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class CycleResultSetAttachment(models.Model):
    cycle_result_set = models.ForeignKey(CycleResultSet, null=False, related_name='attachments')
    nature = models.ForeignKey(AttachmentNature, null=False)
    file = models.FileField(upload_to=attachment_filename, null=False)

    def __str__(self):
        return "%s -> %s (%s)" % (
            self.cycle_result_set, self.file.name, self.nature.name,
        )


class Submission(models.Model):
    answers = jsonfield.JSONField()
    uuid = models.TextField(unique=True)
    cycle_result_set = models.ForeignKey(
        CycleResultSet,
        null=True,
        blank=True,
        related_name="submissions"
    )
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        self.uuid = self.answers['_uuid']
        super(Submission, self).save(*args, **kwargs)
