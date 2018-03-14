from django import forms

from feats.models import Feat, Class


class CharacterForm(forms.Form):
    ch_level = forms.IntegerField(label='Level', min_value=0, required=False)
    ch_class = forms.ModelChoiceField(Class.objects.all(),
                                      required=False, label="Class")
    ch_feats = forms.ModelMultipleChoiceField(Feat.objects.all())
    ch_str = forms.IntegerField(label="STR", min_value=0, required=False)
    ch_dex = forms.IntegerField(label="DEX", min_value=0, required=False)
    ch_con = forms.IntegerField(label="CON", min_value=0, required=False)
    ch_int = forms.IntegerField(label="INT", min_value=0, required=False)
    ch_wis = forms.IntegerField(label="WIS", min_value=0, required=False)
    ch_cha = forms.IntegerField(label="CHA", min_value=0, required=False)

    ch_bab = forms.IntegerField(label="BAB", min_value=0, required=False)
