# This script shows an example of how to use add_bes_to_nl to add the BES islands to an existing map of the Netherlands

import add_bes_to_nl

source_pic = 'example_NL.png'

bes_data = {'bonaire': {'color': '222222'},
            'saba': {'color': '555555'},
            'statia': {'color': '123456'}}

# By default, BES will be put in top-left using a transparent layer and certain generally usable settings.
add_bes_to_nl.add_to(source_pic, bes_data, save_to='untweaked.png')

# But, these settings can be tweaked by specifying a Config object, in which the default settings can be overridden.
config = add_bes_to_nl.Config()  # -> BES config, EU/source config, target config




# Add_bes_to_nl
# NL_at_its_BESt
# nl_bes
# nl_maps