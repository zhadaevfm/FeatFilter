from django import forms

from feats.models import Feat, Class, FeatType, Trait, Race


class CharacterForm(forms.Form):
    ch_lvl = forms.IntegerField(label='Level', min_value=0, required=False)
    ch_bab = forms.IntegerField(label="BAB", min_value=0, required=False)

    ch_str = forms.IntegerField(label="STR", min_value=0, required=False)
    ch_dex = forms.IntegerField(label="DEX", min_value=0, required=False)
    ch_con = forms.IntegerField(label="CON", min_value=0, required=False)
    ch_int = forms.IntegerField(label="INT", min_value=0, required=False)
    ch_wis = forms.IntegerField(label="WIS", min_value=0, required=False)
    ch_cha = forms.IntegerField(label="CHA", min_value=0, required=False)

    ch_class = forms.ModelChoiceField(Class.objects.all(),
                                      required=False, label="Class")
    ch_race = forms.ModelChoiceField(Race.objects.all().order_by("name"),
                                     required=False, label="Race")
    ch_traits = forms.ModelMultipleChoiceField(
        Trait.objects.all().order_by('name'), required=False, label="Traits")
    ch_feats = forms.ModelMultipleChoiceField(
        Feat.objects.all().order_by('name'), required=False, label="Feats")

    feat_type = forms.ModelMultipleChoiceField(FeatType.objects.all(),
                                               required=False, label="FeatType")
