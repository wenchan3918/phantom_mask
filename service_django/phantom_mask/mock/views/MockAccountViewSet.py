from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny

from mock.models import Account
from mock.serializers.AccountItemOut import AccountItemOut
from phantom_mask.ViewSetUtils import ViewSetUtils
from pharmacy.mixins.FilterMixin import FilterMixin


class MockAccountViewSet(ViewSetUtils,
                         FilterMixin,
                         viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    queryset = Account.objects.all()
    serializer_class = AccountItemOut

    @swagger_auto_schema(
        tags=['Mack Account'],
        operation_summary='Account Info',
        operation_description='''
        
        ''',
        manual_parameters=[
        ],
        responses={200: openapi.Response('ok', AccountItemOut(many=False))})
    @action(methods=['GET'], detail=False, url_path='example')
    def example(self, request, *args, **kwargs):
        """
        後端定義好Schema後，再透過mack api的方式，讓前端可以先取得範例資料進行API串接
        """
        use_mock = request.GET.get('use_mock', False)
        queryset = Account.get_mock_qs() if use_mock else Account.objects.all()

        serializer = AccountItemOut(
            queryset.first(),
            many=False,
            context={'request': request},
        )
        return self.response(data=serializer.data)
