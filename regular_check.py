#!/usr/bin/env python
# -*- coding: utf8 -*-


import csv, os

import inkex
from simplestyle import *
from inkpyration import Drawing
import gettext


import numpy as np


_ = gettext.gettext

def rand_power(alpha, limits):
    if alpha >= 0:
        return 0
    ok = False
    while not ok:
        val = limits[0] * pow(np.random.rand(), 1. / alpha)
        if val <= limits[1]:
            ok = True
    return val

def unsignedLong(signedLongString):
    longColor = long(signedLongString)
    if longColor < 0:
        longColor = longColor & 0xFFFFFFFF
    return longColor
    #A*256^0 + B*256^1 + G*256^2 + R*256^3

def getColorString(longColor):
    longColor = unsignedLong(longColor)
    hexColor = hex(longColor)[2:-3]
    hexColor = hexColor.rjust(6, '0')
    return '#' + hexColor.upper()

def RGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def HTMLColorToRGB(colorstring):
    """ convert #RRGGBB to an (R, G, B) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': 
        colorstring = colorstring[1:]
    if len(colorstring) != 6:
        raise ValueError, "input #%s is not in #RRGGBB format" % colorstring
    # r, g, b, a = colorstring[:2], colorstring[2:4], colorstring[4:6], colorstring[6:]
    # r, g, b = [int(n, 16)*int(a, 16)/255 for n in (r, g, b)]
    r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:6]
    r, g, b = [int(n, 16) for n in (r, g, b)]
    return (r, g, b)


class RegCheckEffect(inkex.Effect):
    """
    Exemple d'utilisation de la classe Drawing
    """

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option('-u', '--unit',
                action='store',type='string',
                dest='unit',default='mm',help='Unit')
        self.OptionParser.add_option("-x", "--sizex",
                action="store", type="float",
                dest="sizex", default=60.0,
                help="Image size (vertical)")
        self.OptionParser.add_option("-y", "--sizey",
                action="store", type="float",
                dest="sizey", default=300.0,
                help="Image size (horizontal)")
        self.OptionParser.add_option("--ssizex",
                action="store", type="float",
                dest="ssizex", default=20.0,
                help="Squares size (vertical)")
        self.OptionParser.add_option("--ssizey",
                action="store", type="float",
                dest="ssizey", default=20.0,
                help="Squares size (vertical)")
        self.OptionParser.add_option("-w", "--color",
                action="store", type="string",
                dest="color", default="0",
                help="Color")
        self.OptionParser.add_option("-v", "--color2",
                action="store", type="string",
                dest="color2", default="0",
                help="Color")

    def validate_inputs(self):
        """Parameters validation"""
        if self.options.ssizex > self.options.sizex:
            self.options.ssizex, self.options.sizex = self.options.sizex, self.options.ssizex
        if self.options.ssizey > self.options.sizey:
            self.options.ssizey, self.options.sizey = self.options.sizey, self.options.ssizey

    def effect(self):
        """
        Methode principale
        """
        self.validate_inputs()

        unit = self.options.unit
        image_size = inkex.unittouu( str(self.options.sizey) + unit), inkex.unittouu( str(self.options.sizex) + unit)
        square_size = inkex.unittouu( str(self.options.ssizey) + unit), inkex.unittouu( str(self.options.ssizex) + unit)
        rgb = HTMLColorToRGB(getColorString(self.options.color))
        rgb2 = HTMLColorToRGB(getColorString(self.options.color2))

        svg = self.document.getroot()
        drawing = Drawing(svg)

        i =  0
        for x in np.arange(0, image_size[0], square_size[0]):
            i += 1
            j = 0
            for y in np.arange(0, image_size[1], square_size[1]):
                j += 1
                flip = (i+j)%2
                # color = 255.0 * flip
                if flip:
                    this_rgb = rgb
                else:
                    this_rgb = rgb2
                drawing.createRect((x, y), square_size, fill=RGBToHTMLColor(this_rgb), 
                    stroke=RGBToHTMLColor(this_rgb), width="1")

if __name__ == '__main__':
    effect = RegCheckEffect()
    effect.affect()