#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Andreas Mussgiller
"""

import importlib.resources as pkg_resources
import xml.etree.ElementTree as ET

import logging

from physeng.singleton import Singleton
from physeng.units import *

from physeng.materials.utilities import MaterialDBException
from physeng.materials.materialproperty import *

class Material():
    
    def __init__(self, name, title, category):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self._logger = logging.getLogger('Material')
        self._logger.debug(f'__init__: {name}, {title}')
        
        self.__Name = name
        self.__Title = title
        self.__Category = category
        self.__Groups = []
        self.__Properties = {}

    def name(self):
        return self.__Name

    def title(self):
        return self.__Title
    
    def properties(self):
        return self.__Properties

    def category(self):
        return self.__Category
    
    def addToGroup(self, group):
        self.__Groups.append(group)
    
    def addProperty(self, prop):
        self._logger.debug(f'addProperty: {prop.name()}')
        self.__Properties[(prop.name(), prop.axis())] = prop
        
    def getProperty(self, prop: str, axis: str = None) -> MaterialProperty:
        if (prop, axis) in self.__Properties:
            return self.__Properties[(prop, axis)]
        raise MaterialDBException(f"Property {prop} {axis} not known to material {self.__Name}")
    
    def _initialize(self):
        for prop in self.__Properties.keys():
            attribName = prop[0]
            if prop[1] is not None:
                attribName += prop[1]
            setattr(self, attribName, self.__Properties[prop].value())

    def __str__(self):
        t =  f"{self.__class__.__name__}\n"
        t += f"Name:     {self.__Name}\n"
        t += f"Title:    {self.__Title}\n"
        t += f"Category: {self.__Category}\n"
        t += "Groups:   "
        for i,g in enumerate(self.__Groups):
            if i > 0:
                t += ', '
            t += g
        t += "\n"
        t += "Properties:\n"
        for n,p in self.__Properties.items():
            p = str(p).replace('\n', '\n  ')
            t += '  ' + p + '\n'
        return t

class IsotropicMaterial(Material):
    def __init__(self, name, title, category):
        super().__init__(name, title, category)
        self._logger.name = 'IsotropicMaterial'
        self._logger.debug(f'__init__: {name}, {title}')

class OrthotropicMaterial(Material):
    def __init__(self, name, title, category):
        super().__init__(name, title, category)
        self._logger.name = 'OrthotropicMaterial'
        self._logger.debug(f'__init__: {name}, {title}')
