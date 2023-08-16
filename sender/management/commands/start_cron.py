from django.core.management import BaseCommand
from sender.cron import my_scheduled_job


class Command(BaseCommand):
    def handle(self, *args, **options):
        my_scheduled_job()