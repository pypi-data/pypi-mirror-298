class Config:

    def __init__(self):
        self.bes_config = BESConfig()
        self.eunl_config = EUNLConfig()
        self.out_config = OutConfig()


class BESConfig:

    def __init__(self):
        self.filename_in = 'bes_islands.png'
        self.folder_in = 'source'
        self.crops = {
            'bonaire': [0, 1060, 990, 2050],
            'saba': [0, 0, 250, 200],
            'statia': [640, 560, 990, 950]
        }
        self.raw_color = {
            'background': {'lb': [200, 200, 200], 'ub': [256, 256, 256]},
            'foreground': {'lb': [100, 100, 100], 'ub': [200, 200, 200]}
        }

class EUNLConfig:

    def __init__(self):
        self.filename_in = 'nl_provinces.png'
        self.folder_in = 'source'
        self.nl_locs = {
            'zuid-holland': [[538, 1132], [392, 1318]],
            'noord-holland': [[700, 700], [700, 350]],
            'utrecht': [[900, 1000]],
            'zeeland': [[300, 1350], [380, 1430], [230, 1430], [250, 1500], [300, 1600]],
            'noord-brabant': [[900, 1400]],
            'limburg': [[1250, 1500]],
            'gelderland': [[1100, 1000]],
            'overijssel': [[1400, 800]],
            'flevoland': [[1000, 800], [1100, 600]],
            'drenthe': [[1500, 500]],
            'groningen': [[1400, 200], [1380, 25], [1430, 25]],
            'friesland': [[750, 240], [900, 125], [1100, 88], [1250, 70], [1100, 400]]}


class OutConfig:

    def __init__(self):
        self.bes_locs = {
            'bonaire': [ 100, 300 ],
            'saba': [ 120, 50 ],
            'statia': [ 220, 150 ]
        }
        self.background_color = [255, 255, 255, 255]
        self.folder_out = 'out'
        self.file_out = 'out.png'
