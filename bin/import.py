import umibukela.models as models
import csv

# pd.unique(facility_coldf.facility.ravel())

crs = models.CycleResultSet.objects.filter(site__name__iregex=r'paarl', cycle__name__iregex=r'cycle 2')[0]

f = open('DOH-Citizen-Survey_2016_01_25_04_22_15.csv')
r = csv.DictReader(f, delimiter=',', quotechar='"')

for answer_sheet in r:
    submission = models.Submission(answers=answer_sheet)
    submission.save()

submissions = models.Submission.objects.all()

folweni_submissions = [submission for submission in submissions if submission.answers['facility'] == 'folweni']

for submission in folweni_submissions:
    submission.cycle_result_set = crs
    submission.save()
