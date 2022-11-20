# import logging
from django.db.models import Sum
from drf_queryfields import QueryFieldsMixin
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from pharmacy.mixins.FilterMixin import FilterMixin
from pharmacy.models import Mask, PharmacyMask, PurchaseHistory
from pharmacy.serializers.PharmacyMaskOut import PharmacyMaskOut
from pharmacy.serializers.PurchaseHistoryOut import PurchaseHistoryOut


class MaskOut(FilterMixin,
              QueryFieldsMixin,
              serializers.ModelSerializer):
    sale_pharmacies = serializers.SerializerMethodField(label='Sale pharmacies | 有販售口罩的藥局')
    sale_total_amount = serializers.SerializerMethodField(label='Sale total amount | 販售總數量')
    sale_total_transaction_amount = serializers.SerializerMethodField(
        label='Sale total transaction amount | 販售總金額')
    purchase_history = serializers.SerializerMethodField(label='Purchase history | 購買紀錄')

    class Meta:
        model = Mask
        fields = (
            'name',
            'sale_pharmacies',
            'sale_total_amount',
            'sale_total_transaction_amount',
            'purchase_history',
        )

    def get_sale_total_amount(self, mask):
        return self._get_purchase_history_queryset(mask).count()

    def get_sale_total_transaction_amount(self, mask):
        try:
            queryset = self._get_purchase_history_queryset(mask)
            return round(queryset.aggregate(total_amount=Sum('transaction_amount'))['total_amount'], 2)
        except:
            return 0

    @swagger_serializer_method(serializer_or_field=PurchaseHistoryOut(many=True))
    def get_purchase_history(self, mask):
        queryset = self._get_purchase_history_queryset(mask)
        return PurchaseHistoryOut(queryset, many=True).data

    @swagger_serializer_method(serializer_or_field=PharmacyMaskOut(many=True))
    def get_sale_pharmacies(self, mask):
        queryset = self._get_pharmacy_mask_queryset(mask)
        return PharmacyMaskOut(queryset, many=True).data

    def _get_pharmacy_mask_queryset(self, mask):
        request = self.context.get('request')
        pharmacy_id = self.get_pharmacy_id(request)
        min_price = self.get_min_price(request)
        max_price = self.get_max_price(request)
        queryset = PharmacyMask.objects.filter(mask=mask).order_by('price')

        if pharmacy_id:
            queryset = queryset.filter(pharmacy_id=pharmacy_id)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def _get_purchase_history_queryset(self, mask):
        request = self.context.get('request')
        start_date = self.get_start_date(request)
        end_date = self.get_end_date(request)

        queryset = PurchaseHistory.objects.filter(pharmacy_mask__mask=mask)

        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)

        return queryset
