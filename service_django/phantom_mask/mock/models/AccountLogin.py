from datetime import date

from django.db import models
from django_mock_queries.query import MockSet, MockModel


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

    @classmethod
    def get_mock_qs(cls):
        qs = MockSet(
            MockModel(id=1, account_id=1, login_date=date.today(), ),
            MockModel(id=2, account_id=1, login_date=date.today(), ),
        )

        return qs
