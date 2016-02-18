import umibukela.models as models
import sys

"""
import urllib2
import csv
import pandas as pd
from umibukela import models
import sys
from umibukela.importer import importer

url = ''
f = urllib2.urlopen(url)
r = csv.DictReader(f, delimiter=',', quotechar='"')
dicts = list(r)
for answers in dicts:
    submission = models.Submission(answers=answers)
    submission.save()

df = pd.DataFrame(dicts)
pd.unique(df.facility.ravel())
"""

def claim_submissions(field_name, submission_site_name, site_name, cycle_name):
    crs = models.CycleResultSet.objects.filter(
        site__name__iregex=site_name, cycle__name__iregex=cycle_name)[0]
    submissions = models.Submission.objects.all()
    site_submissions = [s for s in submissions if (s.answers.get(field_name) == submission_site_name) and (s.cycle_result_set is None)]
    for submission in site_submissions:
        submission.cycle_result_set = crs
        submission.save()
        sys.stdout.write('.')
        sys.stdout.flush()
