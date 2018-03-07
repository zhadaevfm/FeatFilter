from django.urls import re_path

from feats import views

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^api/feats/$', views.feat_list, name='feat_list'),
    re_path(r'^api/feats/(?P<feat_id>\d+)/$', views.feat_details, name='feat_details')
]
