"""project URL Configuration."""
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin # NOQA

urlpatterns = [
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('recipes.urls'))
]

if settings.TEST:
    from recipes.views.tests import SubstitutJasmineView
    urlpatterns += patterns('', url(r'^djangojs/', include('djangojs.urls')))
    urlpatterns += patterns('', url(r'^jasmine$', SubstitutJasmineView.as_view(), name='substitut_jasmine_view'))

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns('', url(r'^__debug__/', include(debug_toolbar.urls)))
