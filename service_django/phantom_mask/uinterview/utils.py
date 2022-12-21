# python manage.py test_push_task
import json
from tabulate import tabulate


def choice2html(choices):
    return json.dumps(dict(choices), indent=4, ensure_ascii=False).replace(' ', '&nbsp;').replace('\n', '<br>')


def dict2html(objects):
    return json.dumps(objects, indent=4, ensure_ascii=False).replace(' ', '&nbsp;').replace('\n', '<br>')


def text2html(text):
    return text.replace(' ', '').replace('\n', '<br>')


def choice2str(choices):
    return str(dict(choices))


def print_queryset(queryset, extra_headers=[], limit=30):
    headers = [x.name for x in queryset.model._meta.fields]
    headers.extend(extra_headers)
    rows = queryset.values_list(*headers)
    if limit is not None:
        rows = rows[:limit]

    size = len(headers)
    header_dividing = f'{"=====" * size} {queryset.model._meta.verbose_name} Table {"=====" * size}'
    print(header_dividing)
    print(tabulate(rows, headers))
    # print(f'{"=" * len(header_dividing)}')


def print_cursor(cursor):
    headers = [i[0] for i in cursor.description]
    print(tabulate(cursor.fetchall(), headers))


def prRed(prt):
    print(f"\033[91m{prt}\033[00m")


def prGreen(prt):
    print(f"\033[92m{prt}\033[00m")


def prYellow(prt):
    print(f"\033[93m{prt}\033[00m")


def prLightPurple(prt):
    print(f"\033[94m{prt}\033[00m")


def prPurple(prt):
    print(f"\033[95m{prt}\033[00m")


def prCyan(prt):
    print(f"\033[96m{prt}\033[00m")


def prLightGray(prt):
    print(f"\033[97m{prt}\033[00m")


def prBlack(prt):
    print(f"\033[98m{prt}\033[00m")


def prReset(prt):
    print(f"\033[0m{prt}\033[00m")
