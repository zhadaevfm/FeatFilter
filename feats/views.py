from django.contrib import messages
from django.views.generic import TemplateView
from rest_framework import pagination
from rest_framework import viewsets

from feats.forms import CharacterForm
from feats.models import Feat
from feats.serializers import FeatDetailsSerializer
from feats.serializers import FeatListSerializer
from feats.utils import FeatFilter


class HomePageView(TemplateView):
    template_name = 'feats/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        messages.warning(self.request, 'Hello there! Please aware that it\'s '
                                       'just alpha version of Feat Filter. '
                                       'Have Fun!')

        character_form = kwargs.pop('char_form', None)
        feats_qs = Feat.objects.filter(feat_type__isnull=False)

        if character_form:
            if character_form.is_valid():
                feats_qs = FeatFilter.apply_form(
                    feats_qs, character_form)
        else:
            character_form = CharacterForm()

        context['char_form'] = character_form
        context['feat_list'] = feats_qs.order_by('name')
        context['feats_total'] = feats_qs.count()

        return context

    def post(self, request, *args, **kwargs):
        kwargs['char_form'] = CharacterForm(request.POST)
        return self.get(request, *args, **kwargs)


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
