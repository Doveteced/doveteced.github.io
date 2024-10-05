"""Article URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from os import stat
from django.contrib import admin
from django.urls import path , include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from home.views import login_view

urlpatterns = [
    path('' , include('home.urls')), # Include home app URLs
    path('api/' , include('home.urls_api')), # Include home app URLs
    path('adverts/', include('adverts.urls')),  # Include adverts app URLs
    path('accounts/login/', login_view, name='login_view'), # Include adverts app URLs
    path('admin/', admin.site.urls), # Include admin URLs
    path('froala_editor/',include('froala_editor.urls')), # Include Froala editor URLs
    path('shop/', include('shop.urls')), # Include shop app URLs
    path('community/', include('community.urls')), # Include community app URLs
]


if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)


urlpatterns += staticfiles_urlpatterns()