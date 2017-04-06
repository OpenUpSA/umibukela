from django.core.management.base import BaseCommand
from umibukela.models import Survey


class Command(BaseCommand):
    help = 'Imports all submissions not yet imported for Cycles with this enabled.'

    def handle(self, *args, **options):
        for survey in Survey.objects.filter(cycle__auto_import=True):
            survey.import_submissions()
