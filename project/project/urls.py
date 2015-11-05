"""project URL Configuration."""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('recipes.urls')),
    url(r'^accounts/', include('allaccess.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)))
