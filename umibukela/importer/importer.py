import umibukela.models as models

"""
import urllib

testfile = urllib.URLopener()
testfile.retrieve("https://doc-0g-5s-docs.googleusercontent.com/docs/securesc/ha0ro937gcuc7l7deffksulhg5h7mbp1/vvafdsti2u0snorfm7m36p1h97018hec/1455739200000/17237697729152170611/*/0B8yXDspOrgF9TDMzX3dCTkNPOWM?e=download", "SASSA-citizen-2014.csv")

https://drive.google.com/uc?export=download&id=0B8yXDspOrgF9NVJRZVdUSTBZdms

import csv
import pandas as pd
from umibukela import models

f = open('DOH-Citizen-Survey_2016_01_25_04_22_15.csv')
r = csv.DictReader(f, delimiter=',', quotechar='"')
dicts = list(r)
df = pd.DataFrame(dicts)
pd.unique(df.facility.ravel())
for answers in dicts:
    submission = models.Submission(answers=answers)
    submission.save()
"""

def claim_submissions(field_name, submission_site_name, site_name, cycle_name):
    crs = models.CycleResultSet.objects.filter(
        site__name__iregex=site_name, cycle__name__iregex=cycle_name)[0]
    submissions = models.Submission.objects.all()
    site_submissions = [s for s in submissions if (s.answers.get(field_name) == submission_site_name) and (s.cycle_result_set is None)]
    for submission in site_submissions:
        submission.cycle_result_set = crs
        submission.save()
