#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pprint
import os
from . import image_slicer
import sys
from PIL import Image, ImageFilter
import PIL.ImageOps
import math
import numpy as np
from tqdm import tqdm

import multiprocessing
from functools import partial


def alpha_to_color(image:PIL.Image, color=255) -> PIL.Image:
    """Set all fully transparent pixels of an RGBA image to the specified color.
    This is a very simple solution that might leave over some ugly edges, due
    to semi-transparent areas. You should use alpha_composite_with color instead.

    Source: http://stackoverflow.com/a/9166671/284318

    Keyword Arguments:
    image -- PIL RGBA Image object
    color -- Tuple r, g, b (default 255, 255, 255)

    """ 
    try:
        x = np.array(image)
        r, g, b, a = np.rollaxis(x, axis=-1)
        r[a == 0] = color
        g[a == 0] = color
        b[a == 0] = color
        x = np.dstack([r, g, b, a])
        return Image.fromarray(x, 'RGBA')
    except:
        return image

def calcImgResize(img_size, size, max_size=500):
    # leinwandgröße
    f = max_size / max(size)
    s = (round(f * size[0]), round(f * size[1]))
    # img resize
    f = max(s) / max(img_size)
    i = (round(f * img_size[0]), round(f * img_size[1]))
    return i, s

#@filecache(60*60*24*14)
def detect_edges(filename, out_dir, invert=False, edge=150, alphacolor=255, size=(10,10), padding=(0,0)):
    file_append = "%d_%d_%d_%d_%d_%d_%d.png"%(invert,edge,alphacolor,size[0],size[1],padding[0],padding[1])
    img_path = os.path.join(out_dir, os.path.basename(filename)+file_append)
    if not os.path.exists(img_path):
        image = Image.open(filename)
        #print(out_dir, invert, edge, filename)
        image = alpha_to_color(image,alphacolor)
        resize_size, canvas_size = calcImgResize(image.size, size)
        if padding != 0:
            canvas_size = (canvas_size[0]+padding[0], canvas_size[1]+padding[1])
        image = image.convert("L")
        image = image.resize(resize_size)
        if invert:
            image = PIL.ImageOps.invert(image)
        if edge == -1:
            image = PIL.ImageOps.autocontrast(image)
        elif edge == 0:
            image = image.filter(ImageFilter.FIND_EDGES)
        else:
            image = image.point(lambda i: i < edge and 255)
        if canvas_size != resize_size:
            # todo: we should look at the border of the original image
            # - if more than 50% is white, take white otherwise black
            newImage = Image.new("L", canvas_size, "white")
            x_pad = round((canvas_size[0]-resize_size[0]) / 2)
            y_pad = round((canvas_size[1]-resize_size[1]) / 2)
            newImage.paste(image, (x_pad,y_pad,x_pad+resize_size[0],y_pad+resize_size[1]))
            image = newImage
        image.save(img_path)
    return img_path

def divide(filename, size=(10,10)):
    tiles = image_slicer.slice(filename, size[0]*size[1], save=False, size=size)
    return tiles

def calc_angle(tile, filter=14):
    pixels = tile.image.getdata()
    width, height = tile.image.size
    l = width*height
    c = list(pixels).count(255)
    if c >= l - (l/95): # 95% black
        return 0
    if c <= l/100*filter: # filter% white
        return 900
    # 90% of the time is spent in list creation :(
    xpoints = [i//width for i,x in enumerate(pixels, 1) if x != 0]
    ypoints = [i%width for i,x in enumerate(pixels, 1) if x != 0]
    m,c = calc_polyfit(xpoints, ypoints, width, height)
    return (int(math.degrees(math.atan(m))*10)+3600)%3600

def calc_polyfit(xpoints, ypoints, width, height):
    res1 = np.polyfit(xpoints, ypoints, 1, full=True)
    res2 = np.polyfit(ypoints, xpoints, 1, full=True)
    # calculate c as it would go through the center
    if res1[1][0] < res2[1][0]:
        m = res1[0][0]
        c = width//2 - math.floor(m * height//2)
    else:
        m = res2[0][0]
        c = height//2 - math.floor(m * width//2)
    # this means: y = m * x + c
    return m,c

def all_angles(filename, out_dir=".", invert=False, edge=150, filter=14, alphacolor=255, progress=True, size=(10, 10)):
    simple_file = detect_edges(filename, out_dir, invert, edge, alphacolor, size)

    tiles = divide(simple_file, size)
    angles = [[0]*size[0] for _ in range(size[1])]
    for tile in tqdm(tiles, disable=not progress, desc=filename):
        g = calc_angle(tile, filter)
        angles[tile.position[1]-1][tile.position[0]-1] = g
    return angles, filename

def all_angles_mp(filenames, cpu=-1, **kwargs):
    if cpu == -1:
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
    else:
        pool = multiprocessing.Pool(cpu)
    ret = {}
    for res in pool.imap_unordered(partial(all_angles, **kwargs), filenames):
        angles, fn = res
        ret[fn] = angles
    return ret

if __name__ == "__main__":
    try:
        os.mkdir("out")
    except:
        pass
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        angles,filename = all_angles(filename, "out")
        pprint.pprint(angles)
    if len(sys.argv) > 2:
        filename = sys.argv[1:]
        ret = all_angles_mp(filename, out_dir="out")
        pprint.pprint(ret)
