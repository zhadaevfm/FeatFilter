import json
import re

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
        flat_dict = {}
        for r in records:
            tmp = self._convert_record(r)
            flat_dict[tmp['name']] = tmp

        print(json.dumps(flat_dict['Power Attack'], indent=2))

    def _convert_record(self, record):
        result = dict()
        fields_to_copy = ['name', 'type', 'description', 'benefit', 'normal',
                          'special', 'source', 'fulltext', 'note', 'goal',
                          'completion_benefit']

        for f in fields_to_copy:
            result[f] = record.get(f, None)

        if MYTHIC == result['type']:
            result['name'] = "{} ({})".format(result['name'], MYTHIC)

        result['suggested_traits'] = self._comma_split(
            record['suggested_traits'], title=True)

        requirements = {
            "races": self._comma_split(record.get('race_name', None),
                                       title=True),
            "feats": self._comma_split(
                record.get('prerequisite_feats', None), title=True),
            "as_text": record.get('prerequisites', "").strip('.')
        }
        result['requirements'] = requirements
        requirements.update(
            self._parse_requirements_text(requirements['as_text']))

        flag_fields = ['teamwork', 'critical', 'grit', 'style', 'performance',
                       'racial', 'companion_familiar', 'multiples']
        flags = {x: bool(record.get(x, False)) for x in flag_fields}
        result['flags'] = flags

        return result

    def _parse_requirements_text(self, req_string):
        result = {}
        for s in self._comma_split(req_string):
            for key, pattern in NUMBER_REQ_PATTERNS.items():
                m = pattern.match(s)
                if m:
                    result[key] = int(m.group(1))
            m = SKILL_REQ_PATTERN.match(s)
            if m:
                result.setdefault("req_skills", {})[m.group(1)] = int(m.group(2))
            m = CLASS_FEATURE_PATTERN.match(s)
            if m:
                result.setdefault("req_class_features", []).append(
                    m.group(1).title())
            m = RACIAL_TRAIT_PATTERN.match(s)
            if m:
                result.setdefault("req_traits", []).append(
                    m.group(1).title())
            m = CLASS_LEVEL_PATTERN.match(s)
            if m:
                result["req_lvl"] = m.group(1)
                result.setdefault("req_classes", []).append(m.group(2).title())
        return result

    def _comma_split(self, string, title=False):
        if not string:
            return []
        return [p.strip().title() if title else p.strip()
                for p in string.strip('.').split(',')]


if __name__ == '__main__':
    parser = FeatParser()
    parser.parse("../data/feats-23-03-2014.tsv")
