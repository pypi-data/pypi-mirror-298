#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: mussgill
"""

import yaml
import importlib.resources as pkg_resources
import xml.etree.ElementTree as ET

import logging

from physeng.singleton import Singleton
from physeng.units import *

from physeng.materials.utilities import MaterialDBException
from physeng.materials.materialproperty import *
from physeng.materials.material import *

class MaterialDB(metaclass=Singleton):
    def __init__(self):
        logging.basicConfig(format="{asctime} [{levelname}:{name}]: {message}",
                            style="{",
                            datefmt="%Y-%m-%d %H:%M",
                            level=logging.INFO)
        self.__logger = logging.getLogger('MaterialDB')

        self.__logger.debug('__init__')
        
        self.__materials = []
        self.__materialsByName = {}
        self.__materialsByTitle = {}
        self.__groups = {}
        self.__categories = {}
        self.__groupsByCategory = {}
        
        self.__readDB()
    
    def getMaterials(self) -> list[Material]:
        return self.__materials
        
    def getMaterial(self, name: str) -> Material:
        return self.getMaterialByName(name)
    
    def getMaterialByName(self, name: str) -> Material:
        if name not in self.__materialsByName:
            raise MaterialDBException(f"Material '{name}' (name) not found")
        return self.__materialsByName[name]
    
    def getMaterialByTitle(self, title: str) -> Material:
        if title not in self.__materialsByTitle:
            raise MaterialDBException(f"Material '{title}' (title) not found")
        return self.__materialsByTitle[title]

    def getGroups(self) -> list[str]:
        return list(self.__groups.keys())

    def getGroupsForCategory(self, category: str) -> list[str]:
        return self.__groupsByCategory[category]

    def getMaterialsForGroup(self, group: str) -> list[Material]:
        if group not in self.__groups:
            return []
        return self.__groups[group]

    def getCategories(self) -> list[str]:
        return list(self.__categories.keys())

    def getMaterialsForCategory(self, category: str) -> list[Material]:
        if category not in self.__categories:
            return []
        return self.__categories[category]
    
    def __processMaterial(self, material):
        props = material.properties()

        if all(x in props for x in [('DynamicViscosity', None),
                                    ('Density', None)]):
            dynamicviscosityProp = props[('DynamicViscosity', None)]
            
            if (isinstance(dynamicviscosityProp, MaterialProperty) and 
                not isinstance(dynamicviscosityProp, DerivedMaterialProperty)):
                dynamicviscosity = dynamicviscosityProp.value()
                Tref = dynamicviscosityProp.referencetemperature()
                density = props[('Density', None)].value()
            
                kinematicviscosity = dynamicviscosity / density
            
                prop = DerivedMaterialProperty('KinematicViscosity',
                                               kinematicviscosity,
                                               Tref,
                                               None)
                material.addProperty(prop)
            
            if (isinstance(dynamicviscosityProp, TemperatureDependentMaterialProperty) and 
                not isinstance(dynamicviscosityProp, DerivedTemperatureDependentMaterialProperty)):
                dynamicviscosity = dynamicviscosityProp.values()
                Tref = dynamicviscosityProp.referencetemperatures()
                density = props[('Density', None)].value()
                
                tvs = {}
                for t,v in zip(Tref, dynamicviscosity):
                    kinematicviscosity = v / density
                    tvs[t] = kinematicviscosity
                prop = DerivedTemperatureDependentMaterialProperty('KinematicViscosity',
                                                                   tvs)
                material.addProperty(prop)

        if all(x in props for x in [('KinematicViscosity', None),
                                    ('Density', None)]):
            kinematicviscosityProp = props[('KinematicViscosity', None)]
            if (isinstance(kinematicviscosityProp, MaterialProperty) and
                not isinstance(kinematicviscosityProp, DerivedMaterialProperty)):
                kinematicviscosity = kinematicviscosityProp.value()
                Tref = kinematicviscosityProp.referencetemperature()
                density = props[('Density', None)].value()
            
                dynamicviscosity = kinematicviscosity * density
            
                prop = DerivedMaterialProperty('DynamicViscosity',
                                               dynamicviscosity,
                                               Tref,
                                               None)
                material.addProperty(prop)

        material._initialize()
        
    def __processFile(self, xmlfile):
        try:
            self.__logger.debug(f'processing {xmlfile}')
            tree = ET.parse(xmlfile)
            root = tree.getroot()
            for child in root:
                self.__logger.debug(f'processing {child.tag}')
                
                name = child.find('Name').text
                title = child.find('Title').text
                category = child.find('Category').text
                
                if child.tag == 'IsotropicMaterial':
                    material = IsotropicMaterial(name, title, category)
                elif child.tag == 'OrthotropicMaterial':
                    material = OrthotropicMaterial(name, title, category)
                else:
                    print(child.tag)
                    continue
                
                groups = child.find('Groups')
                if groups is not None:
                    for group in groups:
                        if group.text not in self.__groups:
                            self.__groups[group.text] = []
                        if category not in self.__groupsByCategory:
                            self.__groupsByCategory[category] = []
                        self.__groups[group.text].append(material)
                        material.addToGroup(group.text)
                        self.__groupsByCategory[category].append(group)
                
                props = child.find('Properties')
                if props is not None:
                    for prop in props:
                        if prop.find('Value') is None:
                            p = MaterialProperty.fromXML(prop)
                        else:
                            p = TemperatureDependentMaterialProperty.fromXML(prop)
                        material.addProperty(p)
                
                self.__processMaterial(material)
                
                if category not in self.__categories:
                    self.__categories[category] = []
                self.__categories[category].append(material)
                
                self.addMaterial(material)
        except:
            raise MaterialDBException(f"could not process file {xmlfile}")
        
    def __readDB(self):
        with open( pkg_resources.files('physeng.data').joinpath('MaterialDB.yaml')) as file:
            steeringfile = yaml.safe_load(file)
        filenames = steeringfile['filenames']
        
        for filename in filenames:
            self.__logger.debug(f'reading {filename}')
            xmlfile = pkg_resources.files('physeng.data').joinpath(filename)
            self.__processFile(xmlfile)
    
    def addMaterial(self, material):
        self.__materials.append(material)
        self.__materialsByName[material.name()] = material
        self.__materialsByTitle[material.title()] = material
        self.__logger.debug(f'addMaterial: {material.name()}, {material.title()}')


if __name__ == '__main__':
    matDB = MaterialDB()
    
    #for mat in matDB.getMaterials():
    #    print(f"{mat.name():30}")
        
    
 