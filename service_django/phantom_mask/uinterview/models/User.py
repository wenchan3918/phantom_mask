from django.db import models
from django.db.models import OuterRef, Func, Count, Subquery
from django.db.models.functions import Coalesce

from uinterview import utils
from uinterview.colors import colors
from uinterview.models import Student
from uinterview.models.EmployeeBonus import EmployeeBonus


class User(models.Model):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'User'

    name = models.CharField(verbose_name='Name',
                            max_length=255, )

    def __str__(self):
        return self.name
