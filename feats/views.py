from rest_framework import pagination
from rest_framework import viewsets

from feats.models import Feat
from feats.serializers import FeatDetailsSerializer
from feats.serializers import FeatListSerializer


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
