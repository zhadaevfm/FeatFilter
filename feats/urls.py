from django.urls import path

from feats import views

urlpatterns = [
    path('', views.index, name='index')
]
