from django.urls import re_path, include
from rest_framework import routers

from feats.views import FeatViewSet, HomePageView

router = routers.DefaultRouter()
router.register(r'feats', FeatViewSet)

urlpatterns = [
    re_path(r'^api/', include(router.get_urls())),
    re_path(r'^$', HomePageView.as_view(), name='home'),
]
