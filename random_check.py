#!/usr/bin/env python
# -*- coding: utf8 -*-


import csv, os

import inkex
from simplestyle import *
from inkpyration import Drawing
import gettext
import colorsys
from color_utils import *

import numpy as np


_ = gettext.gettext


class RandCheckEffect(inkex.Effect):
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
        self.OptionParser.add_option("-c", "--colors",
                action="store", type="int",
                dest="colors", default=3,
                help="Number of grayscales")
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
        image_size = self.unittouu( str(self.options.sizey) + unit), self.unittouu( str(self.options.sizex) + unit)
        square_size = self.unittouu( str(self.options.ssizey) + unit), self.unittouu( str(self.options.ssizex) + unit)
        colors = self.options.colors
        rgb = HTMLColorToRGB(getColorString(self.options.color))
        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        rgb2 = HTMLColorToRGB(getColorString(self.options.color2))
        hsv2 = colorsys.rgb_to_hsv(rgb2[0], rgb2[1], rgb2[2])

        svg = self.document.getroot()
        drawing = Drawing(svg)

        shades = get_hsv_shades(colors, hsv, hsv2)

        for x in np.arange(0, image_size[0], square_size[0]):
            for y in np.arange(0, image_size[1], square_size[1]):
                this_hsv = shades[np.random.randint(0, colors)]
                this_rgb = colorsys.hsv_to_rgb(this_hsv[0], this_hsv[1], this_hsv[2])
                drawing.createRect((x, y), square_size, fill=RGBToHTMLColor(this_rgb), 
                    stroke=RGBToHTMLColor(this_rgb),width="1")

if __name__ == '__main__':
    effect = RandCheckEffect()
    effect.affect()