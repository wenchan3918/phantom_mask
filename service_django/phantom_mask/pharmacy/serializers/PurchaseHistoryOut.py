# import logging
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from pharmacy.models import Mask, PharmacyMask, PurchaseHistory
from pharmacy.serializers.PharmacyMaskOut import PharmacyMaskOut


class PurchaseHistoryOut(serializers.ModelSerializer):
    mask = serializers.SerializerMethodField(label='Mask info | 口罩資訊')
    transaction_date = serializers.SerializerMethodField(label='Transaction date | 交易日期')

    class Meta:
        model = PurchaseHistory
        fields = (
            # 'id',
            'mask',
            'transaction_amount',
            'transaction_date',
        )

    @swagger_serializer_method(serializer_or_field=PharmacyMaskOut(many=False))
    def get_mask(self, obj):
        return PharmacyMaskOut(obj.pharmacy_mask, many=False).data

    def get_transaction_date(self, obj):
        try:
            return obj.transaction_date.strftime("%Y-%m-%d %H:%M:%S")
        except:
            return ''
