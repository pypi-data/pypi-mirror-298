import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from nl_maps import NLData, Config
from importlib.resources import files


def replace(image, color_from, color_to):
    newIm = []
    for item in image.getdata():
        if all(color_from['lb'][i] <= x < color_from['ub'][i] for i, x in enumerate(item[:3])):
            newIm.append(tuple(color_to))
        else:
            newIm.append(item)
    image.putdata(newIm)
    return image


def crop_and_paste(image, paste_image, config, loc, island_col, resize, island):
    this_image = paste_image  # paste_image.copy()
    crop = config.bes_config.crops[island]
    this_image = this_image.crop(crop)
    this_image = this_image.resize((int(this_image.size[0] // resize), int(this_image.size[1] // resize)))
    this_image = replace(this_image, config.bes_config.raw_color['foreground'], island_col)
    this_image = replace(this_image, config.bes_config.raw_color['background'], config.out_config.background_color)
    image.paste(this_image, loc, this_image)


def generate_map(data: NLData, config: Config = None, save_to=None):
    config = Config() if config is None else config

    # Load in NLEU map and apply NLEU settings and NLData data
    eunl_config = config.eunl_config
    filename = eunl_config.filename_in
    folder = eunl_config.folder_in + '/'
    file = files("nl_maps").joinpath(folder + filename)  # TODO think about how user can plug in own files
    im = Image.open(file)
    for k, v in eunl_config.nl_locs.items():
        for el in v:
            ImageDraw.floodfill(im, el, tuple(data.color_mapping[data.mapping[k]]), thresh=5)  # TODO replace with get_color method

    sq_fit_size = 1250  # Perhaps out config?
    image_scale = 1  # Out config

    im = im.resize((im.size[0] // image_scale, im.size[1] // image_scale))
    ratio = im.size[0] / sq_fit_size

    # Load in BES maps and apply BES settings and NLData data to it -> paste over NLEU map
    bes_config = config.bes_config
    filename = bes_config.filename_in
    folder = bes_config.folder_in + '/'
    islands = [x for x in ['bonaire', 'saba', 'statia'] if x in data.mapping.keys()]
    for island in islands:
        file = files("nl_maps").joinpath(folder + filename)
        island_image = Image.open(file).convert('RGBA')
        this_loc = tuple([int(x*ratio) for x in config.out_config.bes_locs[island]])
        island_col = data.color_mapping[data.mapping[island]]
        crop_and_paste(im, island_image, config, this_loc, island_col, resize=4/ratio, island=island)

    # TODO: inset and legend

    # Save output while applying Out settings
    out_config = config.out_config # TODO: check if folder exists, if not create
    os.makedirs(out_config.folder_out, exist_ok=True)
    save_to = os.path.join(out_config.folder_out, out_config.file_out) if save_to is None else save_to
    im.save(save_to)


def colors_to_categories(data):
    # Convert a mapping of colors to a mapping of categories/values, as utility for `add_to_existing`.
    unique_cols = list(set([tuple(x) for x in data.values()]))
    return {k: unique_cols.index(tuple(v)) for k, v in data.items()}, {i: v for i, v in enumerate(unique_cols)}


def add_to_existing(source_pic, bes_data, config: Config = None, save_to=None):
    config = Config() if config is None else config

    # Load in NLEU map and apply NLEU settings and NLData data
    im = Image.open(source_pic)

    # TODO: add option to crop and/or zoom?

    sq_fit_size = 1250  # Perhaps out config?
    image_scale = 1  # Out config

    im = im.resize((im.size[0] // image_scale, im.size[1] // image_scale))
    ratio = im.size[0] / sq_fit_size

    # Load in BES maps and apply BES settings and NLData data to it -> paste over NLEU map
    bes_config = config.bes_config
    filename = bes_config.filename_in
    folder = bes_config.folder_in + '/'
    data = NLData(kind='none')
    bes_cats, bes_color_mapping = colors_to_categories(bes_data)
    data.update(bes_cats)
    data.set_colors(bes_color_mapping)

    islands = [x for x in ['bonaire', 'saba', 'statia'] if x in data.mapping.keys()]
    for island in islands:
        file = files("nl_maps").joinpath(folder + filename)
        island_image = Image.open(file).convert('RGBA')
        this_loc = tuple([int(x*ratio) for x in config.out_config.bes_locs[island]])
        island_col = data.color_mapping[data.mapping[island]]
        crop_and_paste(im, island_image, config, this_loc, island_col, resize=4/ratio, island=island)

    # TODO: inset and legend

    # Save output while applying Out settings
    out_config = config.out_config # TODO: check if folder exists, if not create
    os.makedirs(out_config.folder_out, exist_ok=True)
    save_to = os.path.join(out_config.folder_out, out_config.file_out) if save_to is None else save_to
    im.save(save_to)
