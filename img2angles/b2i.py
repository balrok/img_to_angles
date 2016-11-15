#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PIL import Image, ImageDraw, ImageFont, ImageOps
from img2angle import all_angles_mp
import time
import os
#from fontTools.ttLib import TTFont
#from tqdm import tqdm

def createImg(symbol, name, fontfile):
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

def convert_font():
    # ttf = TTFont(fontfile, 0, verbose=0, allowVID=0, ignoreDecompileErrors=True, fontNumber=-1)
    for letter in letters:
        createImg(letter, letter, fontfile)
    return all_angles_mp(["%s/%s.png"%(dir, letter) for letter in letters]
                         , out_dir=out_dir, invert=True, edge=150, filter=14, alphacolor=255, size=(g_width, g_height))

def convert_folder():
    # -4 removes file ending
    chars = [x[:-4] for x in os.listdir(dir)]
    return all_angles_mp(["%s/%s.png"%(dir, x) for x in chars]
                           , out_dir=out_dir, invert=True, edge=150, filter=14, alphacolor=255, size=(g_width, g_height))

if __name__ == "__main__":

    type = "helvetica"

    fontfile = ""
    letters = ""
    g_width = 10
    g_height = 10
    dir = ""
    out_dir = ""

    if type == "IcoMoon":
        fontfile = "" #IcoMoon-Free.ttf"
        dir = "IcoMoon-Free-master/PNG/64px/"
    elif type == "helvetica_num_4x4":
        fontfile = "helveticaneuelight.ttf"
        letters = "0123456789"
        g_width = 4
        g_height = 4
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
        res = convert_font()
    else:
        res = convert_folder()
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
