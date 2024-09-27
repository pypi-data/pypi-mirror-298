import os
from PIL import Image, ImageDraw, ImageFont, ImageOps

import yaml


with open('config.yml', 'r') as file:
   configs = yaml.safe_load(file)

def replace(image, color_from, color_to):
    newIm = []
    for item in image.getdata():
        if all(color_from['lb'][i] <= x < color_from['ub'][i] for i, x in enumerate(item[:3])):
            newIm.append(tuple(color_to))
        else:
            newIm.append(item)
    image.putdata(newIm)
    return image

def run(config):
    bes_config = config['bes_config']
    nl_config = config['nl_config']
    sq_fit_size = 1250
    os.makedirs(config['nl_config']['folder_out'], exist_ok=True)

    island_images = {island: Image.open(bes_config['files'][island]).convert('RGBA') for island in bes_config['islands']}

    def crop_and_paste(image, paste_image, crop, loc, resize, island):
        this_image = paste_image  # paste_image.copy()
        this_image = this_image.crop(crop)
        this_image = this_image.resize((int(this_image.size[0]//resize), int(this_image.size[1]//resize)))
        this_image = replace(this_image, bes_config['colors']['foreground'], nl_config['bes_colors'][island])
        this_image = replace(this_image, bes_config['colors']['background'], nl_config['bes_colors']['background'])
        image.paste(this_image, loc, this_image)

    filename = config['nl_config']['filename_in']
    folder = config['nl_config']['folder_in'] + '/'

    print(f'Appending BES to {filename}..')
    im = Image.open(folder + filename)
    if nl_config['fill_NL']:
        for k, v in nl_config['nl_locs'].items():
            for el in v:
                ImageDraw.floodfill(im, el, tuple(nl_config['nl_colors'][k]), thresh=5)

    if nl_config['do_crop']:
        im = im.crop(nl_config['crop_nl'])

    im = im.resize((im.size[0] // nl_config['image_scale'], im.size[1] // nl_config['image_scale']))
    ratio = im.size[0] / sq_fit_size

    for island in nl_config['locations'].keys():
        this_loc = tuple([int(x*ratio) for x in nl_config['locations'][island]])
        crop_and_paste(im, island_images[island], bes_config['crops'][island], this_loc, resize=4/ratio, island=island)

    def set_inset(image, inset_coords, inset_color):
        this_coords = tuple([ratio * x for x in inset_coords])
        ImageDraw.ImageDraw(image).line([(0, this_coords[1]), tuple(this_coords)], fill=inset_color, width=5)
        ImageDraw.ImageDraw(image).line([(this_coords[0], 0), tuple(this_coords)], fill=inset_color, width=5)
        return image

    if config['nl_config']['add_inset_border']:
        im = set_inset(im, config['nl_config']['inset_loc'], inset_color = tuple(config['nl_config']['inset_color']))

    if config['nl_config']['legend']:
        # Recover color + labels for both NL and BES part (-> labels need to be added to config)
        # Sort by most common, and then alphabetically (or only alphabetically)
        # (Potentially limit to, e.g., 10 most common
        # Plot a square with color-box and text in it and append to figure -> say if 4 fit, create multiple lines

        # Test code below to understand workings
        fontSize = 20
        annotation = "test"
        padding = 20
        font = ImageFont.truetype("/usr/share/fonts/truetype/freefont/FreeMono.ttf", fontSize, encoding="unic")  # TODO make this OS agnostic
        temp = font.getbbox(annotation)
        tw, th = temp[2] - temp[0], temp[3] - temp[1]
        extended = ImageOps.expand(im, border=(0, 0, 0, int(th + 2 * padding)), fill=(0, 0, 0))
        w, h = extended.size
        draw = ImageDraw.Draw(extended)
        draw.text(((w - tw) // 2, h - th - padding), annotation, (255, 255, 255), font=font)
        extended.save('out/result.png')


    im.save(os.path.join(config['nl_config']['folder_out'], config['nl_config']['filename_out']))


if __name__ == "__main__":
    for use_cfg in configs['use_config']:
        this_config = configs[use_cfg]
        run(this_config)
