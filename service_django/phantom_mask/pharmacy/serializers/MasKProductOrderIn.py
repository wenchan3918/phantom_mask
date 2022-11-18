# import logging
from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from pharmacy.models import Mask, PharmacyMask, Customer, PurchaseHistory
from pharmacy.serializers.MasKProductOrderItemIn import MasKProductOrderItemIn


class MaskProductOrderIn(serializers.ModelSerializer):
    items = serializers.ListSerializer(child=MasKProductOrderItemIn())

    class Meta:
        model = PharmacyMask
        fields = (
            'items',
        )

    def create(self):

        with transaction.atomic():
            for item in self.validated_data['items']:
                # 建立新訂單
                num = item['num']
                customer = item['customer_name']
                pharmacy_mask = item['mask_product_id']
                order = PurchaseHistory()
                order.customer = customer
                order.pharmacy_mask = pharmacy_mask
                order.transaction_amount = round(num * pharmacy_mask.price, 2)
                order.transaction_date = datetime.now()
                # print("+order.transaction_amount", order.transaction_amount, order.transaction_date)
                order.save()

                # 顧客餘額扣除
                last_cash_balance = customer.cash_balance
                customer.cash_balance = round(customer.cash_balance - order.transaction_amount, 2)

                if customer.cash_balance < 0:
                    raise serializers.ValidationError(
                        f"Customer cash balance is not enough. {customer}'s cash balance is ${last_cash_balance}.")
                order.customer.save()

                # 藥局餘額增加
                pharmacy_mask.pharmacy.cash_balance = round(
                    pharmacy_mask.pharmacy.cash_balance + order.transaction_amount, 2)
                pharmacy_mask.pharmacy.save()

    # num -= self.validated_data['num']
    # self.phantom_mask.save()
    #
    # self.customer.total_transaction_amount += self.phantom_mask.price * self.validated_data['num']
    # self.customer.save()
