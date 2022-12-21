from datetime import datetime

from django.db import models


class Order(models.Model):
    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Order'

    product = models.ForeignKey('Product',
                                verbose_name="Product",
                                on_delete=models.CASCADE, )

    qty = models.SmallIntegerField(verbose_name='Quantity',
                                   default=0, )

    dispatch_date = models.DateTimeField(verbose_name='Dispatch date')
