# import logging
from rest_framework import serializers

from pharmacy.models import Mask, PharmacyMask


class PharmacyMaskOut(serializers.ModelSerializer):
    pharmacy_id = serializers.SerializerMethodField(label='Pharmacy ID | 藥局ID')
    pharmacy_name = serializers.SerializerMethodField(label='Pharmacy name | 藥局名稱')
    mask_product_id = serializers.SerializerMethodField(label='Mask product ID | 販售的口罩產品ID')
    mask_product_name = serializers.SerializerMethodField(label='Mask product name | 販售的口罩產品名稱')

    class Meta:
        model = PharmacyMask
        fields = (
            'pharmacy_id',
            'pharmacy_name',
            'mask_product_id',
            'mask_product_name',
            'price',
        )

    def get_mask_product_id(self, obj):
        return obj.id

    def get_mask_product_name(self, obj):
        return obj.mask.name

    def get_pharmacy_id(self, obj):
        return obj.pharmacy.id

    def get_pharmacy_name(self, obj):
        return obj.pharmacy.name or ''
