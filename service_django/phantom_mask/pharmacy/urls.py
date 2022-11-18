# from core import views


from django.conf.urls import include, re_path
from rest_framework import routers

from pharmacy import views

router = routers.SimpleRouter()
router.register(r'', views.PharmacyViewSet)

urlpatterns = [
    re_path(r'^pharmacy/', include(router.urls)),
]
