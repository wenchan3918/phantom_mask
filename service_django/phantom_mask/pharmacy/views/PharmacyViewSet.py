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
from pharmacy.views.PharmacyViewSetParameter import LIST_MANUAL_PARAMETERS, MARK_SEARCH_MANUAL_PARAMETERS, \
    CUSTOMER_SEARCH_MANUAL_PARAMETERS


class PharmacyViewSet(ViewSetUtils,
                      FilterMixin,
                      mixins.ListModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacyOut

    @swagger_auto_schema(
        tags=['Pharmacy'],
        operation_summary='Search Pharmacy | 搜尋藥局',
        operation_description=f'''
          ''',
        manual_parameters=LIST_MANUAL_PARAMETERS,
        responses={200: openapi.Response('ok', PharmacyOut(many=True))})
    def list(self, request, *args, **kwargs):
        """
        List all pharmacies open at a specific time and on a day of the week if requested.
        如果需要，列出在特定時間和一周中的某一天營業的所有藥房。

        List all pharmacies with more or less than x mask products within a price range.
        列出價格範圍內口罩產品多於或少於 x 件的所有藥店。

        Search for pharmacies or masks by name, ranked by relevance to the search term.
        按名稱搜索藥房或口罩，按與搜索詞的相關性排名。
        """
        week = self.get_week(request)
        open_at = self.get_open_at(request)
        close_at = self.get_close_at(request)
        name = self.get_name(request)
        mask_name = self.get_mask_name(request)
        min_price = self.get_min_price(request)
        max_price = self.get_max_price(request)

        queryset = Pharmacy.objects.filter()
        pharmacy_mask_queryset = PharmacyMask.objects.filter()
        opening_hour_queryset = OpeningHour.objects.filter(pharmacy=OuterRef('pk')).order_by('week', 'open_at')

        if week:
            opening_hour_queryset = opening_hour_queryset.filter(week=week)

        if open_at:
            opening_hour_queryset = opening_hour_queryset.filter(open_at__gte=open_at)

        if close_at:
            # TODO 需修正跨夜間時間，例如 營業時間為20:00 ~ 02:00，則需能查詢到 22:00 ~ 01:00 的資料
            opening_hour_queryset = opening_hour_queryset.filter(close_at__lte=close_at)

        if week or open_at or close_at:
            queryset = Pharmacy.objects.annotate(
                week=Subquery(opening_hour_queryset.values('week')[:1]),
                open_at=Subquery(opening_hour_queryset.values('open_at')[:1]),
                # close_at=Subquery(opening_hour_queryset.values('close_at')[:1]),
            ).filter(id__in=opening_hour_queryset.values('pharmacy_id'))

        if min_price:
            pharmacy_mask_queryset = pharmacy_mask_queryset.filter(price__gte=min_price)

        if max_price:
            pharmacy_mask_queryset = pharmacy_mask_queryset.filter(price__lte=max_price)

        if mask_name:
            pharmacy_mask_queryset = pharmacy_mask_queryset.filter(mask__name__contains=mask_name)
            queryset = queryset.filter(id__in=pharmacy_mask_queryset.values('pharmacy_id'))
            # TODO 口罩名稱搜尋有實作但無法達成以關聯性做排序

        # 以商店名稱作為搜索詞進行搜尋，並的相關性排名。
        if name:
            # TODO 需驗證rank的計算方式與SearchVector用法
            vector = SearchVector('name')
            query = SearchQuery(name)
            queryset = queryset.filter(name__contains=name)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        return self.response_have_page(queryset=queryset,
                                       serializer=PharmacyOut,
                                       request=request, )

    @swagger_auto_schema(
        tags=['Pharmacy'],
        operation_summary='Search Mask | 搜尋口罩',
        operation_description=f'''
          ''',
        manual_parameters=MARK_SEARCH_MANUAL_PARAMETERS,
        responses={200: openapi.Response('ok', MaskOut(many=True))})
    @action(methods=['GET'], detail=False, url_path='mask')
    def mask_search(self, request, *args, **kwargs):
        """
        List all masks sold by a given pharmacy, sorted by mask name or price.
        列出給定藥房銷售的所有口罩，按口罩名稱或價格排序。

        The total number of masks and dollar value of transactions within a date range.
        某個日期範圍內交易的口罩總數和美元價值。
        """

        pharmacy_id = self.get_pharmacy_id(request)
        min_price = self.get_min_price(request)
        max_price = self.get_max_price(request)
        start_date = self.get_start_date(request)
        end_date = self.get_end_date(request)
        ordering = self.get_ordering(request, 'price')
        is_desc = self.get_is_desc(request)

        pharmacy_mask_queryset = PharmacyMask.objects
        purchase_history_queryset = PurchaseHistory.objects

        if pharmacy_id:
            pharmacy_mask_queryset = pharmacy_mask_queryset.filter(pharmacy_id=pharmacy_id)

        if min_price:
            pharmacy_mask_queryset = pharmacy_mask_queryset.filter(price__gte=min_price)

        if max_price:
            pharmacy_mask_queryset = pharmacy_mask_queryset.filter(price__lte=max_price)

        if start_date:
            purchase_history_queryset = purchase_history_queryset.filter(transaction_date__gte=start_date)

        if end_date:
            purchase_history_queryset = purchase_history_queryset.filter(transaction_date__lte=end_date)

        queryset = Mask.objects.annotate(
            mark_price=Subquery(pharmacy_mask_queryset.values('price')[:1]),
            mark_name=Subquery(pharmacy_mask_queryset.values('mask__name')[:1]),
            # close_at=Subquery(opening_hour_queryset.values('close_at')[:1]),
        ).filter(id__in=pharmacy_mask_queryset.values('mask_id'))

        if start_date or end_date:
            queryset = queryset.filter(id__in=purchase_history_queryset.values('pharmacy_mask__mask__id'))

        if ordering == 'price':
            queryset = queryset.order_by('-mark_price' if is_desc else 'mark_price')
        elif ordering == 'sale_total_amount':
            queryset = queryset.order_by('-sale_total_amount' if is_desc else 'sale_total_amount')
        else:
            queryset = queryset.order_by('-mark_name' if is_desc else 'mark_name')

        # print("=queryset", queryset.query)
        return self.response_have_page(queryset=queryset,
                                       serializer=MaskOut,
                                       request=request,
                                       )

    @swagger_auto_schema(
        tags=['Pharmacy'],
        operation_summary='Search Customer | 搜尋顧客',
        operation_description=f'''
          ''',
        manual_parameters=CUSTOMER_SEARCH_MANUAL_PARAMETERS,
        responses={200: openapi.Response('ok', CustomerOut(many=True))})
    @action(methods=['GET'], detail=False, url_path='customer')
    def customer_search(self, request, *args, **kwargs):
        """
        The top x users by total transaction amount of masks within a date range.
        按某個日期範圍內的口罩總交易金額排名前 x 的顧客。
        """
        start_date = self.get_start_date(request)
        end_date = self.get_end_date(request)
        name = self.get_name(request)
        ordering = self.get_ordering(request, 'total_transaction_amount')
        is_desc = self.get_is_desc(request)

        queryset = Customer.objects.filter()
        purchase_history_queryset = PurchaseHistory.objects.filter(customer=OuterRef('pk'))

        if start_date:
            purchase_history_queryset = purchase_history_queryset.filter(transaction_date__gte=start_date)

        if end_date:
            purchase_history_queryset = purchase_history_queryset.filter(transaction_date__lte=end_date)

        total_transaction_amount = Subquery(
            purchase_history_queryset.annotate(
                total_transaction_amount=Func(F('transaction_amount'), function='SUM')).values(
                'total_transaction_amount')
        )
        queryset = queryset.annotate(
            total_transaction_amount=total_transaction_amount,
        ).filter(id__in=purchase_history_queryset.values('customer_id')).order_by('-total_transaction_amount')

        if name:
            vector = SearchVector('name')
            query = SearchQuery(name)
            queryset = queryset.filter(name__contains=name)
            queryset = queryset.annotate(rank=SearchRank(vector, query)).order_by('-rank')

        if ordering == 'total_transaction_amount':
            queryset = queryset.order_by('-total_transaction_amount' if is_desc else 'total_transaction_amount')
        else:
            queryset = queryset.order_by('-name' if is_desc else 'name')

        return self.response_have_page(queryset=queryset,
                                       serializer=CustomerOut,
                                       request=request,
                                       )

    @swagger_auto_schema(
        tags=['Pharmacy'],
        operation_summary='Buy Mask | 購買口罩',
        operation_description='''
        Test Data:
        mask_product_id can be found in [/admin/pharmacy/pharmacy/](https://mask.langgo.app/admin/pharmacy/pharmacy/).
        
          ```
          {
                "customer_name": "Ada Larson",
                "items": [
                    {
                        "mask_product_id": 1,
                        "num": 1  
                    },
                    {
                        "mask_product_id": 2,
                        "num": 1
                    }
                ]
            }
    ''',
        manual_parameters=[
        ],
        request_body=MaskProductOrderIn(many=True),
        responses={200: openapi.Response('ok', )})
    @action(methods=['POST'], detail=False, url_path='mask/order')
    def order(self, request, *args, **kwargs):
        """
        Process a user purchases a mask from a pharmacy, and handle all relevant data changes in an atomic transaction.
        處理使用者從藥房購買口罩，並處理原子事務中的所有相關數據更改。
        """
        orders = MaskProductOrderIn(data=request.data)
        orders.is_valid(raise_exception=True)
        orders.create()
        return self.response()
