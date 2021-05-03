# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 11:42:31 2021

@author: Tejan
"""

import xml.etree.ElementTree as ET
import os 


CUR_DIR = os.getcwd()

def load_character_xml(level):
    level = str(level)
    filepath = CUR_DIR+'/data/characters/'+'level_0_'+level+'.xml'
    tree = ET.parse(filepath)
    root = tree.getroot()
    #variable file contains the data from xml file
    #return file if you want to see xml file as well
    with open(filepath, 'r') as f:
        file = f.read()
    return root, file   

root1, file = load_character_xml(10)

#in case of reading file as well
#root1, file = load_character_xml(10)

for child in root1:
    print(child.tag, child.attrib)                                                              

