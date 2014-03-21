#!/usr/bin/env python
# -*- coding: utf8 -*-


import inkex
from simplestyle import formatStyle
import math
import abc




# Fonctionnalité permettant d'afficher des informations,
# ce qui peut être utile lors du développement.
# Il faut alors mettre DEBUG_MODE à True.
# Passer DEBUG_MODE à False permettra de faire fonctionner
# le code développé normalement en désactivant les messages.

DEBUG_MODE = False

def debug(what):
    """
    Permet d'afficher des informations lorsque DEBUG_TRUE est à True.
    Est désactivé lorsque DEBUG_MODE est à False.
    """
    if DEBUG_MODE:
        return inkex.debug(what)
    return what




# Recueil de méthodes de création de noeuds.
class Draftsman(object):
    """
    Permet de renvoyer des formes courantes
    """

    @staticmethod
    def createText(content, (x, y), style={}):
        """Renvoie un texte"""
        text = inkex.etree.Element(inkex.addNS('text','svg'))
        text.text = content
        text.set('x', str(x))
        text.set('y', str(y))
        text.set('style', formatStyle(style))
        return text

    @staticmethod
    def createEllipse((cx, cy), (rx, ry), style={}):
        """Renvoie un ellipse"""
        return inkex.etree.Element(inkex.addNS('ellipse','svg'), {
            'cx'    : str(cx),
            'cy'    : str(cy),
            'rx'    : str(rx),
            'ry'    : str(ry),
            'style' : formatStyle(style),
        })

    @staticmethod
    def createCircle((cx, cy), r, style={}):
        """Renvoie un cercle"""
        return inkex.etree.Element(inkex.addNS('circle','svg'), {
            'cx'    : str(cx),
            'cy'    : str(cy),
            'r'     : str(r),
            'style' : formatStyle(style),
        })

    @staticmethod
    def createRect((x, y), (w, h), style={}):
        """Renvoie un rectangle"""
        return inkex.etree.Element(inkex.addNS('rect','svg'), {
            'x'      : str(x),
            'y'      : str(y),
            'height' : str(h),
            'width'  : str(w),
            'style'  : formatStyle(style),
        })

    @staticmethod
    def createSquare((x, y), c, style={}):
        """Renvoie un carré"""
        return inkex.etree.Element(inkex.addNS('rect','svg'), {
            'x'      : str(x),
            'y'      : str(y),
            'height' : str(c),
            'width'  : str(c),
            'style'  : formatStyle(style),
        })

    @staticmethod
    def createRoundedRect((x, y), (w, h), (rx, ry), style={}):
        """Renvoie un rectangle"""
        return inkex.etree.Element(inkex.addNS('rect','svg'), {
            'x'      : str(x),
            'y'      : str(y),
            'height' : str(h),
            'width'  : str(w),
            'rx'     : str(rx),
            'ry'     : str(ry),
            'style'  : formatStyle(style),
        })

    @staticmethod
    def createRoundedSquare((x, y), c, r, style={}):
        """Renvoie un carré"""
        return inkex.etree.Element(inkex.addNS('rect','svg'), {
            'x'      : str(x),
            'y'      : str(y),
            'height' : str(c),
            'width'  : str(c),
            'rx'     : str(r),
            'ry'     : str(r),
            'style'  : formatStyle(style),
        })

    @staticmethod
    def createLine((x1, y1), (x2, y2), style={}):
        """Renvoie une ligne"""
        return inkex.etree.Element(inkex.addNS('line','svg'), {
            'x1'    : str(x1),
            'y1'    : str(y1),
            'x2'    : str(x2),
            'y2'    : str(y2),
            'style' : formatStyle(style),
        })

    @staticmethod
    def createHLine((x1, x2), y, style={}):
        """Renvoie une ligne horizontale"""
        return inkex.etree.Element(inkex.addNS('line','svg'), {
            'x1'    : str(x1),
            'y1'    : str(y),
            'x2'    : str(x2),
            'y2'    : str(y),
            'style' : formatStyle(style),
        })

    @staticmethod
    def createVLine(x, (y1, y2), style={}):
        """Renvoie une ligne verticale"""
        return inkex.etree.Element(inkex.addNS('line','svg'), {
            'x1'    : str(x),
            'y1'    : str(y1),
            'x2'    : str(x),
            'y2'    : str(y2),
            'style' : formatStyle(style),
        })

    @staticmethod
    def createCube((cx, cy), c, style={}):
        trigo = {
            'cos': "0.8660254037844387",
            'sin': "0.5",
            'tan': "0.5773502691896257",
            'cx1' : str(cx),
            'cy1' : str(cy),
            'cx2' : str(cx-0.8660254037844387*c),
            'cy2' : str(cy-0.5*c),
            'cx3' : str(cx-0.8660254037844387*c),
            'cy3' : str(cy-0.5*c),
        }
        text = inkex.etree.Element(inkex.addNS('text','svg'))
        text.text = str(trigo)
        text.set('x', str(cx))
        text.set('y', str(cy))
        return (
            inkex.etree.Element(inkex.addNS('rect','svg'), {
                'x'      : str(0),
                'y'      : str(0),
                'width'  : str(c),
                'height' : str(c),
                'transform' : 'translate(%(cx1)s %(cy1)s) matrix(%(cos)s,-%(sin)s,0,1,0,0)' % trigo,
                'style'  : formatStyle(style),
            }),
            inkex.etree.Element(inkex.addNS('rect','svg'), {
                'x'      : str(0),
                'y'      : str(0),
                'width'  : str(c),
                'height' : str(c),
                'transform' : 'translate(%(cx2)s %(cy2)s) matrix(%(cos)s,%(sin)s,0,1,0,0)' % trigo,
                'style'  : formatStyle(style),
            }),
            inkex.etree.Element(inkex.addNS('rect','svg'), {
                'x'      : str(0),
                'y'      : str(0),
                'width'  : str(c),
                'height' : str(c),
                'transform' : 'translate(%(cx3)s %(cy3)s) matrix(%(cos)s,-%(sin)s,%(cos)s,%(sin)s,0,0)' % trigo,
                'style'  : formatStyle(style),
            }),
        )




