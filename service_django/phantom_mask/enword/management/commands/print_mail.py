import os

from django.core.management.base import BaseCommand


# python manage.py import_data
class Command(BaseCommand):
    help = ''
    current = os.path.dirname(os.path.abspath(__file__))

    def handle(self, *args, **options):
        mails = []
        with open(f'{self.current}/email.csv', 'r') as f:
            for row in f.readlines():
                if '.com' in row:
                    mails.append(row.strip())

        import random
        random.shuffle(mails)
        for mail in mails[:10]:
            print(mail)
