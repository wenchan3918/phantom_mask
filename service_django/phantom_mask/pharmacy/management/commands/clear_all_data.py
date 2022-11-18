import json
import os

from django.core.management.base import BaseCommand

from pharmacy.models import Mask, Pharmacy, PharmacyMask, Customer, PurchaseHistory, OpeningHour


# python manage.py clear_all_data
class Command(BaseCommand):
    help = 'Clears the database.'

    def handle(self, *args, **options):
        PurchaseHistory.objects.all().delete()
        OpeningHour.objects.all().delete()
        PharmacyMask.objects.all().delete()
        Mask.objects.all().delete()
        Pharmacy.objects.all().delete()
        Customer.objects.all().delete()

        print('All data cleared.')
