# Full Netherlands maps - Work In Progress
Create maps of the Netherlands that include the BES islands:
- append the islands to an existing map
- generate a new map (based on provinces or municipalities) that can also include the BES islands.

Status: Work in Progress! This is not yet ready for production, but if you want to take it for a spin as is, feel free
to try. Suggestions and questions are welcome!

## How to install and use
To install, you can use pip:
`pip install nl_maps`

A basic example of how to use this to update an existing figure:
```python
import nl_maps
input_picture = 'input.png'
bes_colors = {'bonaire': [255, 255, 0],
              'saba':    [255, 255, 0],
              'statia':  [0, 255, 0]}
nl_maps.add_to_existing(input_picture, bes_colors, save_to='output.png')
```
A basic example of how to use this to generate a figure from scratch:
```python
import nl_maps
nl_data = nl_maps.NLData(kind='provinces')  # Initialize with all provinces and BES islands set to 'N/A' and gray color
nl_data.update({'bonaire': 'Lived there', 'zuid-holland': 'Lived there', 'utrecht': 'Semi-lived there'})  
nl_maps.generate_map(nl_data, save_to='output.png')
```

### Extra configuration
The functionality of this package can be / will be changed in several ways:
- supplying a nl_maps.Config object to add_to_existing/generate_map, which can:
  - change background color of output
  - change how to crop/zoom an existing figure before appending BES islands
  - change where the BES islands will be put, and whether there will be an inset or not
  - change output size
- initializing nl_data with inputs:
  - input `kind` can be 'provinces' or 'municipalities' to generate with either, or 'None' to skip them
  - input 'include_bes' is True by default and will initialize the BES islands but can be set to False
- updating default colors in nl_data by calling nl_data.set_colors()
  - one can call nl_data.get_categories() to see the current mapping of categories to colors

More options and a full documentation with examples of these are planned for the future.

## Motivation
This package exists because of me coming across a lot of maps for the Netherlands that don't contain the BES islands, 
but being in a situation where they either should contain them or that it would be nice if they would. I started to look
into how difficult this might be, and discovered that only rarely geographic packages include visualizations of both 
parts of the Netherlands in one structure or setup. This is also why for example on Wikipedia page on Dutch 
municipalities the map style is different for the Caribbean ones compared to the European ones. 

Instead of simply accepting this as an unchangeable reality, this package exists to change that. The focus of this
package is on people generating maps without being specialized in the geodata world. People who are part of that world
probably have access to better tools to properly tackle this. This can result in nice interactive plots that would be
extended with the Caribbean islands as well.

But next to the proper solution, there will be a lot of people who are not experts in that topic or have access to the
required packages and shapefiles, and for them this package exists. The simplest use case is probably to append the
islands with a color per island to an existing map without them - and that is something for which geodata tools would
not be an easy solution as well!

Some examples of when you should or could show the Caribbean islands, based on the author's subjective opinion:
- A map that shows results of national or European elections by showing the party with the most votes per municipality
or province. Votes on the BES islands count exactly the same towards that as votes on European Netherlands but they are
often not shown on national media even though the data is available. Without the islands, these maps are simply not
complete so they **should** show them.
- Similarly to above but for municipal elections. There can be an argument to not show them, since there are different
political parties for the island elections with totally different topics. For awareness purposes they **could** be
included ("Oh, on the islands they had elections as well") but for the message that the map is trying to convey it is
probably not relevant ("Across the country, people voted mostly for Party X, with exceptions for Y and Z in regions 
A and B").
- Showing generally available statistics across the country, such as average household size, average household income,
etcetera. The European level data come from CBS (Statistics Netherlands), who also provide data for the Caribbean
Netherlands for most common statistics. In order to show a complete picture of the Netherlands, these maps **should**
include the islands as well as long as the data is easily available.
- A map of the different water suppliers / water companies in the Netherlands. People use such a graph in case they
are interested in the company supplying water to a specific area, for example when they are planning to move there. Of 
course, the islands have their own water infrastructure, so people will not look at the islands for the same reason, but
for completeness it **could** be included and would not be too difficult to find.

There are also cases where including the islands makes little sense and it is fine to not include them:
- For a company only operating in the European parts of the Netherlands, showing some operating statistic across the
country. Including the BES islands could be done but it would just be visualizing 'N/A' anyway.
- Similarly, for services that are organized differently or not present on the islands, such as a map on "walking 
distance to nearest train station" (unless the map is made to show these differences).

### Frequently Asked Questions

_Q: why is this tool in English for a mostly Dutch-speaking country?_

English is the default language for software development, especially in the Western world. It is generally expected
that people who could read and understand the source code will understand English even if Dutch (or Papiamentu or
Frisian for that matter) would be their native language. Since some of the Python syntax is based on English words,
mixing English and Dutch would result in awkward reading, such as when using .lower() (a method name clearly based
on English) on Dutch variables. Also, non-Dutch people will be able to contribute to this project more easily.

Note that I have plans to translate the package to Dutch (and more) on the user side. For example, one could then do
`nl_maps.voeg_bes_toe()`.

_Q: if you want people to include the BES islands on maps of the Netherlands, then why do you support the option to
create maps without them in this package?_

For multiple reasons:
- there can be cases to make maps without the BES islands, as discussed above. To take away the hurdle to also easily
generate maps with the BES islands when the situation arises, it would be best if great if people could use the same
package for both use cases.
- to provide the framework for potentially also including the CAS islands later on - so there should be logic to show
or not show islands.
- to generate examples without the islands for this repository, without having to include examples from the outside
world with potential copyright restrictions. :)

## Future plans
This is a list of future plans, in no particular order.
- Actually include municipalities
- Rework nl_maps.py to classes because of shared functionality between both functions
- Allow for colors on a gradient in case of visualizing numeric data 
- Allow for custom default palettes
- A fully Dutch version, and later on, Papiamentu and Frisian as well
  - Related to this: allow translations of provinces, islands and key municipalities as well
- Extend it to include the CAS islands as well (Curaçao, Aruba, Sint Maarten) which are part of the kingdom but not the
country. There can be maps for which they would be needed or interesting.
- Include generation of legend and customization thereof
- Include potential footnotes for source of data or how BES data was brought in line with EU data (such as converting
dollars to euros)
- Integrate this with data pulled from CBS on municipality or province level (and automatically map to BES data tables)

## Licensing and modifications
The MIT License as included in `LICENSE` applies to all files in this repository outside the `source/` folder. For the
PNG files in that folder, separate licenses apply, as explained in `source/MODIFICATIONS.md` together with the changes
that have been applied to the original files.
