# import logging
from drf_queryfields import QueryFieldsMixin
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from pharmacy.mixins.FilterMixin import FilterMixin
from pharmacy.models import Customer, PurchaseHistory
from pharmacy.serializers.PurchaseHistoryOut import PurchaseHistoryOut


class CustomerOut(FilterMixin,
                  QueryFieldsMixin,
                  serializers.ModelSerializer):
    id = serializers.SerializerMethodField(label='Customer ID | 顧客ID')
    name = serializers.SerializerMethodField(label='Customer name | 顧客名稱')
    total_transaction_amount = serializers.SerializerMethodField(label='Total transaction amount | 總交易金額')
    purchase_history = serializers.SerializerMethodField(label='Purchase history | 購買紀錄')

    class Meta:
        model = Customer
        fields = (
            'id',
            'name',
            'total_transaction_amount',
            'purchase_history',
        )

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_total_transaction_amount(self, obj):
        try:
            return round(obj.total_transaction_amount, 2)
        except:
            return 0

    @swagger_serializer_method(serializer_or_field=PurchaseHistoryOut(many=True))
    def get_purchase_history(self, obj):
        request = self.context.get('request')
        start_date = self.get_start_date(request)
        end_date = self.get_end_date(request)

        queryset = PurchaseHistory.objects.filter(customer_id=self.get_id(obj)).order_by('-transaction_date')

        if start_date:
            queryset = queryset.filter(transaction_date__gte=start_date)

        if end_date:
            queryset = queryset.filter(transaction_date__lte=end_date)

        # queryset = queryset[:3]
        return PurchaseHistoryOut(queryset, many=True).data
