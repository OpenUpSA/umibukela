from django.core.management.base import BaseCommand, CommandError
from umibukela.models import Cycle, Submission


class Command(BaseCommand):
    help = 'Imports all submissions not yet imported for Cycles with this enabled.'

    def handle(self, *args, **options):
        surveys = set()
        for cycle in Cycle.objects.filter(auto_import=True).all():
            for crs in cycle.cycle_result_sets.all():
                surveys.add(crs.survey)
        for survey in surveys:
            survey.import_submissions()
