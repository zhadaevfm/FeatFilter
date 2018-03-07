from django.core.serializers import serialize
from django.http import HttpResponse

from feats.models import Feat


def index(request):
    return feat_list(request)


def feat_list(request):
    feats = Feat.objects.all().order_by('name')
    return HttpResponse(serialize('json', feats),
                        content_type='application/json')


def feat_details(request, feat_id):
    feats = Feat.objects.filter(pk=feat_id)
    return HttpResponse(serialize('json', feats),
                        content_type='application/json')
