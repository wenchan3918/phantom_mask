from django.urls import include, path
from rest_framework import routers

from mock import views

router = routers.SimpleRouter()
router.register(r'account', views.MockAccountViewSet)

urlpatterns = [
    path(r'mock/', include(router.urls)),
]
