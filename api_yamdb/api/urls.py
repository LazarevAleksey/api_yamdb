from django.urls import include, path
from rest_framework import routers
from .views import signup, EmailTokenObtainPairView, UserViewSet,\
    CategoryViewSet, GenreViewSet, TitleViewSet, CommentViewSet, ReviewViewSet


v1_router = routers.DefaultRouter()


v1_router.register('categories', CategoryViewSet, basename='categories')
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('genres', GenreViewSet, basename='genres')
v1_router.register('titles', TitleViewSet, basename='titles')

# v1_router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet, basename='reviews')

v1_router.register(r'titles/((?P<title_id>\d+)/reviews|(?P<review_id>\d+))', ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments', CommentViewSet, basename='comments')
 

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path('v1/auth/signup/', signup),
    path('v1/auth/token/', EmailTokenObtainPairView.as_view(), name='token_obtain'),
]
