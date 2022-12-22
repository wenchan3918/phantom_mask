# from core import views


# from django.conf.urls import include
from django.urls import include, path
from rest_framework import routers

from pharmacy import views

router = routers.SimpleRouter()
router.register(r'', views.PharmacyViewSet)

urlpatterns = [
    path(r'pharmacy/', include(router.urls)),
]
