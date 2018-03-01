import pandas as pd
import json

MYTHIC = 'Mythic'


class FeatEntry(object):
    pass


class FeatParser(object):

    def parse(self, path_to_file):
        data_frame = pd.read_csv(path_to_file, sep="\t", index_col="id",
                                 keep_default_na=False)
        records = data_frame.to_dict('records')
        flat_dict = {}
        for r in records:
            tmp = self._convert_record(r)
            flat_dict[tmp['name']] = tmp

        print(json.dumps(flat_dict['Snatch Arrows'], indent=2))

    def _convert_record(self, record):
        result = dict()
        fields_to_copy = ['name', 'type', 'description', 'benefit', 'normal',
                          'special', 'source', 'fulltext', 'note', 'goal',
                          'completion_benefit']

        for f in fields_to_copy:
            result[f] = record[f]

        if MYTHIC == result['type']:
            result['name'] = "{} ({})".format(result['name'], MYTHIC)

        result['suggested_traits'] = self._comma_split_and_title(
            record['suggested_traits'])

        requirements = {
            "races": self._comma_split_and_title(record['race_name']),
            "feats": self._comma_split_and_title(record['prerequisite_feats']),
            "as_text": record['prerequisites'].strip('.')
        }
        result['requirements'] = requirements

        flag_fields = ['teamwork', 'critical', 'grit', 'style', 'performance',
                       'racial', 'companion_familiar', 'multiples']
        flags = {x: bool(record[x]) for x in flag_fields}
        result['flags'] = flags

        return result

    def _comma_split_and_title(self, string):
        if not string:
            return []
        return [p.strip().title() for p in string.strip('.').split(',')]


if __name__ == '__main__':
    parser = FeatParser()
    parser.parse("../data/feats-23-03-2014.tsv")
