from django.urls import include, path
from rest_framework import routers
from .views import signup, EmailTokenObtainPairView, UserViewSet, CategoryViewSet


v1_router = routers.DefaultRouter()

v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', EmailTokenObtainPairView.as_view(), name='token_obtain'),
]
