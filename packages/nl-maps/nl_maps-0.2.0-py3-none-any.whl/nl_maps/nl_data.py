from collections import defaultdict


DEFAULT_COLORS = [[255, 0, 0, 255],
                  [0, 255, 0, 255],
                  [0, 0, 255, 255],
                  [255, 255, 0, 255],
                  [255, 0, 255, 255],
                  [0, 255, 255, 255],
                  [127, 0, 0, 255],
                  [0, 127, 0, 255],
                  [0, 0, 127, 255],
                  [127, 127, 0, 255],
                  [127, 0, 127, 255],
                  [0, 127, 127, 255],
                  [127, 255, 255, 255],
                  [255, 127, 255, 255],
                  [255, 255, 127, 255],
                  [127, 127, 255, 255],
                  [127, 255, 127, 255],
                  [255, 127, 127, 255],
                  [127, 255, 0, 255],
                  [255, 127, 0, 255],
                  [255, 0, 127, 255],
                  [127, 0, 255, 255],
                  [0, 127, 255, 255],
                  [0, 255, 127, 255] ]

rename = {'bon': 'bonaire', 'bo': 'bonaire', 'sab': 'saba', 'sta': 'statia', 'stat': 'statia', 'eus': 'statia',
          'eustatius': 'statia', 'st eustatius': 'statia', 'sint eustatius': 'statia',
          'zh': 'zuid-holland', 'nh': 'noord-holland', 'ut': 'utrecht', 'fr': 'friesland', 'gr': 'groningen',
          'dr': 'drenthe', 'li': 'limburg', 'nb': 'noord-brabant', 'ov': 'overijssel', 'fl': 'flevoland',
          'ze': 'zeeland',
          'adam': 'amsterdam', 'rdam': 'rotterdam', 'sdam': 'schiedam', 'dh': 'den haag', 'haag': 'den haag',
          'other': 'other'}  # Other is a hack


class NLData:

    def __init__(self, kind='provinces', include_bes=True):
        self.kind = kind
        self.include_bes = include_bes
        self.color_mapping = defaultdict(lambda: DEFAULT_COLORS[len(self.color_mapping)])
        self.color_mapping['N/A'] = [127, 127, 127, 255]
        self.mapping = {}
        if self.kind == 'provinces':
            self._init_provinces()
        if self.kind == 'municipalities':
            self._init_municipalities()
        if self.include_bes:
            self._init_bes()


    def _init_provinces(self):
        province_mapping = {k: 'N/A' for k in ['zuid-holland', 'noord-holland', 'utrecht', 'zeeland', 'noord-brabant',
                                               'limburg', 'gelderland', 'flevoland', 'overijssel', 'drenthe',
                                               'friesland', 'groningen']}
        self._auto_update_colors(province_mapping)
        return {}

    def _init_municipalities(self):
        return {}  # TODO - will be quite some manual work so first make sure the concept works using the provinces

    def _init_bes(self):
        bes_mapping = {k: 'N/A' for k in ['bonaire', 'saba', 'statia']}
        self._auto_update_colors(bes_mapping)

    def _auto_update_colors(self, apply_mapping=None):
        if apply_mapping:
            for k, v in apply_mapping.items():
                # self.mapping[k] = [v, self.color_mapping[v]]
                self.mapping[k] = v
        else:  # TODO: consider to remove below since it is now doing nothing and a remainder from an older setup
            for k, v in self.mapping.items():
                pass  # self.mapping[k] = [v, self.color_mapping[v]]


    def _get_full_mapping(self, mapping):
        if 'bes' in mapping.keys():
            mapping['bonaire'] = mapping['bes']
            mapping['saba'] = mapping['bes']
            mapping['statia'] = mapping['bes']
            del mapping['bes']
        mapping = {rename[k.lower()] if k.lower() not in self.mapping else k.lower(): v for k, v in mapping.items()}
        if 'other' not in mapping.keys():
            return mapping
        return {k: mapping[k] if k in mapping.keys() else mapping['other']
                for k in self.mapping.keys()}

    def update(self, update_dict):
        update_dict = self._get_full_mapping(update_dict)
        self._auto_update_colors(update_dict)
        self.mapping.update(update_dict)

    def get_categories(self):
        return self.color_mapping.values()

    def set_colors(self, color_dict):
        self.color_mapping.update(color_dict)
        self._auto_update_colors()