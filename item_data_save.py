# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 07:22:12 2024

@author: zrobi
"""

import json

#1: item name
#2: item_img_index id
#3: stackable
#4: item destory type
#5: item destory time
#6: damage addition
#7: protection
#8: throwable

item_data = {
            0: ["", 0, True],
            1: ["Log", 1, True],
            2: ["Rock", 2, True],
            3: ["Stick", 3, True],
            4: ["Wooden Axe", 4, False, "wood", 1, 2],
            5: ["Stone Axe", 5, False, "wood", 2, 3],
            6: ["Wooden Pickaxe", 6, False, "stone", 1, 1],
            7: ["Stone Pickaxe", 7, False, "stone", 2, 2],
            8: ["Wooden Planks", 8, True],
            9: ["Cobblestone", 9, True],
            10: ["Sharp Stick", 10, False, "wood", 0, 1],
            11: ["Suger String", 11, True],
            12: ["Suger Cloth", 12, True],
            13: ["Suger Cloth Boots", 13, False, "none", 0, 0, 2],
            14: ["Suger Cloth Pants", 14, False, "none", 0, 0, 4],
            15: ["Suger Cloth Chestplate", 15, False, "none", 0, 0, 6],
            16: ["Suger Cloth Helmet", 16, False, "none", 0, 0, 2],
            17: ["Red Gelatin", 17, False, "none", 0, 0, 0, True],
            18: ["Green Gelatin", 18, False, "none", 0, 0, 0, True],
            19: ["Blue Gelatin", 19, False, "none", 0, 0, 0, True],
            20: ["Yellow Gelatin", 20, False, "none", 0, 0, 0, True],
            }


with open('C:/Users/zrobi/Documents/Python Scripts/Food Wars/V_1.0/game_files/item_data/item_data.json', "w") as file:
    json.dump(item_data, file) 
print('Saved!')               