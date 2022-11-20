import json
import os

from django.core.management.base import BaseCommand

from pharmacy.models import Mask, Pharmacy, PharmacyMask, Customer, PurchaseHistory
from pharmacy.models.OpeningHour import SHORT_WEEK_DICT, OpeningHour


# python manage.py import_data
class Command(BaseCommand):
    help = 'Import pharmacies and users data.'

    def handle(self, *args, **options):
        current = os.path.dirname(os.path.abspath(__file__))
        pharmacies = []
        users = []
        with open(f'{current}/pharmacies.json', 'r') as f:
            for item in json.loads(f.read()):
                pharmacies.append(item)

        with open(f'{current}/users.json', 'r') as f:
            for item in json.loads(f.read()):
                users.append(item)

        self.insert_mask(pharmacies)
        self.insert_pharmacy_and_opening_hour(pharmacies)
        self.insert_pharmacy_mask(pharmacies)

        self.insert_customer(users)
        self.insert_customer_purchase_history(users)

        # self.print_opening_hours(pharmacies)

    def insert_mask(self, pharmacies):
        for pharmacy in pharmacies:
            for mask in pharmacy['masks']:
                mask, created = Mask.objects.get_or_create(name=mask['name'])
                print(f'mask: {mask.name}, created: {created}')

    def insert_pharmacy_and_opening_hour(self, pharmacies):
        for _pharmacy in pharmacies:
            pharmacy, created = Pharmacy.objects.get_or_create(name=_pharmacy['name'])
            pharmacy.cash_balance = _pharmacy['cashBalance']
            pharmacy.save()

            OpeningHour.objects.filter(pharmacy_id=pharmacy).delete()
            for weeks, open_and_close_time in self.parse_weeks_and_times(_pharmacy['openingHours']):
                for week in weeks:
                    opening_hour = OpeningHour(pharmacy=pharmacy,
                                               open_at=open_and_close_time[0],
                                               close_at=open_and_close_time[1],
                                               week=week, )
                    opening_hour.save()

            print(f'pharmacy: {pharmacy.name}, created: {created}')

    def insert_pharmacy_mask(self, pharmacies):
        for _pharmacy in pharmacies:
            for mask in _pharmacy['masks']:
                # pharmacy_mask, created = PharmacyMask.objects.get_or_create(
                #     pharmacy=Pharmacy.objects.get(name=_pharmacy['name']),
                #     mask=Mask.objects.get(name=mask['name']),
                #     number_of_sales=1,
                # )
                # pharmacy_mask.price = mask['price']
                # print(f'pharmacy: {pharmacy_mask.pharmacy.name}, mask: {pharmacy_mask.mask.name}, created: {created}')

                pharmacy_mask = PharmacyMask()
                pharmacy_mask.pharmacy = Pharmacy.objects.get(name=_pharmacy['name'])
                pharmacy_mask.mask = Mask.objects.get(name=mask['name'])
                pharmacy_mask.number_of_sales = 1
                pharmacy_mask.price = mask['price']
                pharmacy_mask.save()

                print(f'pharmacy: {pharmacy_mask.id}, {pharmacy_mask.pharmacy.name}, mask: {pharmacy_mask.mask.name}')

    def insert_customer(self, users):
        for item in users:
            customer, created = Customer.objects.get_or_create(name=item['name'])
            customer.cash_balance = item['cashBalance']
            customer.save()
            print(f'user: {customer.name}, created: {created}')

    def insert_customer_purchase_history(self, users):
        PurchaseHistory.objects.all().delete()
        for item in users:
            for purchase in item['purchaseHistories']:
                customer = Customer.objects.get(name=item['name'])
                pharmacy = Pharmacy.objects.get(name=purchase['pharmacyName'])
                mask = Mask.objects.get(name=purchase['maskName'])
                history = PurchaseHistory.objects.create(
                    customer=customer,
                    pharmacy_mask=PharmacyMask.objects.get(pharmacy=pharmacy, mask=mask),
                    transaction_amount=purchase['transactionAmount'],
                    transaction_date=purchase['transactionDate'],
                )
                print(f'history: {history.id}')

    def parse_weeks_and_times(self, opening_hours):
        # 用/符號進行分割 Mon, Wed, Fri 08:00 - 12:00 / Tue, Thur 14:00 - 18:00
        results = []
        for item in opening_hours.split('/'):
            cols = item.strip().split(' ')  # [::-1]

            open_and_close_hours = []  # [open_at, close_at]
            open_and_close_hours.append(cols.pop())
            cols.pop()
            open_and_close_hours.append(cols.pop())
            open_and_close_hours.reverse()
            # open_and_close_hours = sorted(open_and_close_hours)

            weeks = []  # [1, 2, 3, 4, 5, 6, 7]
            if '-' in cols:  # 解析連續， ['Mon', '-', 'Fri', '08:00', '-', '17:00']
                for week_id in range(SHORT_WEEK_DICT[cols[0]], 1 + SHORT_WEEK_DICT[cols[-1]]):
                    weeks.append(week_id)
            else:  # 解析單一星期， ['Mon,', 'Wed,', 'Fri', '08:00', '-', '12:00']
                for week in cols:
                    weeks.append(SHORT_WEEK_DICT[week.replace(',', '')])

            # print(open_and_close_time, weeks, tmp)

            results.append((weeks, open_and_close_hours))

        return results

    def print_opening_hours(self, pharmacies):
        for pharmacy in pharmacies:
            # print(pharmacy['openingHours'])
            results = self.parse_weeks_and_times(pharmacy['openingHours'])
            print(results)

        """ results:
        [([1, 3, 5], ['12:00', '08:00']), ([2, 4], ['18:00', '14:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00']), ([6, 7], ['12:00', '08:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00']), ([6, 7], ['12:00', '08:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00']), ([6, 7], ['12:00', '08:00'])]
        [([5, 6, 7], ['02:00', '20:00'])]
        [([1, 3, 5], ['12:00', '08:00']), ([2, 4], ['18:00', '14:00'])]
        [([1, 3, 5], ['12:00', '08:00']), ([2, 4], ['18:00', '14:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00']), ([6, 7], ['12:00', '08:00'])]
        [([1, 2, 3], ['17:00', '08:00']), ([4, 6], ['02:00', '20:00'])]
        [([1, 2, 3], ['17:00', '08:00']), ([4, 6], ['02:00', '20:00'])]
        [([1, 2, 3], ['17:00', '08:00']), ([4, 6], ['02:00', '20:00'])]
        [([1, 3, 5], ['12:00', '08:00']), ([2, 4], ['18:00', '14:00'])]
        [([1, 3, 5], ['02:00', '20:00'])]
        [([1, 3, 5], ['02:00', '20:00'])]
        [([1, 2, 3, 4, 5], ['17:00', '08:00'])]
        [([1, 3, 5], ['02:00', '20:00'])]
        [([5, 6, 7], ['02:00', '20:00'])]
        """
