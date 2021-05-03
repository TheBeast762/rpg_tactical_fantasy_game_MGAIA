#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import xml.etree.ElementTree as ET
import os
import random
from src.game_entities.foe import Foe


# CUR_DIR = os.getcwd()

def f(lvl: float):
    tree = ET.parse(f'data/foes/foes{lvl}.xml')
    root = tree.getroot()
    all_foe_tags = [foe.tag for foe in root]
    n_foes = int(6 * lvl + 7)
    selected_foes_tags = random.choices(all_foe_tags, k=n_foes)
    foes = []
    for foe_tag in selected_foes_tags:
        foe_info = root.find(foe_tag)
        if foe_info.find('reach') is None:
            reach = []
        else:
            reach = [int(i) for i in foe_info.find('reach').text.strip().split(',')]

        if foe_info.find('keywords') is None:
            keywords = []
        else:
            keywords = [i for i in foe_info.find('keywords').text.strip().split(',')]
        print('C:\\Users\\georg\\rpg_tactical_fantasy_game\\imgs\\dungeon_crawl\\monster\\' + '\\'.join(foe_info.find('sprite').text.strip().split('/')))
        foe = Foe(foe_info.tag,
                  (1, 1),
                  'C:\\Users\\georg\\rpg_tactical_fantasy_game\\imgs\\dungeon_crawl\\monster\\' + '\\'.join(foe_info.find('sprite').text.strip().split('/')),
                  int(foe_info.find('hp').text),
                  int(foe_info.find('defense').text),
                  int(foe_info.find('resistance').text),
                  int(foe_info.find('move').text),
                  int(foe_info.find('strength').text),
                  foe_info.find('attack_kind').text.strip(),
                  foe_info.find('strategy').text.strip(),
                  reach,
                  int(foe_info.find('xp_gain').text),
                  [],
                  keywords
                  )
        foes.append(foe)

    return foes

f(0.5)

