from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class BasePageNumberPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        next_link = self.get_next_link()
        if next_link is None:
            next_link = ""

        previous = self.get_previous_link()
        if previous is None:
            previous = ""

        return Response({
            'next': next_link,
            'previous': previous,
            'count': self.page.paginator.count,
            'results': data,
        })


class LargeResultsSetPagination(BasePageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 200


class StandardResultsSetPagination(BasePageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100
