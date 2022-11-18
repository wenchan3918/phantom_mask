from datetime import datetime

from django.db import models


class PurchaseHistory(models.Model):
    class Meta:
        verbose_name = 'Purchase History'
        verbose_name_plural = 'Purchase History'

    customer = models.ForeignKey('Customer',
                                 verbose_name='Customer',
                                 on_delete=models.CASCADE, )

    pharmacy_mask = models.ForeignKey('PharmacyMask',
                                      verbose_name="Pharmacy's mask",
                                      on_delete=models.CASCADE, )

    transaction_amount = models.FloatField(verbose_name='Transaction amount',
                                           db_index=True,
                                           default=0, )

    transaction_date = models.DateTimeField(verbose_name='Transaction date',
                                            db_index=True,
                                            default=datetime.now, )

# {
#     "pharmacyName": "Cool Pharmacy Names",
#     "maskName": "Cotton Kiss (black) (10 per pack)",
#     "transactionAmount": 43.82,
#     "transactionDate": "2021-01-07 16:24:34"
# },
#
#
