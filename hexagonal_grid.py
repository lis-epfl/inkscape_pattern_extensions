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

class HexagonalGridEffect(inkex.Effect):
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
        self.OptionParser.add_option("--grid_size",
                action="store", type="float",
                dest="grid_size", default=100.0,
                help="Grid size (distance between points)")
        self.OptionParser.add_option("--marker_size",
                action="store", type="float",
                dest="marker_size", default=10.0,
                help="Marker size")
        self.OptionParser.add_option("--offsety",
                action="store", type="float",
                dest="offsety", default=0.0,
                help="Horizontal offset")
        self.OptionParser.add_option("--offsetx",
                action="store", type="float",
                dest="offsetx", default=0.0,
                help="Vertical offset")


    def validate_inputs(self):
        """Parameters validation"""
        pass

    def get_grid_points(self, image_size, grid_size):
        points_a = np.array([ [x, y] for y in np.arange(0.0, image_size[1], grid_size*np.sqrt(3))
                                     for x in np.arange(0.0, image_size[0], grid_size) 
                            ])
        points_b = np.array([ [x, y] for y in np.arange(grid_size* np.sqrt(3) / 2.0, image_size[1], grid_size*np.sqrt(3))
                                     for x in np.arange(0.5*grid_size, image_size[0], grid_size) 
                        ])
        if points_a.shape[0] != 0 and points_b.shape[0] != 0:
            points = np.vstack([points_a, points_b])
        else:
            points = np.array([0,0])
        return points


    def effect(self):
        """
        Methode principale
        """
        self.validate_inputs()

        unit = self.options.unit
        image_size = self.unittouu( str(self.options.sizey) + unit), self.unittouu( str(self.options.sizex) + unit)
        grid_size = self.unittouu( str(self.options.grid_size) + unit)
        offset = self.unittouu( str(self.options.offsety) + unit), self.unittouu( str(self.options.offsetx) + unit)
        marker_size = self.unittouu( str(self.options.marker_size) + unit)

        svg = self.document.getroot()
        drawing = Drawing(svg)

        points = self.get_grid_points(image_size, grid_size)
        points = points + np.ones([points.shape[0], 2]) * np.array(offset[:])

        for point in points:
            drawing.createSquare(point, marker_size, fill="#000000", stroke="#000000", width="0")
        

     

if __name__ == '__main__':
    effect = HexagonalGridEffect()
    effect.affect()