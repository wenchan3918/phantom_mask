from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response


class ViewSetUtils(object):
    # filter_backends = (DjangoFilterBackend, OrderingFilter,)

    def response_have_page(self,
                           queryset=None,
                           serializer=None,
                           request=None,
                           status_=status.HTTP_200_OK):

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = serializer(page,
                                    many=True,
                                    context={'request': request}
                                    )

            return self.get_paginated_response(serializer.data)

        serializer = serializer(queryset,
                                many=True,
                                context={'request': request})
        return Response(serializer.data, status=status_)

    def response(self,
                 queryset=None,
                 serializer=None,
                 data=None,
                 status_=status.HTTP_200_OK):
        if data is not None:
            return Response(data, status=status_)
        elif queryset:
            # print('===queryset',queryset)
            serializer = serializer(queryset,
                                    many=True)
            return Response(serializer.data, status=status_)
        else:
            return Response(status=status_)

    def response_detail(self,
                        queryset=None,
                        serializer=None,
                        status_=status.HTTP_200_OK):

        if queryset is None:
            return Response(data={},
                            status=status.HTTP_200_OK)

        serializer = serializer(queryset,
                                many=False,
                                context=dict(request=self.request))

        return Response(serializer.data, status=status_)
