"""ameisen_an_die_macht URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from rest_framework import routers
from member_map.views import DiscordUserViewSet, UserMapView


# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'discord-users', DiscordUserViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('', UserMapView.as_view(), name='home'),
    path('impressum', TemplateView.as_view(template_name="impressum.html"), name='impressum'),
    path('datenschutz', TemplateView.as_view(template_name="datenschutz.html"), name='datenschutz'),
    path('nutzungsbedingungen', TemplateView.as_view(template_name="nutzungsbedingungen.html"), name='nutzungsbedingungen'),
    path('unterstützen', TemplateView.as_view(template_name="unterstuetzen.html"), name='unterstuetzen'),
]
