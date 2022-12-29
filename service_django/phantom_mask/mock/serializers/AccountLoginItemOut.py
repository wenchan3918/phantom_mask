# import logging
from rest_framework import serializers

from mock.models import AccountLogin


class AccountLoginItemOut(serializers.ModelSerializer):
    login_date = serializers.SerializerMethodField(label='Login Date')

    class Meta:
        model = AccountLogin
        fields = (
            'login_date',
        )

    def get_login_date(self, obj):
        try:
            return obj.login_date.strftime("%Y-%m-%d %H:%M:%S")
        except Exception as e:
            print(str(e))
            return ""
