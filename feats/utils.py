from django.db.models import Q

from feats.models import Feat, FeatType, Trait, ClassFeature


class FeatFilter:
    numeric_fields = (
        ('ch_lvl', 'req_lvl'),
        ('ch_c_lvl', 'caster_lvl'),
        ('ch_bab', 'req_bab'),
        ('ch_str', 'req_str'),
        ('ch_dex', 'req_dex'),
        ('ch_con', 'req_con'),
        ('ch_int', 'req_int'),
        ('ch_wis', 'req_wis'),
        ('ch_cha', 'req_cha'),

    )

    @classmethod
    def apply_form(cls, feats_qs, form):
        if not form.is_valid():
            return feats_qs
        form_data = form.cleaned_data

        feats_qs = cls._filter_by_feat_type(feats_qs, form_data)
        feats_qs = cls._filter_by_numeric_fields(feats_qs, form_data)
        feats_qs = cls._filter_by_class_and_race(feats_qs, form_data)
        feats_qs = cls._filter_by_class_features(feats_qs, form_data)
        feats_qs = cls._filter_by_feats_and_traits(feats_qs, form_data)
        return feats_qs

    @classmethod
    def _filter_by_numeric_fields(cls, feats_qs, cleaned_data):
        for form_field, model_fileld in cls.numeric_fields:
            if cleaned_data.get(form_field) is not None:
                feats_qs = feats_qs.filter(
                    Q(**{"{}__lte".format(model_fileld): cleaned_data[form_field]}) |
                    Q(**{"{}__isnull".format(model_fileld): True}))
        return feats_qs

    @classmethod
    def _filter_by_class_and_race(cls, feats_qs, cleaned_data):

        if cleaned_data.get('ch_class'):
            feats_qs = feats_qs.filter(
                Q(req_classes=None) |
                Q(req_classes__pk__exact=cleaned_data['ch_class'].pk))

        if cleaned_data.get('ch_race'):
            feats_qs = feats_qs.filter(
                Q(req_races=None) |
                Q(req_races__pk__exact=cleaned_data['ch_race'].pk))

        return feats_qs

    @classmethod
    def _filter_by_feats_and_traits(cls, feats_qs, cleaned_data):
        if cleaned_data.get('ch_feats'):
            ch_feats_qs = Feat.objects.exclude(id__in=cleaned_data['ch_feats']).distinct()
            feats_qs = feats_qs.exclude(req_feats__in=ch_feats_qs).distinct()

        if cleaned_data.get('ch_traits'):
            ch_traits_qs = Trait.objects.exclude(id__in=cleaned_data['ch_traits']).distinct()
            feats_qs = feats_qs.exclude(req_traits__in=ch_traits_qs).distinct()

        return feats_qs

    @classmethod
    def _filter_by_feat_type(cls, feats_qs, cleaned_data):
        if cleaned_data.get('feat_type'):
            types_qs = FeatType.objects.exclude(id__in=cleaned_data['feat_type']).distinct()
            feats_qs = feats_qs.exclude(feat_type__in=types_qs).distinct()
        return feats_qs

    @classmethod
    def _filter_by_class_features(cls, feats_qs, cleaned_data):
        if cleaned_data.get('ch_class_features'):
            types_qs = ClassFeature.objects.exclude(id__in=cleaned_data['ch_class_features']).distinct()
            feats_qs = feats_qs.exclude(req_class_features__in=types_qs).distinct()
        return feats_qs
