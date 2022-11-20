from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import F, OuterRef, Subquery, Func
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from phantom_mask.ViewSetUtils import ViewSetUtils
from pharmacy.mixins.FilterMixin import FilterMixin
from pharmacy.models import Mask, Customer, PurchaseHistory, PharmacyMask, OpeningHour
from pharmacy.models.Pharmacy import Pharmacy
from pharmacy.serializers.CustomerOut import CustomerOut
from pharmacy.serializers.MasKProductOrderIn import MaskProductOrderIn
from pharmacy.serializers.MaskOut import MaskOut
from pharmacy.serializers.PharmacyOut import PharmacyOut

LIST_MANUAL_PARAMETERS = [
    openapi.Parameter(
        name='week',
        in_=openapi.IN_QUERY,
        description="Week | 營業週。{'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thur': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}",
        enum=[1, 2, 3, 4, 5, 6, 7],
        default=1,
        format='int64',
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name='open_at',
        in_=openapi.IN_QUERY,
        description="Open at | 開始營業時間",
        enum=[
            '02:00',
            '08:00',
            '14:00',
        ],
        format='time',
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name='close_at',
        in_=openapi.IN_QUERY,
        description="Close at | 結束營業時間",
        enum=[
            '18:00',
            '19:00',
            '20:00',
        ],
        format='time',
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name='name',
        in_=openapi.IN_QUERY,
        description='Pharmacy Name | 藥局名稱。模糊搜尋',
        enum=[
            'point',
            'Care',
            'Health',
        ],
        format='string',
        required=False,
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name='mask_name',
        in_=openapi.IN_QUERY,
        description='Mask Name | 口罩名稱 。模糊搜尋',
        enum=[
            'Masquerade',
            'True Barrier',
            'Cotton Kiss',
        ],
        format='string',
        required=False,
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name='min_price',
        in_=openapi.IN_QUERY,
        description='Min sale price | 篩選高於於此銷售價格',
        format='int64',
        enum=[
            5,
            10,
            30,
        ],
        required=False,
        type=openapi.TYPE_NUMBER,
    ),

    openapi.Parameter(
        name='max_price',
        in_=openapi.IN_QUERY,
        description='Max sale price | 篩選低於此銷售價格',
        format='int64',
        enum=[
            40,
            60,
            80,
        ],
        required=False,
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name='ordering',
        in_=openapi.IN_QUERY,
        description='Order field | 指定排序欄位',
        format='string',
        enum=[
            "price",
            "name",
        ],
        default="price",
        required=False,
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name='is_desc',
        in_=openapi.IN_QUERY,
        description='Order field use desc sort | 排序欄位是否以降序排列',
        format='boolean',
        enum=[
            "true",
            "false",
        ],
        default="true",
        required=False,
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        name='fields',
        in_=openapi.IN_QUERY,
        description='Display fields | 顯示欄位',
        enum=[
            "id,name",
            "id,name,cash_balance",
            "id,name,cash_balance,opening_hours",
            "id,name,cash_balance,opening_hours,mask_products",
            "id,name,cash_balance,opening_hours,mask_products,sales_history",
        ],
        format='string',
        type=openapi.TYPE_STRING,
        default="id,name,cash_balance,opening_hours,mask_products,sales_history",
        required=False,
    ),
]
MARK_SEARCH_MANUAL_PARAMETERS = [
    openapi.Parameter(
        name='pharmacy_id',
        in_=openapi.IN_QUERY,
        description='Pharmacy ID | 藥局 ID。 Get from `/pharmacy/` API',
        format='int64',
        enum=[
            41,
            51,
            57,
        ],
        required=False,
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name='min_price',
        in_=openapi.IN_QUERY,
        description='Min sale price | 搜尋價格高於此銷售價格',
        format='int64',
        enum=[
            5,
            10,
            30,
        ],
        required=False,
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name='max_price',
        in_=openapi.IN_QUERY,
        description='Max sale price | 搜尋價格低於此銷售價格',
        format='int64',
        enum=[
            40,
            60,
            80,
        ],
        required=False,
        type=openapi.TYPE_NUMBER,
    ),
    openapi.Parameter(
        name='ordering',
        in_=openapi.IN_QUERY,
        description='Order field | 指定排序欄位',
        format='string',
        enum=[
            "price",
            "sale_total_amount",
            "name",
        ],
        default="price",
        required=False,
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name='is_desc',
        in_=openapi.IN_QUERY,
        description='Order field use desc sort | 排序欄位是否以降序排列',
        format='boolean',
        enum=[
            "true",
            "false",
        ],
        default="true",
        required=False,
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        name='start_date',
        in_=openapi.IN_QUERY,
        description='Start date | 搜尋開始日期。Format: YYYY-MM-DD',
        default='2021-01-11',
        format='date',
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name='end_date',
        in_=openapi.IN_QUERY,
        description='End date | 搜尋結束日期。Format: YYYY-MM-DD',
        default='2021-01-12',
        format='date',
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name='fields',
        in_=openapi.IN_QUERY,
        description='Display fields | 顯示欄位',
        enum=[
            "name",
            "name,sale_pharmacies",
            "name,sale_pharmacies,sale_total_amount",
            "name,sale_pharmacies,sale_total_amount,sale_total_transaction_amount",
            "name,sale_pharmacies,sale_total_amount,sale_total_transaction_amount,purchase_history",

        ],
        format='string',
        type=openapi.TYPE_STRING,
        default="name,sale_pharmacies,sale_total_amount",
        required=False,
    ),
]
CUSTOMER_SEARCH_MANUAL_PARAMETERS = [
    openapi.Parameter(
        name='start_date',
        in_=openapi.IN_QUERY,
        description='Start date | 搜尋開始日期。Format: YYYY-MM-DD',
        default='2021-01-11',
        format='date',
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name='end_date',
        in_=openapi.IN_QUERY,
        description='End date | 搜尋結束日期。Format: YYYY-MM-DD',
        default='2021-01-12',
        format='date',
        type=openapi.TYPE_STRING,
        required=False,
    ),
    openapi.Parameter(
        name='name',
        in_=openapi.IN_QUERY,
        description='Customer Name | 客戶姓名',
        enum=[
            'Timothy',
            'Bush',
            'Lester',
        ],
        format='string',
        required=False,
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name='ordering',
        in_=openapi.IN_QUERY,
        description='Order field | 指定排序欄位',
        format='string',
        enum=[
            "total_transaction_amount",
            "name",
        ],
        default="price",
        required=False,
        type=openapi.TYPE_STRING,
    ),
    openapi.Parameter(
        name='is_desc',
        in_=openapi.IN_QUERY,
        description='Order field use desc sort | 排序欄位是否以降序排列',
        format='boolean',
        enum=[
            "true",
            "false",
        ],
        default="true",
        required=False,
        type=openapi.TYPE_BOOLEAN,
    ),
    openapi.Parameter(
        name='fields',
        in_=openapi.IN_QUERY,
        description='Display fields | 顯示欄位',
        enum=[
            "id,name",
            "id,name,total_transaction_amount",
            "id,name,total_transaction_amount,purchase_history",
        ],
        format='string',
        type=openapi.TYPE_STRING,
        default='id,name,total_amount',
        required=False,
    ),
]
