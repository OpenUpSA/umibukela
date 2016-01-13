import os
import uuid

from django.db import models

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
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Province(models.Model):

    code = models.CharField(max_length=2, primary_key=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Partner(models.Model):
    short_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, primary_key=True)
    full_name = models.CharField(max_length=200)
    physical_address = models.CharField(max_length=200)
    province = models.ForeignKey(Province, null=True)
    contact_person = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=200)
    sector = models.ForeignKey(Sector, null=True)
    intro_title = models.CharField(max_length=200)
    intro_statement = models.TextField(max_length=200)
    intro_image = models.ImageField(upload_to=image_filename, null=True, blank=True)
    context_quote = models.CharField(max_length=200)
    context_statement = models.TextField(max_length=200)
    context_image = models.ImageField(upload_to=image_filename, null=True, blank=True)

    def __str__(self):
        return "[ID: %s] %s" % (self.slug, self.short_name)
