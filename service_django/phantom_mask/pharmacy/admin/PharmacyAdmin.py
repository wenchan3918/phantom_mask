from django.contrib.admin import ModelAdmin
from django.utils.safestring import mark_safe

from pharmacy.models import PurchaseHistory, Mask, PharmacyMask, OpeningHour
from django.contrib import admin


class OpeningHourInline(admin.TabularInline):
    verbose_name = 'Opening Hours'
    verbose_name_plural = 'Opening Hours'
    model = OpeningHour
    extra = 0

    fields = (
        'week',
        'open_at',
        'close_at',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by(
            'week',
            'open_at',
        )
        return queryset


class PharmacyMaskInline(admin.TabularInline):
    verbose_name = 'Masks'
    verbose_name_plural = 'Masks'
    model = PharmacyMask
    extra = 0

    fields = (
        'mask',
        'price',
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.order_by(
            'mask__name',
        )
        return queryset


class PharmacyAdmin(ModelAdmin):
    list_display = (
        'name',
        'cash_balance_',
        'purchase_history_count_',
        'opening_hours_',
        'mask_products_',
    )
    inlines = [
        OpeningHourInline,
        PharmacyMaskInline,
    ]

    @admin.display(description='Cash balance')
    def cash_balance_(self, obj):
        return f'${obj.cash_balance}'

    @admin.display(description='Purchase History Count')
    def purchase_history_count_(self, obj):
        return PurchaseHistory.objects.filter(pharmacy_mask__pharmacy=obj).count()

    @admin.display(description='Opening Hours')
    def opening_hours_(self, obj):
        opening_hours = []

        for opening_hour in OpeningHour.objects.filter(pharmacy=obj).order_by('week', 'open_at'):
            week = opening_hour.get_week_display()
            open_at = opening_hour.open_at.strftime('%H:%M')
            end_at = opening_hour.close_at.strftime('%H:%M')
            opening_hours.append(f'<li>{week}, {open_at} ~ {end_at}</li>')

        return mark_safe(f'<ol>{"".join(opening_hours)}</ol>')

    @admin.display(description='Masks')
    def mask_products_(self, obj):
        mask_products = []

        for product in PharmacyMask.objects.filter(pharmacy=obj).order_by('mask__name'):
            mask_products.append(
                f'<li>{product.mask.name} - ${product.price} - <b>mask_product_id:{product.id}</b></li>')

        return mark_safe(f'<ol>{"".join(mask_products)}</ol>')

    def get_queryset(self, request):
        return super().get_queryset(request).order_by('name')
