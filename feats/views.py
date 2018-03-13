from django.contrib import messages
from django.views.generic import TemplateView
from rest_framework import pagination
from rest_framework import viewsets

from feats.models import Feat
from feats.serializers import FeatDetailsSerializer
from feats.serializers import FeatListSerializer


class HomePageView(TemplateView):
    template_name = 'feats/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.warning(self.request, 'Hello there! Please aware that it\'s '
                                       'just alpha version of Feat Filter. '
                                       'Have Fun!')
        context['feat_list'] = Feat.objects.all()
        return context


class FeatViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Feat.objects.all().order_by('name')
    serializer_classes = {
        'list': FeatListSerializer,
        'retrieve': FeatDetailsSerializer
    }
    pagination_class = pagination.LimitOffsetPagination

    def get_serializer_class(self):
        if self.action in self.serializer_classes:
            return self.serializer_classes[self.action]
        return super().get_serializer_class()
