from django.core.management.base import BaseCommand

from uinterview.models import Delivery, Email, Employee, Product, Department, Movie, Account


# python manage.py insert_uinterview_test_data
class Command(BaseCommand):
    help = 'Insert uinterview test data'

    def handle(self, *args, **options):
        # current = os.path.dirname(os.path.abspath(__file__))

        Email.insert_test_data()
        Delivery.insert_test_data()
        Employee.insert_test_data()
        Product.insert_test_data()
        Department.insert_test_data()
        Movie.insert_test_data()
        Account.insert_test_data()
