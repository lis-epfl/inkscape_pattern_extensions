#!/usr/bin/env python
# -*- coding: utf8 -*-


import csv, os

import inkex
from simplestyle import *
from inkpyration import Drawing
from color_utils import *
import gettext
import colorsys

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

class DeadLeaveEffect(inkex.Effect):
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
        self.OptionParser.add_option("-r", "--radmin",
                action="store", type="float",
                dest="radmin", default=0.5,
                help="Minimum circle radius")
        self.OptionParser.add_option("-R", "--radmax",
                action="store", type="float",
                dest="radmax", default=60.0,
                help="Maximum circle radius")
        self.OptionParser.add_option("-i", "--iter",
                action="store", type="int",
                dest="iter", default=10000,
                help="Number of circles")
        self.OptionParser.add_option("-a", "--alpha",
                action="store", type="int",
                dest="alpha", default=-2,
                help="Alpha (power law distribution)")
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
        if self.options.radmin > self.options.radmax:
            self.options.radmin, self.options.radmax = self.options.radmax, self.options.radmin

    def effect(self):
        """
        Methode principale
        """
        self.validate_inputs()

        unit = self.options.unit
        image_size = inkex.unittouu( str(self.options.sizex) + unit), inkex.unittouu( str(self.options.sizey) + unit)
        size_limits = inkex.unittouu( str(self.options.radmin) + unit), inkex.unittouu( str(self.options.radmax) +unit)
        num_iter = self.options.iter
        alpha = self.options.alpha
        colors = self.options.colors
        rgb = HTMLColorToRGB(getColorString(self.options.color))
        hsv = colorsys.rgb_to_hsv(rgb[0], rgb[1], rgb[2])
        rgb2 = HTMLColorToRGB(getColorString(self.options.color2))
        hsv2 = colorsys.rgb_to_hsv(rgb2[0], rgb2[1], rgb2[2])

        svg = self.document.getroot()
        drawing = Drawing(svg)

        shades = get_hsv_shades(colors, hsv, hsv2)

        for _ in range(num_iter):
            pos = [np.random.rand() * image_size[1],
                   np.random.rand() * image_size[0]]
            size = rand_power(alpha, size_limits)
            this_hsv = shades[np.random.randint(0, colors)]
            this_rgb = colorsys.hsv_to_rgb(this_hsv[0], this_hsv[1], this_hsv[2])
            drawing.createCircle(pos, size, width=0, 
                                fill=RGBToHTMLColor(this_rgb))

if __name__ == '__main__':
    effect = DeadLeaveEffect()
    effect.affect()