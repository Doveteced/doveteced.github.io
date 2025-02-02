"""
URL configuration for dovetecenterprises project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from re import DEBUG
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from home.views import login_view


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('app.urls'))),  # Include app URLs
    path('articles/', include('home.urls')),  # Include articles homepage app URLs
    path('api/', include('home.urls_api')),  # Include home app URLs
    path('adverts/', include('adverts.urls')),  # Include adverts app URLs
    path('accounts/login/', login_view, name='login_view'),  # Include login view
    path('froala_editor/', include('froala_editor.urls')),  # Include Froala editor URLs
    path('shop/', include('shop.urls')),  # Include shop app URLs
    path('community/', include('community.urls')),  # Include community app URLs
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

