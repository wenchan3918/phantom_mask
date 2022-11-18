import datetime

# 教學https://q1mi.github.io/Django-REST-framework-documentation/api-guide/authentication_zh/
# swagger 參數設定 https://zoejoyuliao.medium.com/%E8%87%AA%E5%AE%9A%E7%BE%A9-drf-yasg-%E7%9A%84-swagger-%E6%96%87%E6%AA%94-%E4%BB%A5-get-post-%E6%AA%94%E6%A1%88%E4%B8%8A%E5%82%B3%E7%82%BA%E4%BE%8B-eeecd922059b

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication'
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': 'pharmacy.pagination.StandardResultsSetPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
}

# django-rest-auth
REST_USE_JWT = True
# REST_USE_JWT = False

REST_SESSION_LOGIN = False
# REST_SESSION_LOGIN = True

OLD_PASSWORD_FIELD_ENABLED = True
REST_AUTH_SERIALIZERS = {
    'JWT_SERIALIZER': 'core.serializers.JWTSerializer',
}

# django-rest-framework-jwt
# JWT_AUTH = {
#     # 'JWT_SECRET_KEY': '',  # default SECRET_KEY
#     'JWT_PAYLOAD_HANDLER': 'core.auth.default_jwt_payload_handler',
#     'JWT_AUTH_HEADER_PREFIX': 'Bearer',
#     'JWT_EXPIRATION_DELTA': datetime.timedelta(days=62),  # 2 months
# }
