from rest_framework import serializers

from mock.models.Account import Account
from mock.models.AccountLogin import AccountLogin
from mock.serializers.AccountLoginItemOut import AccountLoginItemOut


class AccountItemOut(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(label='Name')
    login_history = serializers.SerializerMethodField(label='Login History')

    class Meta:
        model = Account
        fields = (
            'id',
            'name',
            'login_history'

        )

    def get_id(self, obj):
        return obj.id

    def get_name(self, obj):
        return obj.name

    def get_login_history(self, obj):
        request = self.context.get('request')
        use_mock = request.GET.get('use_mock', False)
        queryset = AccountLogin.get_mock_qs() if use_mock else AccountLogin.objects.filter(account=obj)
        serializer = AccountLoginItemOut(queryset,
                                         many=True,
                                         context={'request': request})

        return serializer.data