class Marker(object):
    __metaclass__ = abc.ABCMeta

    instances = {}

    def __new__(cls, name):
        # Singletons pour les sous-classes:
        if name in cls.instances:
            return cls.instances[name]
        # Factory
        for sub in cls.__subclasses__():
            if sub.__name__ == name:
                o = object.__new__(sub)
                o.__init__(name)
                cls.instances[name] = o
                return o
        o = object.__new__(DefaultMarker)
        o.__init__(name)
        cls.instances[name] = o
        return o

    def _createMarkerNode(self, node):
        marker_id = self.__class__.__name__
        marker = inkex.etree.SubElement(node ,inkex.addNS('marker','svg'))
        marker.set('id', marker_id)
        marker.set('orient', 'auto')
        marker.set('refX', '0.0')
        marker.set('refY', '0.0')
        marker.set('style', 'overflow:visible')
        marker.set(inkex.addNS('stockid','inkscape'), marker_id)
        return marker

    @abc.abstractmethod
    def _createPathNode(self, node):
        pass

    def __call__(self, node):
        marker = self._createMarkerNode(node)
        path = self._createPathNode(node)
        marker.append(path)
        return marker


class DefaultMarker(Marker):
    """Marqueur par défaut"""

    def _createPathNode(self, node):
        marker = inkex.etree.Element("path")
        marker.set('d', 'M -5.0,-5.0 L -5.0,5.0 L 5.0,5.0 L 5.0,-5.0 L -5.0,-5.0 z ')
        marker.set('transform', 'scale(0.8)')
        marker.set('style', 'fill-rule:evenodd;stroke:#FF0000;stroke-width:1.0pt')
        return marker


class Arrow1Lstart(Marker):
    """Marqueur Arrow1Lstart"""

    def _createPathNode(self, node):
        marker = inkex.etree.Element("path")
        marker.set('d', 'M 0.0,0.0 L 5.0,-5.0 L -12.5,0.0 L 5.0,5.0 L 0.0,0.0 z ')
        marker.set('transform', 'scale(0.8) translate(12.5,0)')
        marker.set('style', 'fill-rule:evenodd;stroke:#000000;stroke-width:1.0pt;marker-start:none')
        return marker


