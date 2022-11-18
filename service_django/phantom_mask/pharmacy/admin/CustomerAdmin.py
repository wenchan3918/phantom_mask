from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from pharmacy.models import PurchaseHistory
from django.contrib import admin


class PurchaseHistoryInline(admin.TabularInline):
    verbose_name = 'Purchase History'
    verbose_name_plural = 'Purchase History'
    model = PurchaseHistory
    extra = 0

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    fields = (
        'pharmacy_mask',
        'transaction_amount',
        'transaction_date',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by(
            # 'pharmacy__name',
            # 'mask__name',
            '-transaction_date',
        )
        return queryset


class CustomerAdmin(ModelAdmin):
    list_display = (
        'name',
        'cash_balance_',
        'purchase_history_',
    )

    inlines = [PurchaseHistoryInline]

    @admin.display(description='Purchase History')
    def purchase_history_(self, obj):
        history_items = []
        queryset = PurchaseHistory.objects.filter(customer=obj).order_by('-transaction_date')
        # historys.append(
        #     f'<li> <b>Total:{queryset.count()}</b></li>')
        for history in queryset:
            content = f'''<li>{history.pharmacy_mask.pharmacy.name}, 
                              {history.pharmacy_mask.mask.name}
                              [<b>mask_product_id: {history.pharmacy_mask.id}, price: ${history.transaction_amount}</b>],  
                              {history.transaction_date}</li>'''
            history_items.append(content)
        return mark_safe(f'<ol>{"".join(history_items)}</ol>')

    @admin.display(description='Cash balance')
    def cash_balance_(self, obj):
        return f'${obj.cash_balance}'

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('name')
