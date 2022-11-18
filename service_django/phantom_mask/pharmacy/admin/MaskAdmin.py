from django.contrib.admin import ModelAdmin
from django.contrib import admin

from pharmacy.models import PurchaseHistory


class MaskAdmin(ModelAdmin):
    list_display = (
        'name',
        'purchase_history_count_',
    )

    @admin.display(description='Purchase History Count')
    def purchase_history_count_(self, obj):
        return PurchaseHistory.objects.filter(pharmacy_mask__mask=obj).count()

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('name')
