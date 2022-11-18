# import logging
from rest_framework import serializers

from pharmacy.models import Pharmacy, OpeningHour


class OpeningHourOut(serializers.ModelSerializer):
    week = serializers.SerializerMethodField(label='Week | 有營業的星期')
    open_at = serializers.SerializerMethodField(label='Open at | 開始營業時間')
    close_at = serializers.SerializerMethodField(label='Close at | 結束營業時間')

    class Meta:
        model = OpeningHour
        fields = (
            'id',
            'week',
            'open_at',
            'close_at',
        )

    def get_week(self, obj):
        return obj.get_week_display()

    def get_open_at(self, obj):
        try:
            return obj.open_at.strftime('%H:%M')
        except:
            return ""

    def get_close_at(self, obj):
        try:
            return obj.close_at.strftime('%H:%M')
        except:
            return ""
