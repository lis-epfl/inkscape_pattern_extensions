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
    """
    Generate random value folowing a random distribution 1/x**alpha with alpha < -1 
    """
    if alpha >= -1:
        return 0
    ok = False
    while not ok:
        val = limits[0] * pow(np.random.rand(), 1. / (alpha+1))
        if val <= limits[1]:
            ok = True
    return val


class DeadLeaveEffect(inkex.Effect):
    """
    Exemple d'utilisation de la classe Drawing
    """

    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option("--tab",
                action="store", type="string",
                dest="tab")  
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
        self.OptionParser.add_option("--is_periodic",
                action="store", type="inkbool",
                dest="is_periodic", default=False,
                help="Is periodic")
        self.OptionParser.add_option("--periodx",
                action="store", type="float",
                dest="periodx", default=300.0,
                help="Period (horizontal)")
        self.OptionParser.add_option("--periody",
                action="store", type="float",
                dest="periody", default=60.0,
                help="Period (vertical)")
        self.OptionParser.add_option("-c", "--ncolors",
                action="store", type="int",
                dest="ncolors", default=3,
                help="Number of colors")
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
        image_size = self.unittouu( str(self.options.sizex) + unit), self.unittouu( str(self.options.sizey) + unit)
        period = self.unittouu( str(self.options.periodx) + unit), self.unittouu( str(self.options.periody) + unit)
        size_limits = self.unittouu( str(self.options.radmin) + unit), self.unittouu( str(self.options.radmax) +unit)
        num_iter = self.options.iter
        ncolors = self.options.ncolors
        rgba = HTMLColorToRGBA(getColorString(self.options.color))
        rgba2 = HTMLColorToRGBA(getColorString(self.options.color2))
        
        alpha = rgba[3]
        alpha2 = rgba2[3]
        hsva = colorsys.rgb_to_hsv(rgba[0], rgba[1], rgba[2]) + (rgba[3],)
        hsva2 = colorsys.rgb_to_hsv(rgba2[0], rgba2[1], rgba2[2]) + (rgba2[3],)

        hsva_shades = get_hsva_shades(ncolors, hsva, hsva2)
        
        svg = self.document.getroot()
        drawing = Drawing(svg)

        for _ in range(num_iter):
            size = rand_power(-3, size_limits)
            this_hsva = hsva_shades[np.random.randint(0, ncolors)]
            this_rgb = colorsys.hsv_to_rgb(this_hsva[0], this_hsva[1], this_hsva[2])
            
            if self.options.is_periodic == False:
                pos = [ np.random.rand() * image_size[1],
                        np.random.rand() * image_size[0]]
                drawing._createCircle(  pos, 
                                        size, 
                                        style={ "fill-opacity":this_hsva[3]/255.0,
                                            'width':0, 
                                            'fill':RGBToHTMLColor(this_rgb) }
                                        )
            elif self.options.is_periodic == True:
                pos = [ np.random.rand() * period[1],
                        np.random.rand() * period[0] ]
                # Add periodic circle if necessary
                for periodic_pos in [ [pos[0] + i*period[1], pos[1] + j*period[0]] 
                                        for i in np.arange(-1, 1 + image_size[1]//period[1])
                                        for j in np.arange(-1, 1 + image_size[0]//period[0])
                                    ]:
                    # test if the circle is visible in the document
                    if -size < periodic_pos[0] < image_size[1] + size: 
                        if -size < periodic_pos[1] < image_size[0] + size:
                            # Draw circle
                            drawing._createCircle(  periodic_pos, 
                                                    size, 
                                                    style={ "fill-opacity":this_hsva[3]/255.0,
                                                            'width':0, 
                                                            'fill':RGBToHTMLColor(this_rgb) }
                                                    ) 

if __name__ == '__main__':
    effect = DeadLeaveEffect()
    effect.affect()