from django.db import models
from django.db.models import Case, When, Value

from uinterview import utils
from uinterview.colors import colors
from uinterview.models.EmployeeBonus import EmployeeBonus


class Student(models.Model):
    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Student'

    department = models.ForeignKey('Department',
                                   verbose_name='Department',
                                   related_name='department',
                                   on_delete=models.CASCADE, )

    name = models.CharField(verbose_name='Name',
                            max_length=255, )

    gender = models.CharField(verbose_name='Gender',
                              max_length=2, )

    def __str__(self):
        return f'{self.name}({self.gender})'

