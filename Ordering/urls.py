from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
from OrderFood.views import index, demo, direct_to_template, order_food, order_detail, remove_order, order_today, \
    load_nav_info, order_count_today
from Ordering import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Ordering.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^template/(?P<template_name>\w+)/$', direct_to_template),
    url(r'^$', index),
    url(r'^demo/', demo),
    url(r'^navinfo/', load_nav_info),
    url(r'^orderfood/(?P<restaurant_name>\w+)/$', order_food),
    url(r'^orderdetail/(?P<team>\w+)/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)$', order_detail),
    url(r'^orderdetail/(?P<team>\w+)/today/', order_today),
    url(r'^order/delete/$', remove_order),
    url(r'^orderstatistic/(?P<team>\w+)/today/', order_count_today),
) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
