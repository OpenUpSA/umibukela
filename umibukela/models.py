from django.db import models


class Partner(models.Model):
    short_name = models.CharField(max_length=200)
    full_name = models.CharField(max_length=200)
    physical_address = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    telephone = models.CharField(max_length=200)
    email_address = models.EmailField(max_length=200)
    intro_title = models.CharField(max_length=200)
    intro_statement = models.TextField(max_length=200)
    intro_image = models.ImageField()
    context_quote = models.CharField(max_length=200)
    context_statement = models.TextField(max_length=200)
    context_image = models.ImageField()
