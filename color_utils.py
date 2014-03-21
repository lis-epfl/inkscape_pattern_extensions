import numpy as np
import colorsys

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

def get_hsv_shades(shades, hsv, hsv2=(0, 0, 255)):
    hue = np.linspace(hsv[0], hsv2[0], shades)
    saturation = np.linspace(hsv[1], hsv2[1], shades)
    value = np.linspace(hsv[2], hsv2[2], shades)
    return [(h, s, v) for h, s, v in zip(hue, saturation, value)]