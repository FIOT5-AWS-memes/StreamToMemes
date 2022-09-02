"""
This contains code to superimpose a text onto an image
In other words, it creates the meme
"""

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import math
import pdb
from matplotlib import font_manager as fm

def plsMeme(path, title, caption, outputPath):
    """
    Puts a title and a caption on an image.
    Inputs:
        path        Type: str. Path to image.
        title       Type: str. Title to put on the image.
        caption     Type: str. Caption to put on the image.
        outputPath  Type: str. Path to the outputted image (the meme).
    """


    #   accessory function to print available fonts on the host machine
    system_fonts        = fm.findSystemFonts(fontpaths=None, fontext='ttf')

    #   Read an Image
    img                 = Image.open(path)
    W, H                = img.size[0] , img.size[1]

    top_text            = title
    bottom_text         = caption

    ratio               = 34.3
    top_fontsize        = 35
    bottom_fontsize     = 35

    #   Custom font style and font size
    topFont             = ImageFont.truetype('fonts/ArialTh.ttf', top_fontsize)
    bottomFont          = ImageFont.truetype('fonts/ArialTh.ttf', bottom_fontsize)
    w_top, h_top        = topFont.getsize(top_text)
    w_bottom, h_bottom  = bottomFont.getsize(bottom_text)

    if (w_top > W):
        top_fontsize        = math.floor(ratio / (w_top / W))
        topFont             = ImageFont.truetype('fonts/ArialTh.ttf', top_fontsize)
        w_top, h_top        = topFont.getsize(top_text)

    elif (w_bottom > W):
        bottom_fontsize     = math.floor(ratio / (w_bottom / W))
        bottomFont          = ImageFont.truetype('fonts/ArialTh.ttf', bottom_fontsize)
        w_bottom, h_bottom  = bottomFont.getsize(bottom_text)

    #   Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
    # Add Text to an image
    I1.text(((W-w_top)/2+2, 10), top_text, font=topFont, fill =(0,0,0))
    I1.text(((W-w_top)/2-2, 10), top_text, font=topFont, fill =(0,0,0))
    I1.text(((W-w_top)/2, 10+2), top_text, font=topFont, fill =(0,0,0))
    I1.text(((W-w_top)/2, 10-2), top_text, font=topFont, fill =(0,0,0))
    I1.text(((W-w_top)/2, 10), top_text, font=topFont, fill =(255, 255, 255))

    bottom_text_length  = len(bottom_text)
    count = math.ceil(bottom_text_length / 50)

    bottom_text_in_parts = []
    for i in range(0, count, 50):
        bottom_text_in_parts.append(bottom_text[i*50:i*50+50])

    #   Call draw Method to add 2D graphics in an image
    I1 = ImageDraw.Draw(img)
    #   Add Text to an image
    I1.text(((W-w_bottom)/2+2, (H)-bottom_fontsize), bottom_text, font=bottomFont, fill =(0,0,0))
    I1.text(((W-w_bottom)/2-2, (H)-bottom_fontsize), bottom_text, font=bottomFont, fill =(0,0,0))
    I1.text(((W-w_bottom)/2, (H)-bottom_fontsize+2), bottom_text, font=bottomFont, fill =(0,0,0))
    I1.text(((W-w_bottom)/2, (H)-bottom_fontsize-2), bottom_text, font=bottomFont, fill =(0,0,0))
    I1.text(((W-w_bottom)/2, (H)-bottom_fontsize), bottom_text, font=bottomFont, fill =(255, 255, 255))
     
    #   Save the edited image
    img.save(outputPath)

    return outputPath
    