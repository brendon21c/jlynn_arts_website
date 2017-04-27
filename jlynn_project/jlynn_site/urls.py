from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views, views_shop, purchase, order_summary

app_name = 'jlynn_site'


urlpatterns = [

    url(r'^$', views.homepage, name='homepage'),
    url(r'^shop/$', views_shop.art_store, name='art_store'),
    url(r'^shop/purchase/(?P<image_pk>\d+)/$', purchase.buy_painting, name='buy_painting'),
    url(r'^shop/order_summary/$', order_summary.order_summary, name='order_summary')

    ]