class Arrow1Lend(Marker):
    """Marqueur Arrow1Lend"""

    def _createPathNode(self, node):
        marker = inkex.etree.Element("path")
        marker.set('d', 'M 0.0,0.0 L 5.0,-5.0 L -12.5,0.0 L 5.0,5.0 L 0.0,0.0 z ')
        marker.set('transform', 'scale(0.8) rotate(180) translate(12.5,0)')
        marker.set('style', 'fill-rule:evenodd;stroke:#000000;stroke-width:1.0pt;marker-start:none')
        return marker




class Gradient(object):
    __metaclass__ = abc.ABCMeta

    instances = {}

    def __new__(cls, name):
        # Singletons pour les sous-classes:
        if name in cls.instances:
            return cls.instances[name]
        # Factory
        for sub in cls.__subclasses__():
            if sub.__name__ == name:
                o = object.__new__(sub)
                o.__init__(name)
                cls.instances[name] = o
                return o
        o = object.__new__(DefaultGradient)
        o.__init__(name)
        cls.instances[name] = o
        return o

    links = 0

    def __call__(self, node, coords):
        if self.links == 0:
            self._createStops(node)
        return self._createLink(node, coords)

    @abc.abstractmethod
    def _createStops(self, node):
        pass

    @abc.abstractmethod
    def _createLink(self, node, coords):
        pass


class DefaultGradient(Gradient):
    """Dégradé par défaut"""

    tag = "linearGradient"

    def _createStops(self, node):
        gradient = inkex.etree.SubElement(node ,inkex.addNS(self.tag,'svg'), {
            "id" : self.__class__.__name__,
        })
        inkex.etree.SubElement(gradient, inkex.addNS('stop','svg'), {
            "offset" : "0",
            "style" : "stop-color:#000000;stop-opacity:1;",
        })
        inkex.etree.SubElement(gradient, inkex.addNS('stop','svg'), {
            "offset" : "1",
            "style" : "stop-color:#ffffff;stop-opacity:1;",
        })
        return gradient


    def _createLink(self, node, coords):
        self.links += 1
        link_id = self.__class__.__name__
        return inkex.etree.SubElement(node ,inkex.addNS(self.tag,'svg'), {
            "gradientUnits" : "userSpaceOnUse",
            inkex.addNS("collect", "inkscape") : "always",
            "id" : "%s%02d" % (link_id, self.links),
            inkex.addNS("href", "xlink") : "#%s" % link_id,
            "x1" : str(coords[0][0]),
            "y1" : str((coords[0][1]+coords[1][1])/2),
            "x2" : str(coords[1][0]),
            "y2" : str((coords[0][1]+coords[1][1])/2),
        })


class BlueLinearGradient(Gradient):
    """Dégradé linéaire de bleu"""

    tag = "linearGradient"

    def _createStops(self, node):
        gradient = inkex.etree.SubElement(node ,inkex.addNS(self.tag,'svg'), {
            "id" : self.__class__.__name__,
        })
        inkex.etree.SubElement(gradient, inkex.addNS('stop','svg'), {
            "offset" : "0",
            "style" : "stop-color:#0076ff;stop-opacity:1;",
        })
        inkex.etree.SubElement(gradient, inkex.addNS('stop','svg'), {
            "offset" : "0.125",
            "style" : "stop-color:#1fa8ff;stop-opacity:1;",
        })
        inkex.etree.SubElement(gradient, inkex.addNS('stop','svg'), {
            "offset" : "0.25",
            "style" : "stop-color:#3fdaff;stop-opacity:1;",
        })
        inkex.etree.SubElement(gradient, inkex.addNS('stop','svg'), {
            "offset" : "0.5",
            "style" : "stop-color:#7fffff;stop-opacity:1;",
        })
        inkex.etree.SubElement(gradient, inkex.addNS('stop','svg'), {
            "offset" : "1",
            "style" : "stop-color:#ffffff;stop-opacity:1;",
        })
        return gradient


    def _createLink(self, node, coords):
        self.links += 1
        link_id = self.__class__.__name__
        return inkex.etree.SubElement(node ,inkex.addNS(self.tag,'svg'), {
            "gradientUnits" : "userSpaceOnUse",
            inkex.addNS("collect", "inkscape") : "always",
            "id" : "%s%02d" % (link_id, self.links),
            inkex.addNS("href", "xlink") : "#%s" % link_id,
            "x1" : str(coords[0][0]),
            "y1" : str((coords[0][1]+coords[1][1])/2),
            "x2" : str(coords[1][0]),
            "y2" : str((coords[0][1]+coords[1][1])/2),
        })




