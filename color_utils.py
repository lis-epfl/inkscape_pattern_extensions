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
    hexColor = hex(longColor)[2:-1]
    hexColor = hexColor.rjust(6, '0')
    return '#' + hexColor.upper()

def RGBToHTMLColor(rgba_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgba_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor

def HTMLColorToRGBA(colorstring):
    """ convert #RRGGBBAA to an (R, G, B, A) tuple """
    colorstring = colorstring.strip()
    if colorstring[0] == '#': 
        colorstring = colorstring[1:]
    if len(colorstring) == 6:
        r, g, b = colorstring[:2], colorstring[2:4], colorstring[4:6]
        r, g, b, a = [int(n, 16) for n in (r, g, b, 'ff')]
    elif len(colorstring) == 8:
        r, g, b, a = colorstring[:2], colorstring[2:4], colorstring[4:6], colorstring[6:]
        r, g, b, a = [int(n, 16) for n in (r, g, b, a)]
    else:
        raise ValueError, "input #%s is not in #RRGGBB or #RRGGBBAA format" % colorstring
    return (r, g, b, a)

def get_hsva_shades(shades, hsva, hsva2=(0, 0, 255, 255)):
    hue = np.linspace(hsva[0], hsva2[0], shades)
    saturation = np.linspace(hsva[1], hsva2[1], shades)
    value = np.linspace(hsva[2], hsva2[2], shades)
    alpha = np.linspace(hsva[3], hsva2[3], shades)
    return [(h, s, v, a) for h, s, v, a in zip(hue, saturation, value, alpha)]