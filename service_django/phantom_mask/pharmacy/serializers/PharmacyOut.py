# import logging
from drf_queryfields import QueryFieldsMixin
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from pharmacy.mixins.FilterMixin import FilterMixin
from pharmacy.models import Pharmacy, OpeningHour, PharmacyMask
from pharmacy.serializers.MasKProductOut import MaskProductOut
from pharmacy.serializers.OpeningHourOut import OpeningHourOut


class PharmacyOut(FilterMixin,
                  QueryFieldsMixin,
                  serializers.ModelSerializer):
    opening_hours = serializers.SerializerMethodField(label='Opening Hours | 營業與休息時間')
    mask_products = serializers.SerializerMethodField(label='Mask products | 販售的口罩產品')

    class Meta:
        model = Pharmacy
        fields = (
            'id',
            'name',
            'cash_balance',
            'opening_hours',
            'mask_products',
        )

    @swagger_serializer_method(serializer_or_field=OpeningHourOut(many=True))
    def get_opening_hours(self, obj):
        request = self.context.get('request')
        week = self._get_week(request)
        open_at = self._get_open_at(request)
        close_at = self._get_close_at(request)

        queryset = OpeningHour.objects.filter(pharmacy=obj)

        if week:
            queryset = queryset.filter(week=week)

        if open_at:
            queryset = queryset.filter(open_at__gte=open_at)

        if close_at:
            queryset = queryset.filter(close_at__lte=close_at)

        return OpeningHourOut(queryset, many=True).data

    @swagger_serializer_method(serializer_or_field=MaskProductOut(many=True))
    def get_mask_products(self, obj):
        request = self.context.get('request')
        mask_name = self._get_mask_name(request)
        min_price = self._get_min_price(request)
        max_price = self._get_max_price(request)

        queryset = PharmacyMask.objects.filter(pharmacy=obj)

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        if mask_name:
            queryset = queryset.filter(mask__name__contains=mask_name)

        return MaskProductOut(queryset, many=True).data
