from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import registration_email, token, UsersViewSet

router_v1 = DefaultRouter()

router_v1.register('users', UsersViewSet, basename='users')

urls = [
    path('email/', registration_email, name='registration'),
    path('token/', token, name='token')
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(urls))
]
