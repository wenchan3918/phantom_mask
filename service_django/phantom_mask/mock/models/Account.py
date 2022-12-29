from django.db import models
from django_mock_queries.query import MockSet, MockModel


class Account(models.Model):
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Account'

    name = models.CharField(verbose_name='Name',
                            max_length=255, )

    def __str__(self):
        return self.name

    @classmethod
    def get_mock_qs(cls):
        qs = MockSet(
            MockModel(id=1, name="kevin"),
            MockModel(id=2, name="David"),
        )
        return qs
