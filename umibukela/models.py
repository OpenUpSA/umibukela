from background_task import background
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.core.files import File
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.utils.text import slugify
from kobo import Kobo
from os import makedirs, path
from tempfile import mkdtemp, NamedTemporaryFile
from xform import field_per_SATA_option, skipped_as_na
from xform import map_form, simplify_perf_group, XForm
from zipfile import ZipFile
import analysis
import copy
import json
import jsonfield
import pandas
import pprint
import re
import requests
import shutil
import uuid

# ------------------------------------------------------------------------------
# General utilities
# ------------------------------------------------------------------------------


def image_filename(instance, filename):
    """ Make image filenames
    """
    return 'images/%s_%s' % (uuid.uuid4(), path.basename(filename))


def attachment_filename(instance, filename):
    """ Make attachment filenames
    """
    return 'attachments/%s/%s' % (uuid.uuid4(), path.basename(filename))


def cycle_materials_filename(instance, filename):
    """ Make cycle materials Zip filenames
    """
    return 'cycle_materials/%s' % path.basename(filename)


# ------------------------------------------------------------------------------
# Models
# ------------------------------------------------------------------------------


class Sector(models.Model):
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Province(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Funder(models.Model):
    name = models.CharField(max_length=200, unique=True)
    website = models.URLField(null=True)
    logo = models.FileField(null=True, upload_to='funder/logo/')

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
    intro_image = models.ImageField(
        upload_to=image_filename, null=True, blank=True)
    context_quote = models.CharField(max_length=200, null=True, blank=True)
    context_statement = models.TextField(null=True, blank=True)
    context_image = models.ImageField(
        upload_to=image_filename, null=True, blank=True)

    class Meta:
        ordering = ('short_name', )

    def __str__(self):
        return self.short_name

    def completed_result_sets(self):
        result_sets = list(
            self.cycle_result_sets.filter(
                survey__cycle__end_date__lte=timezone.now(),
                published=True).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp, reverse=True)
        return result_sets

    def latest_complete_result(self):
        """Return the latest ended CycleResultSet, otherwise None"""
        result_sets = self.completed_result_sets()
        return result_sets[0] if result_sets else None

    def get_absolute_url(self):
        return reverse('partner', args=[self.slug])

    def sites(self):
        sites = list(
            set(Site.objects.filter(cycle_result_sets__partner=self).all()))
        sites.sort(key=lambda p: p.name)
        return sites


class Monitor(models.Model):
    name = models.TextField()
    partner = models.ForeignKey(Partner)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return "%s (%s)" % (self.name, self.partner.short_name)


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
        ordering = ('name', )

    def __str__(self):
        return self.name

    def latest_complete_result(self):
        """Return the latest ended CycleResultSet, otherwise None"""
        result_sets = self.completed_result_sets()
        return result_sets[0] if result_sets else None

    def completed_result_sets(self):
        result_sets = list(
            self.cycle_result_sets.filter(
                survey__cycle__end_date__lte=timezone.now(),
                published=True).all())
        result_sets.sort(cmp=CycleResultSet.end_date_cmp, reverse=True)
        return result_sets

    def programmes_latest_results(self):
        """
        Return a distinct list of programmes and the latest completed
        result set for the programme at that site
        """
        programmes = {}
        for result_set in self.completed_result_sets():
            programme = result_set.survey.cycle.programme
            # Relies on the latest completed result sets coming up first.
            if programme.id not in programmes:
                programmes[programme.id] = (programme, result_set)
        return programmes.values()

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
        partners = list(
            set(Partner.objects.filter(cycle_result_sets__site=self).all()))
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
    slug = models.SlugField(max_length=200, unique=True, blank=True)

    def cycles(self):
        cycles = list(set(Cycle.objects.all()))
        cycles.sort(key=lambda p: p.name)
        return cycles

    def __str__(self):
        return self.long_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_name)
        super(Programme, self).save(*args, **kwargs)


