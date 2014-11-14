from django.conf.urls import patterns, include, url

from django.contrib import admin
from OrderFood.views import hello, demo, direct_to_template

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Ordering.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^template/(?P<template_name>\w+)/$',direct_to_template),
    url(r'^hello/', hello),
    url(r'^demo/', demo),
)
