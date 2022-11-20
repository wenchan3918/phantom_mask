from django.db import models


class Pharmacy(models.Model):
    class Meta:
        verbose_name = 'Pharmacy'
        verbose_name_plural = 'Pharmacy'

    name = models.CharField(
        verbose_name="Pharmacy name",
        max_length=256, )

    cash_balance = models.FloatField(verbose_name='Cash balance',
                                     default=0,
                                     db_index=True, )

    def __str__(self):
        return self.name
