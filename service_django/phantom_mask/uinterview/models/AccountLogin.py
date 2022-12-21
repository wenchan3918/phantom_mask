from django.db import models
from django.db.models import Case, When, Value

from uinterview import utils
from uinterview.colors import colors
from uinterview.models.EmployeeBonus import EmployeeBonus


class AccountLogin(models.Model):
    class Meta:
        verbose_name = 'Account Login'
        verbose_name_plural = 'Account Login'

    account = models.ForeignKey('Account',
                                verbose_name='Account',
                                related_name='account',
                                on_delete=models.CASCADE, )

    login_date = models.DateField(verbose_name='Login Date', )

    def __str__(self):
        return f'{self.account} at {self.login_date}'
