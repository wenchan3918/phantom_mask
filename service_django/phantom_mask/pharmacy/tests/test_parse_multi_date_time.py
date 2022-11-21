SHORT_WEEK_DICT = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thur': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}


def parse_weeks_and_times(opening_hours):
    # 以/符號進行分割 ['Mon', '-', 'Fri', '08:00', '-', '17:00', '/', 'Sat,', 'Sun', '08:00', '-', '12:00']
    # return opening_hours
    results = []
    for item in opening_hours.split('/'):
        cols = item.strip().split(' ')  # [::-1]

        open_and_close_hours = []  # [open_at, close_at]
        open_and_close_hours.append(cols.pop())
        cols.pop()
        open_and_close_hours.append(cols.pop())
        open_and_close_hours.reverse()
        # open_and_close_time = sorted(open_and_close_hours)

        weeks = []  # [1, 2, 3, 4, 5, 6, 7]
        if '-' in cols:  # 解析區段星期， ['Mon', '-', 'Fri']
            for week_id in range(SHORT_WEEK_DICT[cols[0]], 1 + SHORT_WEEK_DICT[cols[-1]]):
                weeks.append(week_id)
        else:  # 解析單一星期， ['Mon,', 'Wed,', 'Fri']
            for week in cols:
                weeks.append(SHORT_WEEK_DICT[week.replace(',', '')])

        results.append((weeks, open_and_close_hours))

    return results


rows = """
Mon, Wed, Fri 08:00 - 12:00 / Tue, Thur 14:00 - 18:00
Mon - Fri 08:00 - 17:00
Mon - Fri 08:00 - 17:00
Mon - Fri 08:00 - 17:00 / Sat, Sun 08:00 - 12:00
Mon - Fri 08:00 - 17:00
Mon - Fri 08:00 - 17:00 / Sat, Sun 08:00 - 12:00
Mon - Fri 08:00 - 17:00 / Sat, Sun 08:00 - 12:00
Fri - Sun 20:00 - 02:00
Mon, Wed, Fri 08:00 - 12:00 / Tue, Thur 14:00 - 18:00
Mon, Wed, Fri 08:00 - 12:00 / Tue, Thur 14:00 - 18:00
Mon - Fri 08:00 - 17:00 / Sat, Sun 08:00 - 12:00
Mon - Wed 08:00 - 17:00 / Thur, Sat 20:00 - 02:00
Mon - Wed 08:00 - 17:00 / Thur, Sat 20:00 - 02:00
Mon - Wed 08:00 - 17:00 / Thur, Sat 20:00 - 02:00
Mon, Wed, Fri 08:00 - 12:00 / Tue, Thur 14:00 - 18:00
Mon, Wed, Fri 20:00 - 02:00
Mon, Wed, Fri 20:00 - 02:00
Mon - Fri 08:00 - 17:00
Mon, Wed, Fri 20:00 - 02:00
Fri - Sun 20:00 - 02:00
""".strip().split('\n')

for row in rows:
    result = parse_weeks_and_times(row)
    print(result)
