import time

from pharmacy.models.OpeningHour import WEEK_DICT


class FilterMixin(object):
    def _get_open_at(self, request):
        try:
            open_at = request.GET.get('open_at', None)
            time.strptime(open_at, '%H:%M')
            return open_at
        except:
            return None

    def _get_close_at(self, request):
        try:
            close_at = request.GET.get('close_at', None)
            time.strptime(close_at, '%H:%M')
            return close_at
        except:
            return None

    def _get_start_date(self, request, default=None):
        try:
            start_date = request.GET.get('start_date', default)
            time.strptime(start_date, '%Y-%m-%d')
            return start_date
        except:
            return None

    def _get_end_date(self, request, default=None):
        try:
            end_date = request.GET.get('end_date', default)
            time.strptime(end_date, '%Y-%m-%d')
            return end_date
        except:
            return None

    def _get_week(self, request, default=0):
        try:
            week = int(request.GET.get('week', default))
            if week in WEEK_DICT.keys():
                return week
        except:
            pass

        return None

    def _get_name(self, request, default=None):
        return request.GET.get('name', default)

    def _get_mask_name(self, request, default=None):
        return request.GET.get('mask_name', default)

    def _get_pharmacy_id(self, request, default=None):
        try:
            return int(request.GET.get('pharmacy_id', default))
        except:
            return None

    def _get_ordering(self, request, default=None):
        return request.GET.get('ordering', default)

    def _get_is_desc(self, request):
        return request.GET.get('is_desc', 'false') in ['true', 'True', '1']

    def _get_min_price(self, request, default=None):
        try:
            return int(request.GET.get('min_price', default))
        except:
            return None

    def _get_max_price(self, request, default=None):
        try:
            return int(request.GET.get('max_price', default))
        except:
            return None
