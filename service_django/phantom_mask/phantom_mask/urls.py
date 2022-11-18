"""phantom_mask URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from django.urls import re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from phantom_mask.AdminSite import admin_site

schema_view = get_schema_view(
    openapi.Info(
        title="Phantom Mask API",
        default_version='v1',
        description="Building a backend service and a database for a pharmacy platform",
        terms_of_service="N/A",
        contact=openapi.Contact(email="wenchan3918@gmail.com"),
        # license=openapi.License(name="BSD License"),
    ),
    public=True,
    url="https://mask.langgo.app/swagger/",
    # permission_classes=(permissions.AllowAny,),
    permission_classes=(permissions.IsAuthenticated,),
    authentication_classes=(TokenAuthentication, SessionAuthentication)
)

urlpatterns = [
    path('api/', include('pharmacy.urls')),
    path('admin/', admin_site.urls),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui', ),
    re_path(r'^doc/$', schema_view.with_ui('redoc', cache_timeout=None), name='schema-redoc-ui'),
]
