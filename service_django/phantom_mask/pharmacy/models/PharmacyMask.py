from django.db import models


class PharmacyMask(models.Model):
    class Meta:
        verbose_name = "Pharmacy's Mask"
        verbose_name_plural = "Pharmacy's Mask"
        unique_together = ("pharmacy", "mask", "number_of_sales",)

    pharmacy = models.ForeignKey('Pharmacy',
                                 verbose_name='Pharmacy',
                                 on_delete=models.CASCADE, )

    mask = models.ForeignKey('Mask',
                             verbose_name='Mask',
                             on_delete=models.CASCADE, )

    number_of_sales = models.IntegerField(verbose_name='Number of sales',
                                          blank=True,
                                          default=1, )

    price = models.FloatField(verbose_name='Price',
                              blank=True,
                              db_index=True,
                              default=0, )

    stock_quantity = models.IntegerField(verbose_name='Stock quantity',
                                         blank=True,
                                         default=100, )

    def __str__(self):
        return f'{self.pharmacy} - {self.mask}'
