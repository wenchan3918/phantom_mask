from django.db import models

WEEK_MONDAY = 1
WEEK_TUESDAY = 2
WEEK_WEDNESDAY = 3
WEEK_THURSDAY = 4
WEEK_FRIDAY = 5
WEEK_SATURDAY = 6
WEEK_SUNDAY = 7
WEEK_CHOICES = (
    (WEEK_MONDAY, 'MONDAY'),
    (WEEK_TUESDAY, 'TUESDAY'),
    (WEEK_WEDNESDAY, 'WEDNESDAY'),
    (WEEK_THURSDAY, 'THURSDAY'),
    (WEEK_FRIDAY, 'FRIDAY'),
    (WEEK_SATURDAY, 'SATURDAY'),
    (WEEK_SUNDAY, 'SUNDAY'),
)

WEEK_DICT = dict(WEEK_CHOICES)

SHORT_WEEK_DICT = {
    'Mon': 1,
    'Tue': 2,
    'Wed': 3,
    'Thur': 4,
    'Fri': 5,
    'Sat': 6,
    'Sun': 7,
}


class OpeningHour(models.Model):
    class Meta:
        verbose_name = 'Opening Hours'
        verbose_name_plural = 'Opening Hours'

    pharmacy = models.ForeignKey('Pharmacy',
                                 verbose_name='Pharmacy',
                                 on_delete=models.CASCADE, )

    week = models.SmallIntegerField(verbose_name='Week',
                                    db_index=True,
                                    choices=WEEK_CHOICES, )

    open_at = models.TimeField(verbose_name='Open at',
                               db_index=True,)

    close_at = models.TimeField(verbose_name='Close at',
                                db_index=True,)

    def get_week_display(self):
        return WEEK_DICT[self.week]
