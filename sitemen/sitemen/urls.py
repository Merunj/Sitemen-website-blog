"""
URL configuration for sitemen project.

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
    1. Import the includes() function: from django.urls import includes, path
    2. Add a URL to urlpatterns:  path('blog/', includes('blog.urls'))
"""
from tkinter.font import names

from debug_toolbar.toolbar import debug_toolbar_urls
from django.contrib import admin
from django.urls import path, include
from django.views.decorators.cache import cache_page

from men.sitemaps import PostSitemap, CategorySitemap
from men.views import page_not_found
from django.conf.urls.static import static

from django.contrib.sitemaps.views import sitemap

from . import settings

sitemaps = {
    'posts': PostSitemap,
    'cats': CategorySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('men.urls')),
    path('users/', include('users.urls', namespace="users")),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('sitemap.xml', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')

] + debug_toolbar_urls()


handler404 = page_not_found

admin.site.site_header = "Панель администрирования"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)