from django.core.management.base import BaseCommand
from Cashback.views import save_cashbacks

class Command(BaseCommand):
    help = 'Updates cashbacks'

    def handle(self, *args, **kwargs):
        save_cashbacks()