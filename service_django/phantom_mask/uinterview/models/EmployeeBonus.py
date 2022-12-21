from django.db import models


class EmployeeBonus(models.Model):
    class Meta:
        verbose_name = 'Employee Bonus'
        verbose_name_plural = 'Employee Bonus'

    employee = models.ForeignKey('Employee',
                                 verbose_name='Employee',
                                 related_name='bonus',
                                 on_delete=models.SET_NULL,
                                 null=True, )

    bonus = models.FloatField(verbose_name='Bonus',
                              default=0,
                              db_index=True, )

