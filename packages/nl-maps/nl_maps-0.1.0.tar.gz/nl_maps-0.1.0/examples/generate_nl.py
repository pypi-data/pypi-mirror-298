# This script shows an example of how to use the package to generate a new map of the Netherlands based on plugged-in
# data

import nl_maps

# Generate an empty NLData object. By default, this will be of the municipality type - but it can be provincial as here.
data = nl_maps.NLData(kind='provinces')  # -> with/without BES as well (in future CAS?)

# Initially, all regions are set to have a gray color and N/A label. These can be set manually using a dictionary
# (practically, you probably want to provide it from file and programmatically convert that to a dictionary).
# Let's say you are making a map of how many times you have stayed on holiday in each province and public body.
set_dict = {'friesland': 3,
            'noord-holland': 2,
            'other': 0,
            'bonaire': 2,
            'zeeland': 5,
            'limburg': 3}  # Can use multiple spellings, incl Dutch & English, in future also Spanish, Papiamentu and Frisian, and abbreviations.
# Can use "bes" to set all 3 islands at once

data.update(set_dict)  # By specifying with just numbers or strings, classes will be generated and colors will be assigned
print(data.get_categories())
print(data.mapping)
# data.set_colors({k: '123123' for k in data.get_categories()})

# Then, a map can be made, with default Config:
nl_maps.generate_map(data)

# Or, the config can be changed
config = nl_maps.Config() # -> BES config, EU config, target config
config.out_config.bes_locs = {
    'bonaire': [100, 50],
    'saba': [120, 200],
    'statia': [220, 350]
}
nl_maps.generate_map(data, config, save_to='out/wowie.png')
