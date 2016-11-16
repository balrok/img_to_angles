#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageOps
from .img2angle import all_angles_mp
import time
import os
from tempfile import TemporaryDirectory
#from fontTools.ttLib import TTFont
#from tqdm import tqdm

def createImg(dir, symbol, name, fontfile):
    filename = '%s/%s.png' % (dir, name)
    if os.path.exists(filename):
        return
    image = Image.new("L", (200,200), "white")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontfile, 150)
    draw.text((0, 0), symbol, 0, font=font)
    time.sleep(0.01);
    #print(imageBox)
    #image.save(filename)
    imageBox = ImageOps.invert(image).getbbox()
    cropped=image.crop(imageBox)
    cropped.save(filename)

def convert_font(fontfile, width, height, letters="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"):
    # ttf = TTFont(fontfile, 0, verbose=0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)
    with TemporaryDirectory() as out_dir:
        for letter in letters:
            createImg(out_dir, letter, letter, fontfile)
        result = all_angles_mp(["%s/%s.png"%(out_dir, letter) for letter in letters]
                         , out_dir=out_dir, invert=True, edge=150, filter=14, alphacolor=255, size=(width, height))
    return result

def convert_folder(dir, width, height):
    # -4 removes file ending
    chars = [os.path.splitext(x)[0] for x in os.listdir(dir)]
    with TemporaryDirectory() as out_dir:
        result = all_angles_mp(["%s/%s.png"%(dir, x) for x in chars]
                           , out_dir=out_dir, invert=True, edge=150, filter=14, alphacolor=255, size=(width, height))
    return result

if __name__ == "__main__":

    type = "helvetica"

    fontfile = ""
    letters = ""
    width = 10
    height = 10
    dir = ""
    out_dir = ""

    if type == "IcoMoon":
        fontfile = "" #IcoMoon-Free.ttf"
        dir = "IcoMoon-Free-master/PNG/64px/"
    elif type == "helvetica_num_4x4":
        fontfile = "helveticaneuelight.ttf"
        letters = "0123456789"
        width = 4
        height = 4
    elif type == "helvetica":
        fontfile = "helveticaneuelight.ttf"
        letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"
    if dir == "":
        dir = "dir"
    if out_dir == "":
        out_dir = "out"
    try:
        os.mkdir(dir)
    except:
        pass
    try:
        os.mkdir(out_dir)
    except:
        pass

    if fontfile != "":
        res = convert_font(fontfile, width, height, letters)
    else:
        res = convert_folder(dir, width, height)
    res2 = {}
    for i in res:
        k = os.path.basename(i)[:-4]
        try:
            int(k)
        except:
            res2[k] = res[i]
        else:
            res2[int(k)] = res[i]
    res = res2