class Event(object):
    """Pattern Observable / Observer"""

    def __init__(self, type, content, data={}):
        debug("EVENT (%s): %s" % (type, content))
        self.type = type
        self.content = content
        self.data = data

    def __str__(self):
        return "%s : %s" % (self.type, self.content)


class Observable(object):
    """Pattern Observable / Observer"""

    def __init__(self):
        self.observers = set()

    def addObserver(self, observer):
        self.observers.add(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    def notify(self, event):
        debug("NOTIFY %s" % event)
        for o in self.observers:
            o.update(event)


class Observer(object):
    """Pattern Observable / Observer"""

    def __init__(self, name):
        self.name = name

    @abc.abstractmethod
    def update(self, event):
        pass




class XMLDocument(object):
    """
    Capitalisation des méthodes techniques.
    """

    def __init__(self, root):
        """Initialisation du document"""
        self.root = root

    def findNode(self, path, strict=False):
        try:
            return self.root.xpath(path, namespaces=inkex.NSS)[0]
        except:
            if strict:
                inkex.errormsg(inkex._("No matching node for expression: %s") % path)
            return None




class Defs(XMLDocument, Observer):
    """Définitions du dessin"""

    def __init__(self, root):
        XMLDocument.__init__(self, root)
        Observer.__init__(self, 'defs')
        self.node = self.findNode('/svg:svg//svg:defs')
        if self.node == None:
            self.node = inkex.etree.SubElement(self.svg, inkex.addNS('defs','svg'))

    def _createMarker(self, marker_id):
        """
        Crée une nouvelle définition pour un marqueur
        Seulement s'il n'existe pas déjà
        """
        if self.findNode('/svg:svg//svg:marker[@id="%s"]' % marker_id) is None:
            return Marker(marker_id)(self.node)

    def _createGradient(self, gradient_id, coords):
        """
        Crée une nouvelle définition pour un dégradé
        Chaque utilisation du même dégradé crée une nouvelle définition.
        La première création du dégradé crée les Stops.
        """
        return Gradient(gradient_id)(self.node, coords)

    def update(self, event):
        """
        Permet de rajouter un marqueur au besoin.
        """
        debug("UPDATE Defs")
        if event.type == 'style':
            for k, v in event.content.items():
                if k in ['marker','marker-start','marker-mid','marker-end']:
                    self._createMarker(v[5:-1])
                if k == 'fill' and v[:5] == "url(#":
                    gradient = self._createGradient(v[5:-1], event.data['coords'])
                    event.content['fill'] = "url(#%s)" % gradient.get('id')
                    event.content['fill-opacity'] = "1"
                    event.content['opacity'] = "1"



class Layer(XMLDocument, Observer):
    """Définitions d'un calque"""

    def __init__(self, root, name):
        XMLDocument.__init__(self, root)
        Observer.__init__(self, 'layer')
        self.name = name
        self.node = inkex.etree.SubElement(root, 'g')
        self.node.set(inkex.addNS('label', 'inkscape'), name)
        self.node.set(inkex.addNS('groupmode', 'inkscape'), 'layer')

    def update(self, event):
        """
        Permet de rajouter des objets dans le calque.
        """
        debug("UPDATE Layer: %s" % event.content)
        if event.type == 'append':
            self.node.append(event.content)


class Layers(dict, XMLDocument):
    """Ensemble de calques"""

    def __init__(self, root):
        XMLDocument.__init__(self, root)
        self.current = None

    def addLayer(self, name):
        if name not in self.keys():
            self[name] = Layer(self.root, name)
            self.current = self[name]
        return self.current

    swichLayer = addLayer




class Drawing(XMLDocument, Observable):
    """
    Objet Dessin.
    Dispose des primitives nécessaires pour ajouter des formes.
    """


    def __init__(self, svg):
        """
        Initialisation du dessin avec création d'un calque.
        """
        XMLDocument.__init__(self, svg)
        Observable.__init__(self)
        self.svg = svg

        self.layers = Layers(self.svg)
        self.current_layer = self.layers.addLayer('main')
        self.addObserver(self.current_layer)

        self.defs = Defs(self.svg)
        self.addObserver(self.defs)


    def getSize(self):
        """
        Donne la taille du document courant
        """
        return (inkex.unittouu(self.svg.get('width')),
                 inkex.unittouu(self.svg.get('height')))


    # Actions (utilisant les classes précédentes)
    def _createText(self, content, (x, y), style={}):
        """Rajoute un texte au calque courant"""
        self.notify(Event('style', style, {'coords': ((x, y), (x, y))}))
        self.notify(Event('append', Draftsman.createText(content, (x, y), style)))

    def _createEllipse(self, (cx, cy), (rx, ry), style={}):
        """Rajoute une ellipse au calque courant"""
        ev = Event('style', style, {'coords': ((cx-rx, cy-ry), (cx+rx, cy+ry))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createEllipse((cx, cy), (rx, ry), ev.content)))

    def _createCircle(self, (cx, cy), r, style={}):
        """Rajoute un cercle au calque courant"""
        ev = Event('style', style, {'coords': ((cx-r, cy-r), (cx+r, cy+r))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createCircle((cx, cy), r, ev.content)))

    def _createRect(self, (x, y), (h, w), style={}):
        """Rajoute un rectangle au calque courant"""
        ev = Event('style', style, {'coords': ((x-w/2, y-h/2), (x+w/2, y+h/2))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createRect((x, y), (h, w), ev.content)))

    def _createSquare(self, (x, y), c, style={}):
        """Rajoute un carré au calque courant"""
        ev = Event('style', style, {'coords': ((x-c/2, y-c/2), (x+c/2, y+c/2))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createSquare((x, y), c, ev.content)))

    def _createRoundedRect(self, (x, y), (h, w), (rx, ry), style={}):
        """Rajoute un rectangle au calque courant"""
        ev = Event('style', style, {'coords': ((x-w/2, y-h/2), (x+w/2, y+h/2))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createRoundedRect((x, y), (h, w), (rx, ry), ev.content)))

    def _createRoundedSquare(self, (x, y), c, r, style={}):
        """Rajoute un carré au calque courant"""
        ev = Event('style', style, {'coords': ((x-c/2, y-c/2), (x+c/2, y+c/2))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createRoundedSquare((x, y), c, r, ev.content)))

    def _createLine(self, (x1, y1), (x2, y2), style={}):
        """Rajoute une ligne au calque courant"""
        ev = Event('style', style, {'coords': ((x1, y1), (x2, y2))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createLine((x1, y1), (x2, y2), ev.content)))

    def _createHLine(self, (x1, x2), y, style={}):
        """Rajoute une ligne horizontal au calque courant"""
        ev = Event('style', style, {'coords': ((x1, y), (x2, y))})
        self.notify(ev)
        self.notify(Event('append', Draftsman.createHLine((x1, x2), y, ev.content)))

    def _createVLine(self, x, (y1, y2), style={}):
        """Rajoute une ligne verticale au calque courant"""
        ev = Event('style', style, {'coords': ((x, y1), (x, y2))})
        self.notify(ev)
	self.notify(Event('append', Draftsman.createVLine(x, (y1, y2), ev.content)))

    def _createCube(self, (cx, cy), c, style={}):
        """Rajoute une ligne verticale au calque courant"""
        ev = Event('style', style, {'coords': ((cx-c, cy-c), (cx+c, cy+c))})
        self.notify(ev)
        for face in Draftsman.createCube((cx, cy), c, ev.content):
            self.notify(Event('append', face))




    # Proxies des méthodes précédentes correspondant à un niveau fonctionnel.
    def h1(self, content, (x, y)):
        """
        Rajoute un titre de niveau 1
        """
        self._createText(content, (x, y), {
            'text-align' : 'center',
            'text-anchor' : 'middle',
            'font-size' : '32px',
        })

    def h2(self, content, (x, y)):
        """
        Rajoute un titre de niveau 2
        """
        self._createText(content, (x, y), {
            'text-align' : 'left',
            'text-anchor' : 'middle',
            'font-size' : '24px',
        })

    def h3(self, content, (x, y)):
        """
        Rajoute un titre de niveau 3
        """
        self._createText(content, (x, y), {
            'text-align' : 'left',
            'text-anchor' : 'middle',
            'font-size' : '20px',
            'font-weight' : 'bold',
        })

    def p(self, content, (x, y)):
        """
        Rajoute un paragraphe
        """
        self._createText(content, (x, y), {
            'text-align' : 'left',
            'text-anchor' : 'middle',
            'font-size' : '12px',
        })

    def createEllipse(self, (cx, cy), (rx, ry), fill="#FFFFFF", stroke="#000000", width="1"):
        """
        Rajoute une ellipse avec un fond et une bordure
        dont on peut préciser la couleur
        """
        self._createEllipse((cx, cy), (rx, ry), {
            'fill' : fill,
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createCircle(self, (cx, cy), r, fill="#FFFFFF", stroke="#000000", width="1"):
        """
        Rajoute un cercle avec un fond et une bordure
        dont on peut préciser la couleur
        """
        self._createCircle((cx, cy), r, {
            'fill' : fill,
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createRect(self, (x, y), (h, w), fill="#FFFFFF", stroke="#000000", width="1"):
        """
        Rajoute un cercle avec un fond et une bordure
        dont on peut préciser la couleur
        """
        self._createRect((x, y), (h, w), {
            'fill' : fill,
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createSquare(self, (x, y), c, fill="#FFFFFF", stroke="#000000", width="1"):
        """
        Rajoute un cercle avec un fond et une bordure
        dont on peut préciser la couleur
        """
        self._createSquare((x, y), c, {
            'fill' : fill,
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createRoundedRect(self, (x, y), (h, w), (rx, ry), fill="#FFFFFF", stroke="#000000", width="1"):
        """
        Rajoute un cercle avec un fond et une bordure
        dont on peut préciser la couleur
        """
        self._createRoundedRect((x, y), (h, w), (rx, ry), {
            'fill' : fill,
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createRoundedSquare(self, (x, y), c, r, fill="#FFFFFF", stroke="#000000", width="1"):
        """
        Rajoute un cercle avec un fond et une bordure
        dont on peut préciser la couleur
        """
        self._createRoundedSquare((x, y), c, r, {
            'fill' : fill,
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createLine(self, (x1, y1), (x2, y2), stroke="#000000", width="1"):
        """Rajoute un simple trait"""
        self._createLine((x1, y1), (x2, y2), {
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createHLine(self, (x1, x2), y, stroke="#000000", width="1"):
        """Rajoute un simple trait horizontal"""
        self._createHLine((x1, x2), y, {
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createVLine(self, x, (y1, y2), stroke="#000000", width="1"):
        """Rajoute un simple trait vertical"""
        self._createVLine(x, (y1, y2), {
            'stroke' : stroke,
            'stroke-width' : width,
        })

    def createArrow(self, (x1, y1), (x2, y2), stroke="#000000", width="1"):
        """Rajoute un simple trait"""
        self._createLine((x1, y1), (x2, y2), {
            'stroke' : stroke,
            'marker-start' : 'url(#Arrow1Lstart)',
            'marker-end' : 'url(#Arrow1Lend)',
            'stroke-width' : width,
        })

    def createHArrow(self, (x1, x2), y, stroke="#000000", width="1"):
        """Rajoute un simple trait horizontal"""
        self._createHLine((x1, x2), y, {
            'stroke' : stroke,
            'marker-start' : 'url(#Arrow1Lstart)',
            'marker-end' : 'url(#Arrow1Lend)',
            'stroke-width' : width,
        })

    def createVArrow(self, x, (y1, y2), stroke="#000000", width="1"):
        """Rajoute un simple trait vertical"""
        self._createVLine(x, (y1, y2), {
            'stroke' : stroke,
            'marker-start' : 'url(#Arrow1Lstart)',
            'marker-end' : 'url(#Arrow1Lend)',
            'stroke-width' : width,
        })

    def createCube(self, (cx, cy), c, fill="#FFFFFF", stroke="#000000", width="1"):
        """Rajoute un simple trait vertical"""
        self._createCube((cx, cy), c, {
            'fill' : fill,
            'stroke' : stroke,
            'stroke-width' : width,
        })


