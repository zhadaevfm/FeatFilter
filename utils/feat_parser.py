import os
import re

import django
import pandas as pd

MYTHIC = 'Mythic'

NUMBER_REQ_PATTERNS = {
    "req_dex": re.compile("Dex (\d+)"),
    "req_str": re.compile("Str (\d+)"),
    "req_con": re.compile("Con (\d+)"),
    "req_int": re.compile("Int (\d+)"),
    "req_wis": re.compile("Wis (\d+)"),
    "req_cha": re.compile("Cha (\d+)"),
    "req_bab": re.compile("[Bb]ase attack bonus ([+-]?\d+)"),
    "req_lvl": re.compile("[Cc]haracter level (\d+)\w*"),
    "caster_lvl": re.compile("[Cc]aster level (\d+)\w*")
}

SKILL_REQ_PATTERN = re.compile("(\w+) (\d+) rank[s]?")
CLASS_FEATURE_PATTERN = re.compile("([\w \d]+) class feature")
RACIAL_TRAIT_PATTERN = re.compile("([\w \d]+) racial trait")
CLASS_LEVEL_PATTERN = re.compile("(\d+)\w*-level (\w+)")


class FeatParser(object):

    def parse(self, path_to_file):
        data_frame = pd.read_csv(path_to_file, sep="\t", index_col="id",
                                 keep_default_na=False)
        records = data_frame.to_dict('records')
        for r in records:
            self._add_to_db(r)

    def _add_to_db(self, record):
        f_name = record['name'].title()
        f_type = record['type'].title()

        if MYTHIC == f_type:
            f_name = "{} ({})".format(f_name, MYTHIC)

        new_feat = Feat.objects.get_or_create(name=f_name)[0]
        new_feat.feat_type = FeatType.objects.get_or_create(name=f_type)[0]

        fields_to_copy = ['description', 'benefit', 'normal',
                          'special', 'source', 'note', 'goal',
                          'completion_benefit']

        for f in fields_to_copy:
            setattr(new_feat, f, record.get(f, None))

        new_feat.full_text = record.get('fulltext', None)

        for t in self._comma_split(record['suggested_traits']):
            trait = Trait.objects.get_or_create(name=t.title())[0]
            new_feat.suggested_traits.add(trait)

        for r in self._comma_split(record.get('race_name', None)):
            race = Race.objects.get_or_create(name=r.title())[0]
            new_feat.req_races.add(race)

        for f in self._comma_split(record.get('prerequisite_feats', None)):
            feat = Feat.objects.get_or_create(name=f.title())[0]
            new_feat.req_feats.add(feat)

        new_feat.req_as_text = record.get('prerequisites', "").strip('.')

        self._parse_requirements_text(new_feat)

        flag_fields = ['teamwork', 'critical', 'grit', 'style', 'performance',
                       'racial', 'companion_familiar', 'multiples']
        for field in flag_fields:
            setattr(new_feat, field, bool(record.get(field, False)))
        new_feat.save()

    def _parse_requirements_text(self, feat_obj):
        for s in self._comma_split(feat_obj.req_as_text):
            for key, pattern in NUMBER_REQ_PATTERNS.items():
                m = pattern.match(s)
                if m:
                    setattr(feat_obj, key, int(m.group(1)))
            m = SKILL_REQ_PATTERN.match(s)
            if m:
                skill = Skill.objects.get_or_create(name=m.group(1).title())[0]
                RequiredSkill.objects.create(skill=skill,
                                             feat=feat_obj,
                                             ranks=int(m.group(2)))

            m = CLASS_FEATURE_PATTERN.match(s)
            if m:
                class_feature = ClassFeature.objects.get_or_create(
                    name=m.group(1).title())[0]
                feat_obj.req_class_features.add(class_feature)

            m = RACIAL_TRAIT_PATTERN.match(s)
            if m:
                trait = Trait.objects.get_or_create(name=m.group(1).title())[0]
                feat_obj.req_traits.add(trait)

            m = CLASS_LEVEL_PATTERN.match(s)
            if m:
                feat_obj.req_lvl = int(m.group(1))
                req_class = Class.objects.get_or_create(
                    name=m.group(2).title())[0]
                feat_obj.req_classes.add(req_class)

    def _comma_split(self, string):
        if not string:
            return []
        return [p.strip() for p in string.strip('.').split(',')]


if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FeatFilter.settings")
    django.setup()
    from feats.models import *

    parser = FeatParser()
    parser.parse("../data/feats-23-03-2014.tsv")
