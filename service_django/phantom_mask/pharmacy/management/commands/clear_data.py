from django.core.management.base import BaseCommand

from pharmacy.models import Mask, Pharmacy, PharmacyMask, Customer, PurchaseHistory, OpeningHour


# python manage.py clear_data
class Command(BaseCommand):
    help = 'Clear the database.'

    def handle(self, *args, **options):
        for cls in [
            PurchaseHistory,
            OpeningHour,
            PharmacyMask,
            Mask,
            Pharmacy,
            Customer,
        ]:
            cls.objects.all().delete()

        print('All data cleared.')
