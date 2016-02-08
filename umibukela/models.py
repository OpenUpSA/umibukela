import os
import uuid

from django.db import models
from django.contrib.gis.db import models as gis_models
import jsonfield
from django.utils import timezone

# ------------------------------------------------------------------------------
# General utilities
# ------------------------------------------------------------------------------


def image_filename(instance, filename):
    """ Make image filenames
    """
    return 'images/%s_%s' % (uuid.uuid4(), os.path.basename(filename))

# ------------------------------------------------------------------------------
# Models
# ------------------------------------------------------------------------------


class Sector(models.Model):
    name = models.CharField(max_length=200, unique=True)

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
    telephone = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=200)
    intro_title = models.CharField(max_length=200)
    intro_statement = models.TextField()
    intro_image = models.ImageField(upload_to=image_filename, null=True, blank=True)
    context_quote = models.CharField(max_length=200)
    context_statement = models.TextField()
    context_image = models.ImageField(upload_to=image_filename, null=True, blank=True)

    def __str__(self):
        return "[ID: %s] %s" % (self.id, self.short_name)

    def latest_complete_result(self):
        """Return the latest ended CycleResultSet, otherwise None"""
        result_sets = list(
            self.cycle_result_sets.filter(cycle__end_date__lte=timezone.now()).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp)
        result_sets.reverse()
        return result_sets[0] if result_sets else None


class Site(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=200, unique=True)
    address_1 = models.CharField(max_length=200, null=True, blank=True)
    address_2 = models.CharField(max_length=200, null=True, blank=True)
    address_3 = models.CharField(max_length=200, null=True, blank=True)
    province = models.ForeignKey(Province, null=True, blank=True)
    telephone = models.CharField(max_length=200)
    sector = models.ForeignKey(Sector, null=True, blank=True)
    coordinates = gis_models.PointField(null=True, blank=True)

    def __str__(self):
        return "[ID: %s] %s" % (self.id, self.name)

    def latest_complete_result(self):
        """Return the latest ended CycleResultSet, otherwise None"""
        result_sets = list(
            self.cycle_result_sets.filter(cycle__end_date__lte=timezone.now()).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp)
        result_sets.reverse()
        return result_sets[0] if result_sets else None

    def result_sets(self):
        return CycleResultSet.objects.filter(site=self).all()


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
        return "%s [%s to %s]" % (
            self.programme.short_name, self.start_date, self.end_date
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

    class Meta:
        unique_together = ('cycle', 'site', 'survey_type')

    def __str__(self):
        return "%s -> %s (%s)" % (
            self.partner.short_name, self.site.name, self.cycle
        )

    def end_date_cmp(a, b):
        return Cycle.end_date_cmp(a.cycle, b.cycle)

    def get_previous(self):
        result_sets = list(CycleResultSet.objects.filter(
            cycle__end_date__lte=self.cycle.start_date,
            site__exact=self.site,
            survey_type=self.survey_type,
        ).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp)
        result_sets.reverse()
        if result_sets:
            return result_sets[0]
        else:
            return None


class Submission(models.Model):
    answers = jsonfield.JSONField()
    cycle_result_set = models.ForeignKey(
        CycleResultSet,
        null=True,
        blank=True,
        related_name="submissions"
    )
