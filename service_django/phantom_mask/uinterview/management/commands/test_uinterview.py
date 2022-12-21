from django.core.management.base import BaseCommand
from django.db import connection

from uinterview.colors import colors
from uinterview.models import Delivery, Email, Employee, Product, Department, Movie, Account


# python manage.py test_uinterview
class Command(BaseCommand):
    help = '執行考題單元測試'

    cases = [
        Delivery.test_case_1,  # case 1
        Delivery.test_case_1_2,  # case 2

        Email.test_case_1,  # case 3
        Email.test_case_1_2,  # case 4

        Employee.test_case_1,  # case 5
        Employee.test_case_1_2,  # case 6

        Employee.test_case_2,  # case 7
        Employee.test_case_2_2,  # case 8

        Product.test_case_1,  # case 9
        Product.test_case_1_2,  # case 10

        Department.test_case_1,  # case 11
        Department.test_case_1_2,  # case 12

        Movie.test_case_1,  # case 13
        Movie.test_case_1_2,  # case 14

        Movie.test_case_2,  # case 15
        Movie.test_case_2_2,  # case 16

        Account.test_case_1,  # case 17
    ]

    def add_arguments(self, parser):
        parser.add_argument('--case', type=int, nargs='?', default=-1)
        parser.add_argument('--show_sql', type=int, nargs='?', default=0)

    def handle(self, *args, **options):
        case = options['case']
        if case not in range(1, len(self.cases) + 1):
            for case in self.cases:
                case(colors.fg.green)
        else:
            self.cases[case - 1](colors.fg.green)

        if options['show_sql'] == 1:
            print('\n************************************Executed SQL************************************')
            for idx, sql in enumerate(connection.queries):
                print(f'run {idx + 1}:', sql['sql'])
