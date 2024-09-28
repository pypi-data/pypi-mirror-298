# This script shows an example of how to use nl_maps to add the BES islands to an existing map of the Netherlands

import nl_maps

source_pic = '../nl_maps/source/nl_provinces.png'

bes_data = {'bonaire': [255, 255, 0],
            'saba': [ 255, 255, 0],
            'statia': [0, 255, 0]}

# By default, BES will be put in top-left using a transparent layer and certain generally usable settings.
nl_maps.add_to_existing(source_pic, bes_data, save_to='out/not-tweaked.png')

# But, these settings can be tweaked by specifying a Config object, in which the default settings can be overridden.
config = nl_maps.Config()  # -> BES config, EU/source config, target config
