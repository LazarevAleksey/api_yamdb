from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path('', include('reviews.urls')),
    path('admin/', admin.site.urls),
    path(
        'redoc/',
        TemplateView.as_view(template_name='redoc.html'),
        name='redoc'
    ),


    path('auth/', include('users.urls')),

    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),



]