class Cycle(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateField()
    end_date = models.DateField()
    programme = models.ForeignKey(Programme)
    materials = models.FileField(
        upload_to=cycle_materials_filename, blank=True, null=True)
    auto_import = models.BooleanField()

    class Meta:
        unique_together = ('name', 'programme')
        ordering = ('name', )

    def __str__(self):
        return "%s - %s [%s to %s]" % (self.name, self.programme.short_name,
                                       self.start_date, self.end_date)

    def end_date_cmp(a, b):
        if a.end_date > b.end_date:
            return 1
        elif a.end_date == b.end_date:
            return 0
        else:
            return -1

    def get_previous(self):
        cycles = list(
            Cycle.objects.filter(
                end_date__lte=self.start_date,
                programme=self.programme,
            ).all())
        cycles.sort(cmp=Cycle.end_date_cmp)
        cycles.reverse()
        if cycles:
            return cycles[0]
        else:
            return None

    @staticmethod
    @background(schedule=0)
    def schedule_create_materials_zip(cycle_id, artifacts):
        cycle = Cycle.objects.get(id=cycle_id)
        cycle.create_materials_zip(artifacts)

    def create_materials_zip(self, artifacts):
        tmpdir = mkdtemp()
        try:
            to_archive = []
            for artifact in artifacts:
                archive_dir = artifact['dir']
                localdir = path.join(tmpdir, archive_dir)
                if not path.isdir(localdir):
                    makedirs(localdir)
                r = requests.get(artifact['url'], stream=True)
                d = r.headers['content-disposition']
                filename = re.findall("filename=\"(.+)\"", d)[0]
                local_filename = path.join(localdir, filename)
                archive_filename = path.join(archive_dir, filename)
                with open(local_filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                to_archive.append({
                    'local_filename': local_filename,
                    'archive_filename': archive_filename,
                })
            ziptmpdir = mkdtemp()
            try:
                with NamedTemporaryFile(dir=ziptmpdir, delete=False) as zfh:
                    with ZipFile(zfh, 'w') as zf:
                        for file in to_archive:
                            zf.write(file['local_filename'],
                                     file['archive_filename'])
                    filename = "%s-%s-%s-to-%s.zip" % (
                        slugify(self.name),
                        slugify(self.programme.short_name),
                        self.start_date,
                        self.end_date,
                    )
                    self.materials.save(filename, File(zfh))
            finally:
                shutil.rmtree(ziptmpdir)
        finally:
            shutil.rmtree(tmpdir)


class SurveyType(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    short_description = models.TextField(
        help_text=
        "This is a short line to indicate who is being surveyed to what degree, e.g. \"Light-touch survey completed by users of facility X\""
    )
    full_description = models.TextField(
        help_text=
        "This is a thorough description used to fully explain the purpose behind the surveys of this type."
    )
    public = models.BooleanField(default=False)
    poster_template = models.CharField(
        max_length=1000,
        blank=True,
        null=True,
        help_text=
        "Path of template from the application root. If it's blank, poster links won't be generated for this survey type."
    )
    has_handout = models.BooleanField(default=False)

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name


class Survey(models.Model):
    name = models.CharField(max_length=200, unique=True)
    cycle = models.ForeignKey(Cycle, related_name="surveys")
    type = models.ForeignKey(SurveyType)
    form = jsonfield.JSONField()
    map_to_form = jsonfield.JSONField(blank=True, null=True)

    def __getattribute__(self, attrname):
        attr = super(Survey, self).__getattribute__(attrname)
        if attrname in {'form', 'map_to_form'}:
            if attr:
                attr = XForm(attr)
        return attr

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    @property
    def programme(self):
        return self.cycle.programme

    def import_submissions(self):
        refresh_token = self.programme.kobo_refresh_token
        kobo = Kobo.from_refresh_token(refresh_token.token)
        refresh_token.token = kobo.refresh_token
        refresh_token.save()
        responses = kobo.get_responses(self.surveykoboproject.form_id)
        if self.form.get_by_path('facility'):
            facility_q_name = 'facility'
        elif self.form.get_by_path('site'):
            facility_q_name = 'site'
        else:
            raise Exception('No facility/site/location question')
        facility_crs = {}
        for crs in self.cycle_result_sets.all():
            facility_crs[crs.site_option_name] = crs
        responses = field_per_SATA_option(self.form, responses)
        responses = skipped_as_na(self.form, responses)
        for response in responses:
            try:
                obj = Submission.objects.get(uuid=response['_uuid'])
                obj.assert_answers_equal(response)
            except Submission.DoesNotExist:
                facility_name = response[facility_q_name]
                obj = Submission(
                    answers=response,
                    cycle_result_set=facility_crs[facility_name])
                obj.save()

    def get_submission_count(self):
        return Submission\
            .objects\
            .filter(cycle_result_set__survey__name=self.name)\
            .count()


class SurveyKoboProject(models.Model):
    survey = models.OneToOneField(
        Survey, on_delete=models.CASCADE, primary_key=True)
    # Kobo is deprecating projects so from this point on,
    # when we refer to a kobo project (a form and its submissions),
    # the formid field is the unique reference for the URLs
    # https://kc.kobotoolbox.org/api/v1/forms/69399?format=json (project)
    # https://kc.kobotoolbox.org/api/v1/forms/69399/form.json (the xform as json)
    # https://kc.kobotoolbox.org/api/v1/data/69399?format=json (the submissions)
    form_id = models.IntegerField(unique=True, null=False)


class UserKoboRefreshToken(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True)
    token = models.TextField(null=False, blank=False)


class ProgrammeKoboRefreshToken(models.Model):
    programme = models.OneToOneField(
        Programme,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="kobo_refresh_token")
    token = models.TextField(null=False, blank=False)


class CycleResultSet(models.Model):
    """
    An entity representing the data collection period for a given site
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
    site = models.ForeignKey(Site, related_name='cycle_result_sets')
    site_option_name = models.TextField()
    partner = models.ForeignKey(Partner, related_name='cycle_result_sets')
    # This is meant to allow identifying comparable CycleResultSets
    # which don't necessarily have exactly the same survey
    survey = models.ForeignKey(
        Survey, null=True, blank=True, related_name="cycle_result_sets")
    monitors = models.ManyToManyField(
        "Monitor",
        blank=True,
        help_text=
        "Only monitors for the current partner are shown. If you update the Partner you'll have to save and edit this Cycle Result Set again to see the available monitors."
    )
    funder = models.ForeignKey(
        Funder, null=True, blank=True, on_delete=models.SET_NULL)

    action_items = models.TextField(
        null=True,
        blank=True,
        help_text="Key challenges identified for improvement. Markdown allowed."
    )
    follow_up_date = models.DateField(
        null=True,
        blank=True,
        help_text="Date when follow up check was performed")
    follow_up = models.TextField(
        null=True,
        blank=True,
        help_text="Follow ups to key challenges. Markdown allowed.")
    published = models.BooleanField(
        null=False,
        blank=False,
        help_text=
        "Whether the results may be listed publicly with the assumption that it's somewhat validated",
        default=False)

    class Meta:
        unique_together = ('site', 'survey')
        ordering = ('site__name', 'partner__short_name')

    def __str__(self):
        return "%s <- %s (%s: %s)" % (self.site.name, self.partner.short_name,
                                      self.survey.type, self.survey.cycle)

    def end_date_cmp(a, b):
        return Cycle.end_date_cmp(a.survey.cycle, b.survey.cycle)

    def get_previous(self):
        result_sets = list(
            CycleResultSet.objects.filter(
                survey__cycle__end_date__lte=self.survey.cycle.start_date,
                site__exact=self.site,
                survey__type=self.survey.type,
                published=True).filter(~Q(pk=self.pk)).all())
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
            form, responses = self.get_survey()
            if responses:
                df = pandas.DataFrame(responses)
                self._summary = analysis.count_submissions(df)
            else:
                self._summary = {'male': 0, 'female': 0, 'total': 0}
        return self._summary

    def has_poster_attachment(self):
        return any(a.nature.name == 'poster' for a in self.attachments.all())

    def has_handout_attachment(self):
        return any(a.nature.name == 'handout' for a in self.attachments.all())

    def get_survey(self, map=True):
        """
        Returns the python structure representing the JSON of the survey form
        and the survey responses
        Maps group and question names to those expected by various things by
        default. Pass map=False to disable this.
        """
        form = self.survey.form
        responses = [s.answers for s in self.submissions.all()]
        if map:
            if self.survey.map_to_form:
                map_form(form, responses, self.survey.map_to_form)
                form = self.survey.map_to_form
            simplify_perf_group(form, responses)
        return form, responses

    def has_monitoring_outputs(self):
        return any([
            self.has_poster_attachment(),
            self.has_handout_attachment(),
            self.action_items,
            self.follow_up,
            self.survey.type.poster_template,
            self.survey.type.has_handout,
        ])


class AttachmentNature(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class CycleResultSetAttachment(models.Model):
    cycle_result_set = models.ForeignKey(
        CycleResultSet, null=False, related_name='attachments')
    nature = models.ForeignKey(AttachmentNature, null=False)
    file = models.FileField(upload_to=attachment_filename, null=False)

    def __str__(self):
        return "%s -> %s (%s)" % (
            self.cycle_result_set,
            self.file.name,
            self.nature.name,
        )


class Submission(models.Model):
    answers = jsonfield.JSONField()
    uuid = models.TextField(unique=True)
    cycle_result_set = models.ForeignKey(
        CycleResultSet, null=True, blank=True, related_name="submissions")
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def save(self, *args, **kwargs):
        self.uuid = self.answers['_uuid']
        super(Submission, self).save(*args, **kwargs)

    def assert_answers_equal(self, remote_answers):
        """
        Raise an exception if any fields except _id and _submission_time differ
        """
        remote_copy = copy.copy(remote_answers)
        del remote_copy['_id']
        del remote_copy['_submission_time']
        remote_copy_json = json.dumps(remote_copy, sort_keys=True)

        local_copy = copy.copy(self.answers)
        del local_copy['_id']
        del local_copy['_submission_time']
        local_copy_json = json.dumps(local_copy, sort_keys=True)

        if local_copy_json != remote_copy_json:
            raise Exception("Same uuid but different values\n"
                            "Remote: %s\n\nDB: %s" %
                            (pprint.pformat(remote_copy),
                             pprint.pformat(local_copy)))

    def __str__(self):
        return "uuid=%s" % self.uuid


class ProgrammeStory(models.Model):
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, related_name='programme')
    title = models.CharField(max_length=100)
    description = models.TextField()
    slug = models.SlugField(max_length=200, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(ProgrammeStory, self).save(*args, **kwargs)


class ProgrammeStoryImage(models.Model):
    story = models.ForeignKey(
        ProgrammeStory, on_delete=models.CASCADE, related_name='story_image')
    caption = models.CharField(max_length=255)
    image = models.ImageField(upload_to='story/images')
    date = models.DateField(null=True)

    def __str__(self):
        return self.caption


class ProgrammeImage(models.Model):
    programme = models.ForeignKey(
        Programme, on_delete=models.CASCADE, related_name='program_image')
    caption = models.CharField(max_length=255)
    image = models.ImageField(upload_to='programme/images/')
    date = models.DateField(null=True)

    def __str__(self):
        return self.caption
