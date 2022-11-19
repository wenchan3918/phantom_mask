# import logging
from aioredis.commands import transaction
from rest_framework import serializers

from pharmacy.models import Mask, PharmacyMask, Customer


class MasKProductOrderItemIn(serializers.ModelSerializer):
    mask_product_id = serializers.IntegerField(label='Product ID | 販售的口罩產品ID')
    num = serializers.IntegerField(label='Order num | 口罩購買數量')

    phantom_mask = None

    class Meta:
        model = PharmacyMask
        fields = (
            'mask_product_id',
            'num',
        )

    def validate_mask_product_id(self, value):
        try:
            return PharmacyMask.objects.get(id=value)
            # print("==self.phantom_mask",self.phantom_mask)
        except:
            raise serializers.ValidationError('mask_product_id not exists.')

