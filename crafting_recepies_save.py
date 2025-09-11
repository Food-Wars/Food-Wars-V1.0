# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 13:31:29 2024

"""
import json

crafting_recepies = [
    [0,1,0,0,1,0,0,0,0,8],
    [0,8,0,8,3,8,0,3,0,6],
    [0,9,0,9,3,9,0,3,0,8],
    [8,8,0,8,3,0,0,3,0,4],
    [9,9,0,9,3,0,0,3,0,5],

    
    ]

crafting_recepies = {
                    "planks_recepie": [[0,1,0,0,1,0,0,0,0], [8, 2]],
                    "wooden_axe_recepie": [[8,8,0,8,3,0,0,3,0], [4, 1]],
                    "stone_axe_recepie": [[9,9,0,9,3,0,0,3,0], [5, 1]],
                    "wooden_pickaxe_recepie": [[0,8,0,8,3,8,0,3,0], [6, 1]],
                    "stone_pickaxe_recepie": [[0,9,0,9,3,9,0,3,0], [7, 1]],
                    "sharp_stick_recepie": [[0,3,0,0,3,0,0,0,0], [10, 1]],
                    "suger_cloth_recepie": [[11,11,0,11,11,0,0,0,0], [12, 2]],
                    "suger_cloth_boots_recepie": [[0,0,0,12,0,12,12,0,12], [13, 1]],
                    "suger_cloth_pants_recepie": [[12,12,12,12,0,12,12,0,12], [14, 1]],
                    "suger_cloth_chestplate_recepie": [[12,0,12,12,12,12,12,12,12], [15, 1]],
                    "suger_cloth_helmet_recepie": [[12,12,12,12,0,12,0,0,0], [16, 1]],
                    }

with open('C:/Users/zrobi/Documents/Python Scripts/Food Wars/V_1.0/game_files/crafting/crafting_recepies.json', "w") as file:
    json.dump(crafting_recepies, file)
    
print('Saved!')