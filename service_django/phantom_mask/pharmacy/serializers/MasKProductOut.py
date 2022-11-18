# import logging
from rest_framework import serializers

from pharmacy.models import Mask, PharmacyMask


class MaskProductOut(serializers.ModelSerializer):
    product_id = serializers.SerializerMethodField(label='Product ID | 販售的口罩產品ID')
    product_name = serializers.SerializerMethodField(label='Product name | 販售的口罩產品名稱')

    # pharmacy_name = serializers.SerializerMethodField()

    class Meta:
        model = PharmacyMask
        fields = (
            'product_id',
            'product_name',
            # 'pharmacy_name',
            'price',
        )

    def get_product_id(self, obj):
        return obj.id

    def get_product_name(self, obj):
        return obj.mask.name

    def get_pharmacy_name(self, obj):
        return obj.pharmacy.name or ''
