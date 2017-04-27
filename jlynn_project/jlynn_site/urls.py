from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views, views_shop

app_name = 'jlynn_site'


urlpatterns = [

    url(r'^$', views.homepage, name='homepage'),
    url(r'^shop/$', views_shop.art_store, name='art_store'),
    url(r'^shop/buy/(?P<image_pk>\d+)/$', views_shop.buy_painting, name='buy_painting')

    ]
