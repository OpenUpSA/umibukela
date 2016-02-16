import umibukela.models as models
import csv

# f = open('DOH-Citizen-Survey_2016_01_25_04_22_15.csv')
# r = csv.DictReader(f, delimiter=',', quotechar='"')
# pd.unique(facility_coldf.facility.ravel())
# for answer_sheet in answer_sheets:
#     submission = models.Submission(answers=answer_sheet)
#     submission.save()


def claim_submissions(field_name, submission_site_name, site_name, cycle_name):
    crs = models.CycleResultSet.objects.filter(
        site__name__iregex=site_name, cycle__name__iregex=cycle_name)[0]
    submissions = models.Submission.objects.all()
    site_submissions = [s for s in submissions if (s.answers.get(field_name) == submission_site_name) and (s.cycle_result_set is None)]
    for submission in site_submissions:
        submission.cycle_result_set = crs
        submission.save()
