from rest_framework import serializers

from feats.models import Feat


class FeatListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feat
        fields = ('pk', 'name', 'feat_type')


class FeatDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feat
        fields = ('pk', 'name', 'feat_type', 'benefit', 'html_text',
                  'req_feats', 'req_traits')
        depth = 1
