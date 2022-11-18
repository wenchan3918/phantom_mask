from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Customer(models.Model):
    class Meta:
        verbose_name = 'Customer'
        verbose_name_plural = 'Customer'

    name = models.CharField(
        verbose_name="User name",
        unique=True,
        max_length=65)

    cash_balance = models.FloatField(verbose_name='Cash balance',
                                     default=0,
                                     validators=[MinValueValidator(0.0), MaxValueValidator(10000.0)],
                                     )

    def __str__(self):
        return self.name
