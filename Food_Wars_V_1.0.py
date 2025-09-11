# -*- coding: utf-8 -*-
"""
Created on Thu Aug  1 08:12:39 2024

"""

#import modules
import pygame
from pygame import mixer
from os import path
import random
import opensimplex
import json
import pyperclip
import math

#initalise modules
pygame.init()
#initalise mixer
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()

#game variables
tile_size = 16
fps = 30
true_scroll = [0,0]
chunk_size = 8
game_state = 6
debug = False
creation_difficulty = 0
settings_difficulty = 0
world_seed = 0
save_timer = 0
world_num = 0
delete_state = 0
settings_state = 1
ingame_settings_state = 1
debug_menu = False
entities = []
projectiles = []
devtools_keybinds = False
chunk_borders_debug = False

#define screen
screen_height = 600
screen_width = 600
screen = pygame.display.set_mode((screen_width, screen_height))


#load images tiles
grass = pygame.image.load('game_files/imgs/tiles/grass.png')
water = pygame.image.load('game_files/imgs/tiles/water.png')
tree_unscaled = pygame.image.load('game_files/imgs/tiles/tree.png')
tree = pygame.transform.scale(tree_unscaled, (tile_size * 2, tile_size * 4))
rock_unscaled = pygame.image.load('game_files/imgs/tiles/rock.png')
rock = pygame.transform.scale(rock_unscaled, (tile_size * 1.5, tile_size * 1.5))
cobblestone_unscaled = pygame.image.load('game_files/imgs/tiles/cobblestone.png')
cobblestone = pygame.transform.scale(cobblestone_unscaled, (tile_size * 1.5, tile_size * 1.5))
log_unscaled = pygame.image.load('game_files/imgs/tiles/log.png')
log = pygame.transform.scale(log_unscaled, (tile_size * 1.5, tile_size * 1.5))
stick_unscaled = pygame.image.load('game_files/imgs/tiles/stick.png')
stick = pygame.transform.scale(stick_unscaled, (tile_size * 1.5, tile_size * 1.5))
suger_string_unscaled = pygame.image.load('game_files/imgs/tiles/suger_string.png')
suger_string = pygame.transform.scale(suger_string_unscaled, (tile_size * 1.5, tile_size * 1.5))
red_gelatin_unscaled = pygame.image.load('game_files/imgs/tiles/gelatin_red_projectile.png')
red_gelatin = pygame.transform.scale(red_gelatin_unscaled, (tile_size * 1.5, tile_size * 1.5))
green_gelatin_unscaled = pygame.image.load('game_files/imgs/tiles/gelatin_green_projectile.png')
green_gelatin = pygame.transform.scale(green_gelatin_unscaled, (tile_size * 1.5, tile_size * 1.5))
blue_gelatin_unscaled = pygame.image.load('game_files/imgs/tiles/gelatin_blue_projectile.png')
blue_gelatin = pygame.transform.scale(blue_gelatin_unscaled, (tile_size * 1.5, tile_size * 1.5))
yellow_gelatin_unscaled = pygame.image.load('game_files/imgs/tiles/gelatin_yellow_projectile.png')
yellow_gelatin = pygame.transform.scale(yellow_gelatin_unscaled, (tile_size * 1.5, tile_size * 1.5))
#load images gui
inventory_slot = pygame.image.load('game_files/imgs/gui/inventory_slot.png')
inventory_bg = pygame.image.load('game_files/imgs/gui/inventory_background.png')
respawn_bg = pygame.image.load('game_files/imgs/gui/respawn_bg.png')
icon_img = pygame.image.load('game_files/imgs/gui/cupcake_icon.png')
world_select_bg = pygame.image.load('game_files/imgs/gui/world_selection_bg.png')
world_select_bg = pygame.transform.scale(world_select_bg, (tile_size * 29, tile_size * 20))
settings_bg = pygame.image.load('game_files/imgs/menu/settings_bg.png')
keybinds_display = pygame.image.load('game_files/imgs/menu/keybinds_selector.png')
logo = pygame.image.load('game_files/imgs/menu/logo.png')
logo = pygame.transform.scale(logo, (555, 93))
logo_rect = logo.get_rect()
logo_rect.centerx = 300
logo_rect.centery = 100
#load images items
item_empty = pygame.image.load('game_files/imgs/items/item_empty.png')
item_empty = pygame.transform.scale(item_empty, (tile_size *3, tile_size * 3))
log_item = pygame.image.load('game_files/imgs/items/log_img.png')
log_item = pygame.transform.scale(log_item, (tile_size *3, tile_size * 3))
rock_item = pygame.image.load('game_files/imgs/items/rock_img.png')
rock_item = pygame.transform.scale(rock_item, (tile_size *3, tile_size * 3))
stick_item = pygame.image.load('game_files/imgs/items/stick_img.png')
stick_item = pygame.transform.scale(stick_item, (tile_size *3, tile_size * 3))
wooden_axe_img = pygame.image.load('game_files/imgs/items/wooden_axe.png')
wooden_axe_img = pygame.transform.scale(wooden_axe_img, (tile_size *3, tile_size * 3))
stone_axe_img = pygame.image.load('game_files/imgs/items/stone_axe.png')
stone_axe_img = pygame.transform.scale(stone_axe_img, (tile_size *3, tile_size * 3))
wooden_pickaxe_img = pygame.image.load('game_files/imgs/items/wooden_pickaxe.png')
wooden_pickaxe_img = pygame.transform.scale(wooden_pickaxe_img, (tile_size *3, tile_size * 3))
stone_pickaxe_img = pygame.image.load('game_files/imgs/items/stone_pickaxe.png')
stone_pickaxe_img = pygame.transform.scale(stone_pickaxe_img, (tile_size *3, tile_size * 3))
wooden_planks_img = pygame.image.load('game_files/imgs/items/wood_planks.png')
wooden_planks_img = pygame.transform.scale(wooden_planks_img, (tile_size *3, tile_size * 3))
cobblestone_img = pygame.image.load('game_files/imgs/items/cobblestone_img.png')
cobblestone_img = pygame.transform.scale(cobblestone_img, (tile_size *3, tile_size * 3))
sharp_stick_img = pygame.image.load('game_files/imgs/items/sharp_stick_img.png')
sharp_stick_img = pygame.transform.scale(sharp_stick_img, (tile_size *3, tile_size * 3))
suger_string_img = pygame.image.load('game_files/imgs/items/suger_string_img.png')
suger_string_img = pygame.transform.scale(suger_string_img, (tile_size *3, tile_size * 3))
suger_cloth_img = pygame.image.load('game_files/imgs/items/suger_cloth_img.png')
suger_cloth_img = pygame.transform.scale(suger_cloth_img, (tile_size *3, tile_size * 3))
suger_cloth_boots_img = pygame.image.load('game_files/imgs/items/suger_cloth_boots_img.png')
suger_cloth_boots_img = pygame.transform.scale(suger_cloth_boots_img, (tile_size *3, tile_size * 3))
suger_cloth_pants_img = pygame.image.load('game_files/imgs/items/suger_cloth_pants.png')
suger_cloth_pants_img = pygame.transform.scale(suger_cloth_pants_img, (tile_size *3, tile_size * 3))
suger_cloth_chestplate_img = pygame.image.load('game_files/imgs/items/suger_cloth_chestplate_img.png')
suger_cloth_chestplate_img = pygame.transform.scale(suger_cloth_chestplate_img, (tile_size *3, tile_size * 3))
suger_cloth_helmet_img = pygame.image.load('game_files/imgs/items/suger_cloth_helmet_img.png')
suger_cloth_helmet_img = pygame.transform.scale(suger_cloth_helmet_img, (tile_size *3, tile_size * 3))
gelatin_red_img = pygame.image.load('game_files/imgs/items/gelatin_red_item.png')
gelatin_red_img = pygame.transform.scale(gelatin_red_img, (tile_size *3, tile_size * 3))
gelatin_green_img = pygame.image.load('game_files/imgs/items/gelatin_green_item.png')
gelatin_green_img = pygame.transform.scale(gelatin_green_img, (tile_size *3, tile_size * 3))
gelatin_blue_img = pygame.image.load('game_files/imgs/items/gelatin_blue_item.png')
gelatin_blue_img = pygame.transform.scale(gelatin_blue_img, (tile_size *3, tile_size * 3))
gelatin_yellow_img = pygame.image.load('game_files/imgs/items/gelatin_yellow_item.png')
gelatin_yellow_img = pygame.transform.scale(gelatin_yellow_img, (tile_size *3, tile_size * 3))
#load button textures
button_img = pygame.image.load('game_files/imgs/menu/button_img.png')
button_img = pygame.transform.scale(button_img, (tile_size * 8, tile_size * 4))
button_hover_img = pygame.transform.scale(button_img, (tile_size * 9, tile_size * 4.5))
button_selected = pygame.image.load('game_files/imgs/menu/selected_button.png')
button_selected = pygame.transform.scale(button_selected, (tile_size * 8, tile_size * 4))
button_settings = pygame.image.load('game_files/imgs/menu/settings_button.png')
button_settings = pygame.transform.scale(button_settings, (tile_size * 4, tile_size * 4))
button_settings_hover = pygame.image.load('game_files/imgs/menu/settings_button_hover.png')
button_settings_hover = pygame.transform.scale(button_settings_hover, (tile_size * 4, tile_size * 4))
button_settings_game = pygame.image.load('game_files/imgs/menu/game_settings_button.png')
button_settings_game = pygame.transform.scale(button_settings_game, (tile_size * 7.5, tile_size * 4))
button_settings_selected = pygame.image.load('game_files/imgs/menu/game_settings_button_selected.png')
button_settings_selected = pygame.transform.scale(button_settings_selected, (tile_size * 8, tile_size * 4))
switch_off = pygame.image.load('game_files/imgs/menu/switch_off.png')
switch_off = pygame.transform.scale(switch_off, (tile_size * 5, tile_size * 2.5))
switch_on = pygame.image.load('game_files/imgs/menu/switch_on.png')
switch_on = pygame.transform.scale(switch_on, (tile_size * 5, tile_size * 2.5))
#load music
#player_walk_sfx = pygame.mixer.Sound('imgs/coin.wav')
pygame.mixer.music.set_endevent ( pygame.USEREVENT ) 
playlist = ['game_files/music/Leaving.wav']
pygame.mixer.music.load(random.choice(playlist))


#screen details
pygame.display.set_caption('Food Wars')
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()


#create dictionaries
game_map = {}
game_map_interactables = {}
tile_index = { 1:grass,
               2:water
    }
tile_index_interactables = {1:tree,
                            2:rock,
                            3:log,
                            4:cobblestone,
                            5:stick,
                            6:suger_string,
                            7:red_gelatin,
                            8:green_gelatin,
                            9:blue_gelatin,
                            10:yellow_gelatin,
                            }
item_index = {0: item_empty,
              1: log_item,
              2: rock_item,
              3: stick_item,
              4: wooden_axe_img,
              5: stone_axe_img,
              6: wooden_pickaxe_img,
              7: stone_pickaxe_img,
              8: wooden_planks_img,
              9: cobblestone_img,
              10: sharp_stick_img,
              11: suger_string_img,
              12: suger_cloth_img,
              13: suger_cloth_boots_img,
              14: suger_cloth_pants_img,
              15: suger_cloth_chestplate_img,
              16: suger_cloth_helmet_img,
              17: gelatin_red_img,
              18: gelatin_green_img,
              19: gelatin_blue_img,
              20: gelatin_yellow_img,
            }
world_generated = {}
world_names = {}
world_difficulties = {}
world_seeds = {}
#load files
if path.exists('game_files/crafting/crafting_recepies.json'):
    with open('game_files/crafting/crafting_recepies.json', 'r') as recepies:
        crafting_recepies = json.load(recepies)
if path.exists('game_files/item_data/item_data.json'):
    with open('game_files/item_data/item_data.json', 'r') as data:
        item_data = json.load(data)
if path.exists('game_files/world_data/world_1/generated/generated.json'):
    with open('game_files/world_data/world_1/generated/generated.json', 'r') as one_gen:
        world_one_generated = json.load(one_gen)
        world_generated[1] = world_one_generated
if path.exists('game_files/world_data/world_2/generated/generated.json'):
    with open('game_files/world_data/world_2/generated/generated.json', 'r') as two_gen:
        world_two_generated = json.load(two_gen)
        world_generated[2] = world_two_generated
if path.exists('game_files/world_data/world_3/generated/generated.json'):
    with open('game_files/world_data/world_3/generated/generated.json', 'r') as three_gen:
        world_three_generated = json.load(three_gen)
        world_generated[3] = world_three_generated
if path.exists('game_files/world_data/world_4/generated/generated.json'):
    with open('game_files/world_data/world_4/generated/generated.json', 'r') as four_gen:
        world_four_generated = json.load(four_gen)
        world_generated[4] = world_four_generated
#load names
if path.exists('game_files/world_data/world_1/name/world_name.json'):
    with open('game_files/world_data/world_1/name/world_name.json', 'r') as one_name:
        world_one_name = json.load(one_name)
        world_names[1] = world_one_name
if path.exists('game_files/world_data/world_2/name/world_name.json'):
    with open('game_files/world_data/world_2/name/world_name.json', 'r') as two_name:
        world_two_name = json.load(two_name)
        world_names[2] = world_two_name
if path.exists('game_files/world_data/world_3/name/world_name.json'):
    with open('game_files/world_data/world_3/name/world_name.json', 'r') as three_name:
        world_three_name = json.load(three_name)
        world_names[3] = world_three_name
if path.exists('game_files/world_data/world_4/name/world_name.json'):
    with open('game_files/world_data/world_4/name/world_name.json', 'r') as four_name:
        world_four_name = json.load(four_name)
        world_names[4] = world_four_name
#load difficultes
if path.exists('game_files/world_data/world_1/difficulty/difficulty.json'):
    with open('game_files/world_data/world_1/difficulty/difficulty.json', 'r') as one_difficulty:
        world_one_diffuclty = json.load(one_difficulty)
        world_difficulties[1] = world_one_diffuclty
if path.exists('game_files/world_data/world_2/difficulty/difficulty.json'):
    with open('game_files/world_data/world_2/difficulty/difficulty.json', 'r') as two_difficulty:
        world_two_diffuclty = json.load(two_difficulty)
        world_difficulties[2] = world_two_diffuclty
if path.exists('game_files/world_data/world_3/difficulty/difficulty.json'):
    with open('game_files/world_data/world_3/difficulty/difficulty.json', 'r') as three_difficulty:
        world_three_diffuclty = json.load(three_difficulty)
        world_difficulties[3] = world_three_diffuclty
if path.exists('game_files/world_data/world_4/difficulty/difficulty.json'):
    with open('game_files/world_data/world_4/difficulty/difficulty.json', 'r') as four_difficulty:
        world_four_diffuclty = json.load(four_difficulty)
        world_difficulties[4] = world_four_diffuclty
#load seeds
if path.exists('game_files/world_data/world_1/seed/seed.json'):
    with open('game_files/world_data/world_1/seed/seed.json', 'r') as one_seed:
        world_one_seed = json.load(one_seed)
        world_seeds[1] = world_one_seed
if path.exists('game_files/world_data/world_2/seed/seed.json'):
    with open('game_files/world_data/world_2/seed/seed.json', 'r') as two_seed:
        world_two_seed = json.load(two_seed)
        world_seeds[2] = world_two_seed
if path.exists('game_files/world_data/world_3/seed/seed.json'):
    with open('game_files/world_data/world_3/seed/seed.json', 'r') as three_seed:
        world_three_seed = json.load(three_seed)
        world_seeds[3] = world_three_seed
if path.exists('game_files/world_data/world_4/seed/seed.json'):
    with open('game_files/world_data/world_4/seed/seed.json', 'r') as four_seed:
        world_four_seed = json.load(four_seed)
        world_seeds[4] = world_four_seed
#load settings
if path.exists('game_files/settings/settings.json'):
    with open('game_files/settings/settings.json', 'r') as settings_loaded:
        loaded_settings = json.load(settings_loaded)
        sfx = loaded_settings[0]
        music = loaded_settings[1]
        scroll_sense_ratio = loaded_settings[2]
        coords_on = loaded_settings[3]
#load credits
if path.exists('game_files/fonts/medieval-sharp-font/info.txt'):
    with open('game_files/fonts/medieval-sharp-font/info.txt', 'r') as credits_loaded:
        credits_txt = credits_loaded.read()
#colours
white = (255, 255, 255)
colour_inactive = (43, 45, 70)
colour_active = (75, 77, 108)
settings_bg_colour = (198, 198, 198)
settings_bg_colour_active = (190, 190, 190)

#define fonts 
font =  pygame.font.Font('game_files/fonts/medieval-sharp-font/MedievalSharp-xOZ5.ttf', 24)
font_inventory =  pygame.font.Font('game_files/fonts/medieval-sharp-font/MedievalSharp-xOZ5.ttf', 15)
font_difficulty =  pygame.font.Font('game_files/fonts/medieval-sharp-font/MedievalSharp-xOZ5.ttf', 19)

#load/define settings
scroll_sensitivity = 1

if music == True:
    pygame.mixer.music.play() 
else:
    pygame.mixer.music.pause()

#functions
def handle_music(playlist, event, music):
    if music == True:
        pygame.mixer.music.unpause()
        if event == pygame.USEREVENT:
            print(2)
            music_load = random.choice(playlist)
            pygame.mixer.music.load(music_load) 
            pygame.mixer.music.play() 
    else:
        pygame.mixer.music.pause()
    
def generate_chunks(x, y, seed):
    chunk_data = []
    opensimplex.seed(seed)
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            tile_type = 0
            height = opensimplex.noise2(target_x / 30, target_y / 30)
            if height < -0.3:
                tile_type = 2
            elif height == -0.3:
                tile_type = 2
            elif height > -0.3:
                tile_type = 1
            if tile_type != 0:
                chunk_data.append([[target_x, target_y], tile_type])
    return chunk_data

def generate_chunks_interactables(x, y, seed, game_map):
    chunk_data = []
    opensimplex.seed(seed)
    for y_pos in range(chunk_size):
        for x_pos in range(chunk_size):
            target_x = x * chunk_size + x_pos
            target_y = y * chunk_size + y_pos
            tile_type = 0
            height = opensimplex.noise2(target_x , target_y)
            for tile in game_map[str(x) + ':' + str(y)]:
                if tile[1] == 2:
                    tile_type = 0
                    break
                #coords, type, health
                elif height < -0.78:
                    tile_type = 1
                elif height > 0.78:
                    tile_type = 2
                else: 
                    tile_type = 0
            chunk_data.append([[target_x, target_y], tile_type, 12])
            #if tile_type != 0:
                #coords, type, health
                #chunk_data.append([[target_x, target_y], tile_type, 12])
    return chunk_data

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
def draw_text_wrap(text, font, colour, x, y, screen, allowed_width, centered):
    # first, split the text into words
    words = text.split()
    # now, construct lines out of these words
    lines = []
    while len(words) > 0:
        # get as many words as will fit within allowed_width
        line_words = []
        while len(words) > 0:
            line_words.append(words.pop(0))
            fw, fh = font.size(' '.join(line_words + words[:1]))
            if fw > allowed_width:
                break
        # add a line consisting of those words
        line = ' '.join(line_words)
        lines.append(line)
    # now we've split our text into lines that fit into the width, actually
    # render them
    # we'll render each line below the last, so we need to keep track of
    # the culmative height of the lines we've rendered so far
    y_offset = 0
    for line in lines:
        fw, fh = font.size(line)
        # (tx, ty) is the top-left of the font surface
        ty = y + y_offset
        if centered == True:
            tx = x - fw / 2
        else:
            tx = x
        font_surface = font.render(line, True, colour)
        #screen.blit(font_surface, (tx, ty))
        screen.blit(font_surface, (tx, ty))

        y_offset += fh
#tile functions
def tree(tile, hotbar_slots, hotbar_selector_slots, damage):
    #tile is chunk tile in map- looking for what value is the 1st occurance of the coorect tree's coordinents in the chunk
    index = game_map_interactables[tile[2]].index(tile[1])
    if [[tile[1][0][0], tile[1][0][1] + 2], 0, 12] not in game_map_interactables[tile[2]]:
        game_map_interactables[tile[2]].append([[tile[1][0][0], tile[1][0][1] + 2], 0, 12])
    index_two = game_map_interactables[tile[2]].index([[tile[1][0][0], tile[1][0][1] + 2], 0, 12])
    item_num = hotbar_slots['slot_' + str(hotbar_selector_slots + 1)][0]
    if game_map_interactables[tile[2]][index][2] <= 0:
        if item_num != 4 and item_num != 5 and item_num != 10:
            game_map_interactables[tile[2]][index][1] = 5
        else:
            game_map_interactables[tile[2]][index][1] = 3
        game_map_interactables[tile[2]][index_two][1] = 5
        tree_rects.remove(tile)
    else:
        if item_num == 4 or item_num == 4:
            damage_addition = damage
        else:
            damage_addition = 0
        #rect, from chunk data, target chunk
        game_map_interactables[tile[2]][index][2] -= 1 + damage_addition

def rock(tile, hotbar_slots, hotbar_selector_slots, damage):
   index = game_map_interactables[tile[2]].index(tile[1])
   item = hotbar_slots['slot_' + str(hotbar_selector_slots + 1)][0]
   if game_map_interactables[tile[2]][index][2] <= 0:
       if item != 6 and item != 7:
           game_map_interactables[tile[2]][index][1] = 0
       else:
           game_map_interactables[tile[2]][index][1] = 4
       rock_rects.remove(tile)
   else:
       #rect, from chunk data, target chunk
       if item == 6 or item == 7:
           damage_addition = damage
       else:
           damage_addition = 0
       game_map_interactables[tile[2]][index][2] -= 1 + damage_addition


#world functions
def generate_world(world_num, world_name, seed, difficulty):
    with open(f'game_files/world_data/world_{world_num}/generated/generated.json', "w") as file:
        json.dump(True, file)
    with open(f'game_files/world_data/world_{world_num}/name/world_name.json', "w") as file:
        json.dump(world_name, file)
    with open(f'game_files/world_data/world_{world_num}/seed/seed.json', "w") as file:
        json.dump(seed, file)
    with open(f'game_files/world_data/world_{world_num}/difficulty/difficulty.json', "w") as file:
        json.dump(difficulty, file)
    world_names[world_num] = world_name
    world_generated[world_num] = True
def save_world(world_num, game_map, game_map_interactables, inventory, armour, hotbar, health, scroll, player_x, player_y, player_direction):
    temp_inventory = []
    #print(inventory)
    #print(armour)
    #print(hotbar)
    for tile in inventory:
        slot = []
        slot.append(inventory[tile][2])
        slot.append(inventory[tile][3])
        temp_inventory.append(slot)
    temp_armour = []
    for tile in armour:
        slot = []
        slot.append(armour[tile][2])
        slot.append(armour[tile][3])
        temp_armour.append(slot)
    temp_hotbar = []
    for tile in hotbar:
        slot = []
        slot.append(hotbar[tile][2])
        slot.append(hotbar[tile][3])
        temp_hotbar.append(slot)
    stats = [health, scroll, [player_x, player_y], player_direction]
    with open(f'game_files/world_data/world_{world_num}/map_data/game_map.json', "w") as file:
        json.dump(game_map, file)
    with open(f'game_files/world_data/world_{world_num}/map_data/game_map_interactables.json', "w") as file:
        json.dump(game_map_interactables, file)
    with open(f'game_files/world_data/world_{world_num}/player_data/inventory.json', "w") as file:
        json.dump(temp_inventory, file)
    with open(f'game_files/world_data/world_{world_num}/player_data/armour.json', "w") as file:
        json.dump(temp_armour, file)
    with open(f'game_files/world_data/world_{world_num}/player_data/hotbar.json', "w") as file:
        json.dump(temp_hotbar, file)
    with open(f'game_files/world_data/world_{world_num}/player_data/stats.json', "w") as file:
        json.dump(stats, file)
def load_world(world_num):
    if path.exists(f'game_files/world_data/world_{world_num}/map_data/game_map.json'):
        with open(f'game_files/world_data/world_{world_num}/map_data/game_map.json', 'r') as world_map:
            global game_map
            game_map = json.load(world_map)
    if path.exists(f'game_files/world_data/world_{world_num}/map_data/game_map_interactables.json'):
        with open(f'game_files/world_data/world_{world_num}/map_data/game_map_interactables.json', 'r') as world_map_interactables:
            global game_map_interctables
            game_map_interctables = json.load(world_map_interactables)
    if path.exists(f'game_files/world_data/world_{world_num}/seed/seed.json'):
        with open(f'game_files/world_data/world_{world_num}/seed/seed.json', 'r') as loaded_seed:
            global world_seed
            world_seed = int(json.load(loaded_seed))
    if path.exists(f'game_files/world_data/world_{world_num}/player_data/inventory.json'):
        with open(f'game_files/world_data/world_{world_num}/player_data/inventory.json', 'r') as loaded_inventory:
            inventory_counter = 0
            inventory_data = json.load(loaded_inventory)
            #print(inventory_data)
            for tile in inventory.slots:
                inventory.slots[tile][2] = inventory_data[inventory_counter][0]
                inventory.slots[tile][3] = inventory_data[inventory_counter][1]
                inventory_counter += 1
    if path.exists(f'game_files/world_data/world_{world_num}/player_data/armour.json'):
        with open(f'game_files/world_data/world_{world_num}/player_data/armour.json', 'r') as loaded_inventory:
            inventory_counter = 0
            inventory_data = json.load(loaded_inventory)
            for tile in inventory.armour_slots:
                inventory.armour_slots[tile][2] = inventory_data[inventory_counter][0]
                inventory.armour_slots[tile][3] = inventory_data[inventory_counter][1]
                inventory_counter += 1
    if path.exists(f'game_files/world_data/world_{world_num}/player_data/hotbar.json'):
        with open(f'game_files/world_data/world_{world_num}/player_data/hotbar.json', 'r') as loaded_inventory:
            inventory_counter = 0
            inventory_data = json.load(loaded_inventory)
            for tile in inventory.hotbar_slots:
                inventory.hotbar_slots[tile][2] = inventory_data[inventory_counter][0]
                inventory.hotbar_slots[tile][3] = inventory_data[inventory_counter][1]
                inventory_counter += 1
    if path.exists(f'game_files/world_data/world_{world_num}/player_data/stats.json'):
        with open(f'game_files/world_data/world_{world_num}/player_data/stats.json', 'r') as statistics:
            stats = json.load(statistics)
            player.hearts['health_count'] = stats[0]
            global true_scroll
            true_scroll = stats[1]
            player.rect.x = stats[2][0]
            player.rect.y = stats[2][1]
            player.direction = stats[3]
    return game_map_interctables

def debug_menu_show(target_chunk):
    if coords_on == False:
        draw_text(str(scroll), font, white, 10, 10)
    draw_text('Target Chunk: ' + target_chunk, font, white, 10, 40)
    
def spawn_entities():
    if world_difficulties[world_num] == 1:
        if len(entities) < 3:
            spawn = random.randint(0, 100)
            if spawn == 0:
                x = random.randint(player.rect.x - 300, player.rect.x + 300)
                y = random.randint(player.rect.y - 300, player.rect.y + 300)
                if random.randint(1, 2) == 1:
                    entities.append([len(entities), Cotten_Candy(len(entities), x, y)])
                else:
                    entities.append([len(entities), Gelatin(len(entities), x, y)])
                
#entity classes
class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        
    def reset(self, x, y):
        self.dead = False
        self.front_walk = []
        self.back_walk = []
        self.left_walk = []
        self.right_walk = []
        self.front_run = []
        self.back_run = []
        self.left_run = []
        self.right_run = []
        self.front_swim = []
        self.back_swim = []
        self.left_swim = []
        self.right_swim = []
        self.right_hit = []
        self.left_hit = []
        self.front_hit = []
        self.back_hit = []
        self.counter = 0
        self.index = 0
        self.direction = 2
        self.regen_counter = 0
        for num in range(1,5):
            temp_img_front = pygame.image.load(f'game_files/imgs/player/player_front_{num}.png')
            temp_img_front = pygame.transform.scale(temp_img_front, (tile_size * 2, tile_size * 4))
            self.front_walk.append(temp_img_front)
            temp_img_back = pygame.image.load(f'game_files/imgs/player/player_back_{num}.png')
            temp_img_back = pygame.transform.scale(temp_img_back, (tile_size * 2, tile_size * 4))
            self.back_walk.append(temp_img_back)
            temp_img_right = pygame.image.load(f'game_files/imgs/player/player_side_{num}.png')
            temp_img_right = pygame.transform.scale(temp_img_right, (tile_size * 2, tile_size * 4))
            self.right_walk.append(temp_img_right)
            temp_img_left =  pygame.transform.flip(temp_img_right, 180, 0)
            self.left_walk.append(temp_img_left)
        for num in range(1, 6):
            temp_img_right_hit = pygame.image.load(f'game_files/imgs/player/player_side_hit_{num}.png')
            temp_img_right_hit = pygame.transform.scale(temp_img_right_hit, (tile_size * 2, tile_size * 4))
            self.right_hit.append(temp_img_right_hit)
            temp_img_left_hit =  pygame.transform.flip(temp_img_right_hit, 180, 0)
            self.left_hit.append(temp_img_left_hit)
            temp_img_front_hit = pygame.image.load(f'game_files/imgs/player/player_front_hit_{num}.png')
            temp_img_front_hit = pygame.transform.scale(temp_img_front_hit, (tile_size * 2, tile_size * 4))
            self.front_hit.append(temp_img_front_hit)
            temp_img_back_hit = pygame.image.load(f'game_files/imgs/player/player_back_hit_{num}.png')
            temp_img_back_hit = pygame.transform.scale(temp_img_back_hit, (tile_size * 2, tile_size * 4))
            self.back_hit.append(temp_img_back_hit)
        temp_img_right_swim = pygame.image.load('game_files/imgs/player/player_swim_side.png')
        temp_img_right_swim = pygame.transform.scale(temp_img_right_swim, (tile_size * 2, tile_size * 4))
        self.right_swim.append(temp_img_right_swim)
        temp_img_left_swim =  pygame.transform.flip(temp_img_right_swim, 180, 0)
        self.left_swim.append(temp_img_left_swim)
        temp_img_front_swim = pygame.image.load('game_files/imgs/player/player_swim_front.png')
        temp_img_front_swim = pygame.transform.scale(temp_img_front_swim, (tile_size * 2, tile_size * 4))
        self.front_swim.append(temp_img_front_swim)
        temp_img_back_swim = pygame.image.load('game_files/imgs/player/player_swim_back.png')
        temp_img_back_swim = pygame.transform.scale(temp_img_back_swim, (tile_size * 2, tile_size * 4))
        self.back_swim.append(temp_img_back_swim)
        front_swim = pygame.image.load('game_files/imgs/player/player_swim_front.png')
        front_swim = pygame.transform.scale(front_swim, (tile_size *2, tile_size * 4))
        self.front_swim.append(front_swim)
        back_swim = pygame.image.load('game_files/imgs/player/player_swim_back.png')
        back_swim = pygame.transform.scale(back_swim, (tile_size *2, tile_size * 4))
        self.back_swim.append(back_swim)
        right_swim = pygame.image.load('game_files/imgs/player/player_swim_side.png')
        right_swim = pygame.transform.scale(right_swim, (tile_size *2, tile_size * 4))
        self.right_swim.append(right_swim)
        left_swim = pygame.transform.flip(right_swim, 180, 0)
        self.left_swim.append(left_swim)
        self.img = self.front_walk[0]
        self.rect = self.front_walk[1].get_rect()
        self.hitbox = self.rect
        self.rect.x = x
        self.rect.y = y
        self.width = self.front_walk[1].get_width()
        self.height = self.front_walk[1].get_height()
        #armour stuff
        self.armour_full = pygame.image.load('game_files/imgs/gui/armour_full.png')
        self.armour_half = pygame.image.load('game_files/imgs/gui/armour_half.png')
        self.armour_empty = pygame.image.load('game_files/imgs/gui/armour_empty.png')
        self.armour_bg = pygame.image.load('game_files/imgs/gui/armour_bg.png')
        self.armour_points = {
                    'armour_count': 0,
                    'armour_1': self.armour_empty,
                    'armour_2': self.armour_empty,
                    'armour_3': self.armour_empty,
                    'armour_4': self.armour_empty,
                    'armour_5': self.armour_empty,
                    'armour_6': self.armour_empty,
                    'armour_7': self.armour_empty,
                    'armour_8': self.armour_empty,
                    'armour_9': self.armour_empty,
                    'armour_10': self.armour_empty,
                    }
        #health stuff
        self.heart_full = pygame.image.load('game_files/imgs/gui/heart_full.png')
        self.heart_half = pygame.image.load('game_files/imgs/gui/heart_half.png')
        self.heart_empty = pygame.image.load('game_files/imgs/gui/heart_empty.png')
        self.heart_bg= pygame.image.load('game_files/imgs/gui/heart_bg.png')
        self.hearts = {
                    'health_count': 20,
                    'heart_1': self.heart_full,
                    'heart_2': self.heart_full,
                    'heart_3': self.heart_full,
                    'heart_4': self.heart_full,
                    'heart_5': self.heart_full,
                    'heart_6': self.heart_full,
                    'heart_7': self.heart_full,
                    'heart_8': self.heart_full,
                    'heart_9': self.heart_full,
                    'heart_10': self.heart_full,
                    }
        self.tool_rect = item_index[1].get_rect()
        self.speed = 0
        self.run = False
        walk_icon = pygame.image.load('game_files/imgs/gui/walk_icon.png')
        self.walk_icon = pygame.transform.scale(walk_icon, (tile_size * 2, tile_size * 2))
        run_icon = pygame.image.load('game_files/imgs/gui/run_icon.png')
        self.run_icon = pygame.transform.scale(run_icon, (tile_size * 2, tile_size * 2))
        self.run_cooldown = 2
        self.selected_item = hotbar.selected_item
        self.item = 0
        self.chopping = False
        self.chop_timer = 0
        self.broken = False
        self.in_water = False
        self.submerged = False
        self.speed_modifier = 1.5
        self.event = 'unused text'
    def respawn(self):
        self.hearts['health_count'] = 20
        self.dead = False
        
    def update(self):
        walk_cooldown = 4
        key = pygame.key.get_pressed()
        for tile in water_rects:
            if player.hitbox.colliderect(tile[0]):
                self.in_water = True
                self.speed_modifier = 2.2
                break
            else:
                self.in_water = False
                self.speed_modifier = 1.5
        if self.in_water == True:
            for tile in grass_rects:
                if player.hitbox.colliderect(tile[0]):
                    self.submerged = False
                    break
                else:
                    self.submerged = True
        if key[pygame.K_r]:
            if self.run == False and self.run_cooldown >= 1:
                self.speed = 0.8
                self.run = True
                self.run_cooldown = 0
            elif self.run == True and self.run_cooldown >= 1:
                self.speed = 0.1
                self.run = False
                self.run_cooldown = 0
            self.run_cooldown += 1
        if key[pygame.K_w]:
            self.rect.y -= tile_size // (self.speed_modifier - self.speed)
            self.direction = 0
            self.counter += 1
        if key[pygame.K_s]:
            self.rect.y += tile_size // (self.speed_modifier - self.speed)
            self.direction = 2
            self.counter += 1
        if key[pygame.K_a]:
            self.rect.x -= tile_size // (self.speed_modifier - self.speed)
            self.direction = 1
            self.counter += 1
        if key[pygame.K_d]:
            self.rect.x += tile_size // (self.speed_modifier - self.speed)
            self.direction = 3
            self.counter += 1
        #pick up items
        for tile in item_rects:
            search = 1
            breaker = 1
            if pygame.Rect.colliderect(self.hitbox, tile[0]):
                if tile[1][1] == 3:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 1:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 1:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 1
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 1
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
                elif tile[1][1] == 4:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 9:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 9:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 9
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 9
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
                elif tile[1][1] == 5:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 3:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 3:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 3
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 3
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
                elif tile[1][1] == 6:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 11:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 11:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 11
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 11
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
                elif tile[1][1] == 7:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 17:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 17:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 17
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 17
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
                elif tile[1][1] == 8:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 18:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 18:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 18
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 18
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
                elif tile[1][1] == 9:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 19:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 19:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 19
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 19
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
                elif tile[1][1] == 10:
                    while search == 1:
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 20:
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 20:
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                        if breaker == 0:
                            break
                        for item in inventory.hotbar_slots:
                            if inventory.hotbar_slots[item][2] == 0:
                                inventory.hotbar_slots[item][2] = 20
                                inventory.hotbar_slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break 
                        if breaker == 0:
                            break
                        for item in inventory.slots:
                            if inventory.slots[item][2] == 0:
                                inventory.slots[item][2] = 20
                                inventory.slots[item][3] += 1
                                game_map_interactables[tile[2]].remove(tile[1])
                                item_rects.remove(tile)
                                breaker = 0
                                break
                        if breaker == 0:
                            break
        #print run icon
        if self.run == False:
            screen.blit(self.walk_icon, (400, 1))
        elif self.run == True:
            screen.blit(self.run_icon, (400, 1))
        #add animation
        if run == False:
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.front_walk):
                    self.index = 0
                if self.direction == 0:
                    self.img = self.back_walk[self.index]
                if self.direction == 1:
                    self.img = self.left_walk[self.index]
                if self.direction == 2:
                    self.img = self.front_walk[self.index]
                if self.direction == 3:
                    self.img = self.right_walk[self.index]
        elif run == True:
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.front_walk):
                    self.index = 0
                if self.direction == 0:
                    self.img = self.back_walk[self.index]
                if self.direction == 1:
                    self.img = self.left_walk[self.index]
                if self.direction == 2:
                    self.img = self.front_walk[self.index]
                if self.direction == 3:
                    self.img = self.right_walk[self.index]


        #set back to standing if no key is pressed
        if not key[pygame.K_w] and not key[pygame.K_a] and not key[pygame.K_s] and not key[pygame.K_d]:
            if self.direction == 0:
                self.counter = 0
                self.index = 0
                self.img = self.back_walk[self.index]
            if self.direction == 1:
                self.counter = 0
                self.index = 0
                self.img = self.left_walk[self.index]
            if self.direction == 2:
                self.counter = 0
                self.index = 0
                self.img = self.front_walk[self.index]
            if self.direction == 3:
                self.counter = 0
                self.index = 0
                self.img = self.right_walk[self.index]
            if self.chop_timer > 0:
                if self.direction == 0:
                    self.img = self.back_hit[self.chop_timer - 1]
                if self.direction == 1:
                    self.img = self.left_hit[self.chop_timer - 1]
                if self.direction == 2:
                    self.img = self.front_hit[self.chop_timer - 1]
                if self.direction == 3:
                    self.img = self.right_hit[self.chop_timer - 1]
        if self.submerged == True:
            if self.direction == 0:
                self.img = self.back_swim[0]
            if self.direction == 1:
                self.img = self.left_swim[0]
            if self.direction == 2:
                self.img = self.front_swim[0]
            if self.direction == 3:
                self.img = self.right_swim[0]
        self.hitbox = self.img.get_rect()
        self.hitbox.x = self.rect.x - true_scroll[0]
        self.hitbox.y = self.rect.y - true_scroll[1]
        screen.blit(self.img, self.hitbox)
        #mke new rect that locks to img for hitbox
        if debug == True:
            pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)
    def armour(self):
        if len(item_data[str(inventory.armour_slots['slot_1'][2])]) == 7:
            helmet_protection = item_data[str(inventory.armour_slots['slot_1'][2])][6]
        else:
            helmet_protection = 0
        if len(item_data[str(inventory.armour_slots['slot_2'][2])]) == 7:
            chestplate_protection = item_data[str(inventory.armour_slots['slot_2'][2])][6]
        else:
            chestplate_protection = 0
        if len(item_data[str(inventory.armour_slots['slot_3'][2])]) == 7:
            legs_protection = item_data[str(inventory.armour_slots['slot_3'][2])][6]
        else:
            legs_protection = 0
        if len(item_data[str(inventory.armour_slots['slot_4'][2])]) == 7:
            boots_protection = item_data[str(inventory.armour_slots['slot_4'][2])][6]
        else:
            boots_protection = 0
        self.armour_points['armour_count'] = helmet_protection + chestplate_protection + legs_protection + boots_protection
            
        if self.armour_points['armour_count'] == 20:
            for num in range(1,11):
                self.armour_points[f'armour_{num}'] = self.armour_full
        elif self.armour_points['armour_count'] == 19:
            for num in range(1,10):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(10,11):
                self.armour_points[f'armour_{num}'] = self.armour_half
        elif self.armour_points['armour_count'] == 18:
            for num in range(1,10):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(10,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 17:
            for num in range(1,9):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(9,10):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(10,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 16:
            for num in range(1,9):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(9,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 15:
            for num in range(1,8):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(8,9):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(9,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 14:
            for num in range(1,8):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(8,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 13:
            for num in range(1,7):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(7,8):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(8,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 12:
            for num in range(1,7):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(7,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 11:
            for num in range(1,6):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(6,7):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(7,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 10:
            for num in range(1,6):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(6,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 9:
            for num in range(1,5):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(5,6):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(6,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 8:
            for num in range(1,5):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(5,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 7:
            for num in range(1,4):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(4,5):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(5,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 6:
            for num in range(1,4):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(4,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 5:
            for num in range(1,3):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(3,4):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(4,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 4:
            for num in range(1,3):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(3,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 3:
            for num in range(1,2):
                self.armour_points[f'armour_{num}'] = self.armour_full
            for num in range(2,3):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(3,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 2:
            for num in range(1,2):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(2,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 1:
            for num in range(1,2):
                self.armour_points[f'armour_{num}'] = self.armour_half
            for num in range(2,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
        elif self.armour_points['armour_count'] == 0:
            for num in range(1,11):
                self.armour_points[f'armour_{num}'] = self.armour_empty
                
        for num in range(1,11):
            screen.blit(self.armour_bg, (num * 15 + 420, 16))
            screen.blit(self.armour_points[f'armour_{num}'], (num * 15 + 420, 16))
    def health(self):
        if self.hearts['health_count'] <= 20:
            if self.regen_counter == 25:
                self.hearts['health_count'] += 1
                self.regen_counter = 0
            else:
                self.regen_counter += 1
        if self.hearts['health_count'] == 20:
            for num in range(1,11):
                self.hearts[f'heart_{num}'] = self.heart_full
        elif self.hearts['health_count'] == 19:
            for num in range(1,10):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(10,11):
                self.hearts[f'heart_{num}'] = self.heart_half
        elif self.hearts['health_count'] == 18:
            for num in range(1,10):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(10,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 17:
            for num in range(1,9):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(9,10):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(10,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 16:
            for num in range(1,9):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(9,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 15:
            for num in range(1,8):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(8,9):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(9,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 14:
            for num in range(1,8):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(8,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 13:
            for num in range(1,7):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(7,8):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(8,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 12:
            for num in range(1,7):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(7,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 11:
            for num in range(1,6):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(6,7):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(7,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 10:
            for num in range(1,6):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(6,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 9:
            for num in range(1,5):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(5,6):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(6,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 8:
            for num in range(1,5):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(5,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 7:
            for num in range(1,4):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(4,5):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(5,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 6:
            for num in range(1,4):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(4,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 5:
            for num in range(1,3):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(3,4):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(4,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 4:
            for num in range(1,3):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(3,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 3:
            for num in range(1,2):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(2,3):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(3,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 2:
            for num in range(1,2):
                self.hearts[f'heart_{num}'] = self.heart_full
            for num in range(2,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 1:
            for num in range(1,2):
                self.hearts[f'heart_{num}'] = self.heart_half
            for num in range(2,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        elif self.hearts['health_count'] == 0:
            for num in range(1,11):
                self.hearts[f'heart_{num}'] = self.heart_empty
        if self.hearts['health_count'] == 0:
            self.dead = True
        for num in range(1,11):
            screen.blit(self.heart_bg, (num * 15 + 420, 0))
            screen.blit(self.hearts[f'heart_{num}'], (num * 15 + 420, 0))
        return game_state
    def damage(self, damage_amount):
        print(9)
        if self.armour_points['armour_count'] == 0:
            damage_reduce_percent = 1
        else:
            #print(self.armour_points['armour_count'] / 21)
            damage_reduce_percent = 1 - round(self.armour_points['armour_count'] / 21, 1)
        self.hearts['health_count'] -= round(damage_amount * damage_reduce_percent)
    def get_event(self, event):
        self.event = event
    def use_item(self, hotbar_slots, hotbar_selector_slots):
        self.selected_item = hotbar.selected_item
        item_num = hotbar_slots['slot_' + str(hotbar_selector_slots + 1)][0]
        if len(item_data[str(item_num)]) == 6:
            item_stats = [item_data[str(item_num)][4], item_data[str(item_num)][5]]
        else:
            item_stats = [0, 0]
        self.selected_item = hotbar.selected_item
        event = self.event
        key = pygame.key.get_pressed()
        for item in item_data:
            if item[0] == self.item:
                self.item_data = item
                break
        if self.direction == 0:
            item_rect_top = self.rect.y - scroll[1] - self.height
            item_rect_left = self.rect.x  - scroll[0]
        if self.direction == 1:
            item_rect_left = self.rect.x   - scroll[0] - self.width
            item_rect_top = self.rect.y  - scroll[1]
        if self.direction == 2:
            item_rect_top = self.rect.y  - scroll[1] + self.height
            item_rect_left = self.rect.x  - scroll[0]
        if self.direction == 3:
            item_rect_left = self.rect.x  - scroll[0] + self.width
            item_rect_top = self.rect.y  - scroll[1]
        item_rect = pygame.Rect(item_rect_left, item_rect_top, self.width, self.height)
        if key[pygame.K_q] and self.chopping == False:
            self.chopping = True
        if self.chopping == True:
            if self.chop_timer == 5 and self.broken == False:
                for tile in tree_rects:
                    if pygame.Rect.colliderect(item_rect, tile[0]):
                        tree(tile, hotbar_slots, hotbar_selector_slots, item_stats[0])
                for tile in rock_rects:
                    if item_rect.colliderect(tile[0]):
                        rock(tile, hotbar_slots, hotbar_selector_slots, item_stats[0])
                for entity in entities:
                    if item_rect.colliderect(entity[1].rect):
                        entity[1].health -= 1 + item_stats[1]
                if len(item_data[str(item_num)]) == 8:
                    global projectiles
                    if item_num == 17:
                        inventory.hotbar_slots['slot_' + str(hotbar_selector_slots + 1)][3] -= 1
                        projectiles.append([len(projectiles), Projectile('red', self.direction, self.rect.x, self.rect.y, len(projectiles), 20)])
                    elif item_num == 18:
                        inventory.hotbar_slots['slot_' + str(hotbar_selector_slots + 1)][3] -= 1
                        projectiles.append([len(projectiles), Projectile('green', self.direction, self.rect.x, self.rect.y, len(projectiles), 20)])
                    elif item_num == 19:
                        inventory.hotbar_slots['slot_' + str(hotbar_selector_slots + 1)][3] -= 1
                        projectiles.append([len(projectiles), Projectile('blue', self.direction, self.rect.x, self.rect.y, len(projectiles), 20)])
                    elif item_num == 20:
                        inventory.hotbar_slots['slot_' + str(hotbar_selector_slots + 1)][3] -= 1
                        projectiles.append([len(projectiles), Projectile('yellow', self.direction, self.rect.x, self.rect.y, len(projectiles), 20)])

                self.broken = True
            elif self.broken == True:
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_q:
                        self.chop_timer = 0
                        self.broken = False
                        self.chopping = False
            else:
                self.chop_timer += 1
        if debug == True:
            pygame.draw.rect(screen, (255, 255, 255), item_rect, 2)
            
class Cotten_Candy():
    def __init__(self, entity_num, x, y):
        self.front_walk = []
        self.back_walk = []
        self.right_walk = []
        self.left_walk = []
        for num in range(1,5):
            temp_front_walk_img = pygame.image.load(f'game_files/imgs/entities/cotten_candy_front_{num}.png')
            temp_front_walk_img = pygame.transform.scale(temp_front_walk_img, (tile_size * 2, tile_size * 4))
            self.front_walk.append(temp_front_walk_img)
            temp_back_walk_img = pygame.image.load(f'game_files/imgs/entities/cotten_candy_back_{num}.png')
            temp_back_walk_img = pygame.transform.scale(temp_back_walk_img, (tile_size * 2, tile_size * 4))
            self.back_walk.append(temp_back_walk_img)
            temp_right_walk_img = pygame.image.load(f'game_files/imgs/entities/cotten_candy_side_{num}.png')
            temp_right_walk_img = pygame.transform.scale(temp_right_walk_img, (tile_size * 2, tile_size * 4))
            self.right_walk.append(temp_right_walk_img)
            temp_left_walk_img = pygame.transform.flip(temp_right_walk_img, 180, 0)
            self.left_walk.append(temp_left_walk_img)
        self.img = self.front_walk[0]
        self.rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.health = 20
        self.walk_count = 0
        self.direction = random.choice([1, 2, 3, 4])
        self.entity_num = entity_num
        self.direction = 0
        self.attack_cooldown = 0
        self.animation_switch_counter =  0
    def update(self):
        if self.health <= 0:
            for tile in entities:
                if tile [0] == self.entity_num:  
                    entities_index = entities.index(tile)
            entities.pop(entities_index)
            for tile in drop_map:
                #rect, target chunk, tile
                if tile[0].collidepoint(self.rect.centerx, self.rect.centery):
                    drop_item_location = tile
                    break
            game_map_interactables[drop_item_location[1]].append([drop_item_location[2][0], 6, 12])
        else:
            distance = math.sqrt(((player.hitbox.centerx - self.rect.centerx) ** 2) + ((player.hitbox.centery - self.rect.centery) ** 2))
            self.rect.x = self.x - scroll[0]
            self.rect.y = self.y - scroll[1]
            #4000
            if distance < 40000000000000:
                if player.hitbox.centerx > self.rect.centerx:
                    self.x += 1
                    self.direction = 3
                elif player.rect.centerx < self.rect.centerx:
                    self.x -= 1
                    self.direction = 1
                if player.hitbox.centery > self.rect.centery:
                    self.y += 1
                    self.direction = 2
                elif player.hitbox.centery < self.rect.centery:
                    self.y -= 1
                    self.direction = 0
            if self.walk_count == 3:
                self.walk_count = 0 
            elif self.animation_switch_counter >= 2:
                self.walk_count += 1
                self.animation_switch_counter = 0
            else:
                self.animation_switch_counter += 1
            #collision
            if distance <= 50:
                if self.attack_cooldown == 14:
                    player.damage(2)
                    self.attack_cooldown = 0
                else:
                    self.attack_cooldown += 1
            #wsad based
            if self.direction == 0:
                self.img  = self.back_walk[self.walk_count]
            elif self.direction == 2:
                self.img  = self.front_walk[self.walk_count]
            elif self.direction  == 1:
                self.img  = self.left_walk[self.walk_count]
            elif self.direction == 3:
                self.img  = self.right_walk[self.walk_count]
            screen.blit(self.img, self.rect)
            if debug == True:
                pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
class Gelatin():
    def __init__(self, entity_num, x, y):
        self.colour = random.choice(['red', 'yellow', 'blue', 'green'])
        self.front_walk = []
        self.back_walk = []
        self.right_walk = []
        self.left_walk = []
        for num in range(1,3):
            temp_front_walk_img = pygame.image.load('game_files/imgs/entities/gelatin_front_' + self.colour + f'_{num}.png')
            temp_front_walk_img = pygame.transform.scale(temp_front_walk_img, (tile_size * 2, tile_size * 4))
            self.front_walk.append(temp_front_walk_img)
            temp_back_walk_img = pygame.image.load('game_files/imgs/entities/gelatin_back_' + self.colour + f'_{num}.png')
            temp_back_walk_img = pygame.transform.scale(temp_back_walk_img, (tile_size * 2, tile_size * 4))
            self.back_walk.append(temp_back_walk_img)
            temp_right_walk_img = pygame.image.load('game_files/imgs/entities/gelatin_side_' + self.colour + f'_{num}.png')
            temp_right_walk_img = pygame.transform.scale(temp_right_walk_img, (tile_size * 2, tile_size * 4))
            self.right_walk.append(temp_right_walk_img)
            temp_left_walk_img = pygame.transform.flip(temp_right_walk_img, 180, 0)
            self.left_walk.append(temp_left_walk_img)
        self.img = self.front_walk[0]
        self.rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        self.health = 20
        self.walk_count = 0
        self.direction = random.choice([1, 2, 3, 4])
        self.entity_num = entity_num
        self.direction = 0
        self.attack_cooldown = 0
    def update(self):
        if self.health <= 0:
            for tile in entities:
                if tile [0] == self.entity_num:  
                    entities_index = entities.index(tile)
            entities.pop(entities_index)
            for tile in drop_map:
                #rect, target chunk, tile
                if tile[0].collidepoint(self.rect.centerx, self.rect.centery):
                    drop_item_location = tile
                    break
            if self.colour == 'red':
                game_map_interactables[drop_item_location[1]].append([drop_item_location[2][0], 7, 12])
            elif self.colour == 'green':
                game_map_interactables[drop_item_location[1]].append([drop_item_location[2][0], 8, 12])
            elif self.colour == 'blue':
                game_map_interactables[drop_item_location[1]].append([drop_item_location[2][0], 9, 12])
            elif self.colour == 'yellow':
                game_map_interactables[drop_item_location[1]].append([drop_item_location[2][0], 10, 12])
        else:
            distance = math.sqrt(((player.hitbox.centerx - self.rect.centerx) ** 2) + ((player.hitbox.centery - self.rect.centery) ** 2))
            self.rect.x = self.x - scroll[0]
            self.rect.y = self.y - scroll[1]
            #4000
            if distance < 40000000000000:
                if player.hitbox.centerx > self.rect.centerx:
                    self.x += 1
                    self.direction = 3
                elif player.rect.centerx < self.rect.centerx:
                    self.x -= 1
                    self.direction = 1
                if player.hitbox.centery > self.rect.centery:
                    self.y += 1
                    self.direction = 2
                elif player.hitbox.centery < self.rect.centery:
                    self.y -= 1
                    self.direction = 0
            if self.walk_count == 1:
                self.walk_count = 0 
            else:
                self.walk_count += 1
            #collision
            if distance <= 200:
                if self.attack_cooldown == 10:
                    self.attack_cooldown = 0
                    global projectiles
                    projectiles.append([len(projectiles), Projectile(self.colour, self.direction, self.x, self.y, len(projectiles), 25)])
                else:
                    self.attack_cooldown += 1
            #base on wsad
            if self.direction == 0:
                self.img  = self.back_walk[self.walk_count]
            elif self.direction == 2:
                self.img  = self.front_walk[self.walk_count]
            elif self.direction  == 1:
                self.img  = self.left_walk[self.walk_count]
            elif self.direction == 3:
                self.img  = self.right_walk[self.walk_count]
            screen.blit(self.img, self.rect)
            if debug == True:
                pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)

class Projectile():
    def __init__(self, colour, direction, x, y, projectile_num, hit_timer):
        self.colour = colour
        self.hit_timer = hit_timer
        self.projectile_num = projectile_num
        self.direction = direction
        if self.colour == 'red':
            self.img = red_gelatin
        elif self.colour == 'green':
            self.img = green_gelatin
        elif self.colour == 'blue':
            self.img = blue_gelatin
        elif self.colour == 'yellow':
            self.img = yellow_gelatin
        self.rect = self.img.get_rect()
        self.x = x
        self.y = y
        self.rect.centerx = self.x
        self.rect.centery = self.y
        if self.direction == 3:
            self.x_change = -4
            self.y_change = 0
        elif self.direction == 1:
            self.x_change = 4
            self.y_change = 0
        elif self.direction == 2:
            self.x_change = 0
            self.y_change = -4
        elif self.direction == 0:
            self.x_change = 0
            self.y_change = 4
        
    def update(self):
        self.hit_timer -= 1
        if self.rect.colliderect(player.hitbox) and self.hit_timer <= 0:
            for tile in projectiles:
                if tile [0] == self.projectile_num:  
                    projectiles_index = projectiles.index(tile)
            projectiles.pop(projectiles_index)
            player.damage(2)
        for tile in entities:
            if self.rect.colliderect(tile[1].rect)  and self.hit_timer <= 0:
                tile[1].health -= 1
                for tile in projectiles:
                    if tile [0] == self.projectile_num:  
                        projectiles_index = projectiles.index(tile)
                projectiles.pop(projectiles_index)
                break
        self.rect.x = self.x - scroll[0]
        self.rect.y = self.y - scroll[1]
        self.x -= self.x_change
        self.y -= self.y_change
        screen.blit(self.img, self.rect)
        if debug == True:
            pygame.draw.rect(screen, (255, 0, 0), self.rect, 2)
        
#gui classes
class Hotbar():
    def __init__(self):
        img_selected = pygame.image.load('game_files/imgs/gui/inventory_slot_selected.png')
        self.img_selected = pygame.transform.scale(img_selected, (tile_size *3, tile_size *3))
        hotbar_img = pygame.image.load('game_files/imgs/gui/hotbar.png')
        self.hotbar_img = pygame.transform.scale(hotbar_img, (tile_size *15, tile_size * 3))
        self.hotbar_rect = self.hotbar_img.get_rect()
        hotbar_bg = pygame.image.load('game_files/imgs/gui/hotbar_bg.png')
        self.hotbar_bg = pygame.transform.scale(hotbar_bg, (tile_size *15, tile_size * 3))
        #first is item ID, second is stack size
        self.selector = [[self.hotbar_rect.x, self.hotbar_rect.y], self.img_selected]
        self.selector_slot = 0
        self.hotbar_slots = { 'slot_1': [0, 0],
                             'slot_2': [0, 0],
                             'slot_3': [0, 0],
                             'slot_4': [0, 0],
                             'slot_5': [0, 0],
                             }
        self.selected_item = 0
    def update(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_1]:
            self.selector_slot = 0
            self.selected_item = self.hotbar_slots['slot_1'][0]
        if key[pygame.K_2]:
            self.selector_slot = 1
            self.selected_item = self.hotbar_slots['slot_2'][0]
        if key[pygame.K_3]:
            self.selector_slot = 2
            self.selected_item = self.hotbar_slots['slot_3'][0]
        if key[pygame.K_4]:
            self.selector_slot = 3
            self.selected_item = self.hotbar_slots['slot_4'][0]
        if key[pygame.K_5]:
            self.selector_slot = 4
            self.selected_item = self.hotbar_slots['slot_5'][0]
        self.hotbar_rect.centerx = 300
        self.hotbar_rect.y = 540
        
        self.selector = [[self.hotbar_rect.x + (tile_size * self.selector_slot * 3), self.hotbar_rect.y], self.img_selected]
        screen.blit(self.hotbar_bg, self.hotbar_rect)
        screen.blit(self.hotbar_img, self.hotbar_rect)
        for num in range (1, 6):
            if inventory.hotbar_slots[f'slot_{num}'][3] == 0:
                inventory.hotbar_slots[f'slot_{num}'][2] = 0
            self.hotbar_slots[f'slot_{num}'][0] = inventory.hotbar_slots[f'slot_{num}'][2]
            self.hotbar_slots[f'slot_{num}'][1] = inventory.hotbar_slots[f'slot_{num}'][3]
            screen.blit(item_index[self.hotbar_slots[f'slot_{num}'][0]], (self.hotbar_rect.x + (tile_size * 3 * (num - 1)), self.hotbar_rect.y))
            if self.hotbar_slots[f'slot_{num}'][1] != 0:
                draw_text(str([self.hotbar_slots[f'slot_{num}'][1]]), font_inventory, white, self.hotbar_rect.x + (tile_size * 3 * (num - 1)) + 9, self.hotbar_rect.y + (tile_size * 1.8))
        screen.blit(self.selector[1],(self.selector[0][0], self.selector[0][1]))

class Inventory():
    def __init__(self):
        inventory_img = pygame.image.load('game_files/imgs/gui/inventory.png')
        self.inventory_img = pygame.transform.scale(inventory_img, (tile_size * 15, tile_size * 12))
        self.inventory_rect = self.inventory_img.get_rect()
        self.inventory_rect.centerx = 300
        self.inventory_rect.centery = 300

        hotbar_img = pygame.image.load('game_files/imgs/gui/inventory_hotbar.png')
        self.hotbar_img = pygame.transform.scale(hotbar_img, (tile_size * 15, tile_size * 3))
        self.hotbar_rect = self.hotbar_img.get_rect()
        self.hotbar_rect.centerx = self.inventory_rect.centerx
        self.hotbar_rect.y = self.inventory_rect.y + 195
        self.hotbar_slots = hotbar.hotbar_slots
        
        armour_img = pygame.image.load('game_files/imgs/gui/armour_slots.png')
        self.armour_img = pygame.transform.scale(armour_img, (tile_size * 3, tile_size * 12))
        self.armour_rect = self.armour_img.get_rect()
        self.armour_rect.centerx = 200 - (tile_size * 3)
        self.armour_rect.y = self.inventory_rect.y
        helmet_img = pygame.image.load('game_files/imgs/gui/armour_slot_helmet.png')
        self.helmet_img = pygame.transform.scale(helmet_img, (tile_size * 3, tile_size * 3))
        chestplate_img = pygame.image.load('game_files/imgs/gui/armour_slot_chestplate.png')
        self.chestplate_img = pygame.transform.scale(chestplate_img, (tile_size * 3, tile_size * 3))
        legs_img = pygame.image.load('game_files/imgs/gui/armour_slot_legs.png')
        self.legs_img = pygame.transform.scale(legs_img, (tile_size * 3, tile_size * 3))
        boots_img = pygame.image.load('game_files/imgs/gui/armour_slot_boots.png')
        self.boots_img = pygame.transform.scale(boots_img, (tile_size * 3, tile_size * 3))
        
        self.slot_img = pygame.transform.scale(inventory_slot, (tile_size *3, tile_size * 3))
        self.slots = {}
        self.armour_slots = {}
        self.hotbar_slots = {}
        coord = 0
        #0: slot img, 1:rectangle for slot, 3: item ID, 4: stack size
        for num in range(1,21):
            if coord > 4:
                coord = 0
            if 1 <= num <= 5:
                rect = self.slot_img.get_rect()
                rect.x = self.inventory_rect.x + (tile_size * 3 * coord)
                rect.y =  self.inventory_rect.y
                self.slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            if 6 <= num <= 10:
                rect = self.slot_img.get_rect()
                rect.x = self.inventory_rect.x + (tile_size * 3 * coord)
                rect.y =  self.inventory_rect.y + (tile_size * 3)
                self.slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            if 11 <= num <= 15:
                rect = self.slot_img.get_rect()
                rect.x = self.inventory_rect.x + (tile_size * 3 * coord)
                rect.y =  self.inventory_rect.y  + (tile_size * 3 * 2)
                self.slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            if 16 <= num <= 20:
                rect = self.slot_img.get_rect()
                rect.x = self.inventory_rect.x + (tile_size * 3 * coord)
                rect.y =  self.inventory_rect.y  + (tile_size * 3 * 3)
                self.slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            coord += 1
        coord = 0
        for num in range(1, 5):
            if num == 1:
               rect = self.helmet_img.get_rect()
               rect.x = self.armour_rect.x
               rect.y =  self.armour_rect.y + (tile_size * 3 * coord)
               self.armour_slots[f'slot_{num}'] = [self.helmet_img, rect, 0, 0, 0]
            if num == 2:
                rect = self.chestplate_img.get_rect()
                rect.x = self.armour_rect.x
                rect.y =  self.armour_rect.y + (tile_size * 3 * coord)
                self.armour_slots[f'slot_{num}'] = [self.chestplate_img, rect, 0, 0, 0]
            if num == 3:
                rect = self.legs_img.get_rect() 
                rect.x = self.armour_rect.x 
                rect.y =  self.armour_rect.y + (tile_size * 3 * coord)
                self.armour_slots[f'slot_{num}'] = [self.legs_img, rect, 0, 0, 0]
            if num == 4:
                rect = self.boots_img.get_rect()
                rect.x = self.armour_rect.x
                rect.y =  self.armour_rect.y + (tile_size * 3 * coord)
                self.armour_slots[f'slot_{num}'] = [self.boots_img, rect, 0, 0, 0]
            coord += 1
        coord = 0
        for num in range(1, 6):
            rect = self.slot_img.get_rect()
            rect.x = self.hotbar_rect.x + (tile_size * 3 * coord)
            rect.y =  self.hotbar_rect.y
            self.hotbar_slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            coord += 1
    def update(self):
        screen.blit(self.inventory_img, self.inventory_rect)
        screen.blit(self.armour_img, self.armour_rect)
        screen.blit(self.hotbar_img, self.hotbar_rect)
        for num in range(1,6):
            if self.hotbar_slots[f'slot_{num}'][3] == 0:
                self.hotbar_slots[f'slot_{num}'][2] = 0
            screen.blit(self.hotbar_slots[f'slot_{num}'][0], self.hotbar_slots[f'slot_{num}'][1])
            screen.blit(item_index[self.hotbar_slots[f'slot_{num}'][2]], self.hotbar_slots[f'slot_{num}'][1])
            if self.hotbar_slots[f'slot_{num}'][3] != 0:
                draw_text(str([self.hotbar_slots[f'slot_{num}'][3]]), font_inventory, white, self.hotbar_slots[f'slot_{num}'][1].x + 9, self.hotbar_slots[f'slot_{num}'][1].y + (tile_size * 1.8))
        for num in range(1, 21):
            screen.blit(self.slots[f'slot_{num}'][0], self.slots[f'slot_{num}'][1])
            screen.blit(item_index[self.slots[f'slot_{num}'][2]], self.slots[f'slot_{num}'][1])
            if self.slots[f'slot_{num}'][3] != 0:
                draw_text(str([self.slots[f'slot_{num}'][3]]), font_inventory, white, self.slots[f'slot_{num}'][1].x + 9, self.slots[f'slot_{num}'][1].y + (tile_size * 1.8))
        for num in range(1, 5):
            screen.blit(self.armour_slots[f'slot_{num}'][0], self.armour_slots[f'slot_{num}'][1])
            screen.blit(item_index[self.armour_slots[f'slot_{num}'][2]], self.armour_slots[f'slot_{num}'][1])


class Crafting():
    def __init__(self):
        grid_img = pygame.image.load('game_files/imgs/gui/crafting_grid.png')
        self.grid_img = pygame.transform.scale(grid_img, (tile_size * 15, tile_size * 9))
        self.grid_rect = self.grid_img.get_rect()
        self.grid_rect.centerx = 300
        self.grid_rect.y = 55
        self.slot_img = pygame.transform.scale(inventory_slot, (tile_size *3, tile_size * 3))
        arrow = pygame.image.load('game_files/imgs/gui/crafting_arrow.png')
        self.arrow = pygame.transform.scale(arrow, (tile_size * 3, tile_size * 3))
        self.slots = {}
        self.crafting = []
        coord = 0
        for num in range(1, 11):
            if coord > 2:
                coord = 0
            if 1 <= num <= 3:
                rect = self.slot_img.get_rect()
                rect.x = self.grid_rect.x + (tile_size * 3 * coord)
                rect.y =  self.grid_rect.y
                self.slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            if 4 <= num <= 6:
                rect = self.slot_img.get_rect()
                rect.x = self.grid_rect.x + (tile_size * 3 * coord)
                rect.y =  self.grid_rect.y + (tile_size * 3 * 1)
                self.slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            if 7 <= num <= 9:
                rect = self.slot_img.get_rect()
                rect.x = self.grid_rect.x + (tile_size * 3 * coord)
                rect.y =  self.grid_rect.y + (tile_size * 3 * 2)
                self.slots[f'slot_{num}'] = [self.slot_img, rect, 0, 0]
            coord += 1
            if num == 10:
                rect = self.slot_img.get_rect()
                rect.x = self.grid_rect.x + (tile_size * 3 * 4)
                rect.y =  self.grid_rect.y + (tile_size * 3)
                self.slots['slot_10'] = [self.slot_img, rect, 0, 0]
    def update(self):
        self.crafting = []
        for num in range (1, 10):
            self.crafting.append(self.slots[f'slot_{num}'][2])
        for tile in crafting_recepies:
            if self.crafting == crafting_recepies[tile][0]:
                self.slots['slot_10'][2] = crafting_recepies[tile][1][0]
                self.slots['slot_10'][3] = crafting_recepies[tile][1][1]
                break
            else:
                self.slots['slot_10'][2] = 0
                self.slots['slot_10'][3] = 0
        screen.blit(self.grid_img, self.grid_rect)
        for num in range(1,11):
            screen.blit(self.slots[f'slot_{num}'][0], self.slots[f'slot_{num}'][1])
            screen.blit(item_index[self.slots[f'slot_{num}'][2]], self.slots[f'slot_{num}'][1])
            if self.slots[f'slot_{num}'][3] != 0:
                draw_text(str([self.slots[f'slot_{num}'][3]]), font_inventory, white, self.slots[f'slot_{num}'][1].x + 9, self.slots[f'slot_{num}'][1].y + (tile_size * 1.8))
        screen.blit(self.arrow, (self.grid_rect.x + (tile_size * 9), self.grid_rect.y + (tile_size * 3)))


class Selector():
    def __init__(self):
        selector_img = pygame.image.load('game_files/imgs/gui/inventory_slot_selected.png')
        self.img = pygame.transform.scale(selector_img, (tile_size *3, tile_size *3))
        self.selected = False
        self.select_one = 0
        self.declick = False
        self.declick_two = False
        self.click_count = 0
        self.select_one_location = []
        self.crafted = False
    
    def update(self):
        key = pygame.key.get_pressed()
        pos = pygame.mouse.get_pos()
        if self.selected == False and self.click_count > 4:
            if event.type == pygame.MOUSEBUTTONUP:
                self.declick = True
            if self.declick == True:
                for num in range(1,21):
                    if inventory.slots[f'slot_{num}'][2] <= 0 or inventory.slots[f'slot_{num}'][3] <= 0:
                        inventory.slots[f'slot_{num}'][2] = 0
                        inventory.slots[f'slot_{num}'][3] = 0
                    if inventory.slots[f'slot_{num}'][1].collidepoint(pos):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            #self.select_one =
                            self.selector_pos = inventory.slots[f'slot_{num}'][1]
                            self.selected = True
                            self.declick = False
                            self.select_one_location = [1, num]
                            self.click_count = 0
                            self.selected_item = inventory.slots[f'slot_{num}'][2]
                for num in range(1,5):
                    if inventory.armour_slots[f'slot_{num}'][2] <= 0 or inventory.armour_slots[f'slot_{num}'][3] <= 0:
                        inventory.armour_slots[f'slot_{num}'][2] = 0
                        inventory.armour_slots[f'slot_{num}'][3] = 0
                    if inventory.armour_slots[f'slot_{num}'][1].collidepoint(pos):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.selector_pos = inventory.armour_slots[f'slot_{num}'][1]
                            self.selected = True
                            self.declick = False
                            self.select_one_location = [2, num]
                            self.click_count = 0
                            self.selected_item = inventory.armour_slots[f'slot_{num}'][2]
                for num in range(1,6):
                    if inventory.hotbar_slots[f'slot_{num}'][2] <= 0 or inventory.hotbar_slots[f'slot_{num}'][3] <= 0:
                        inventory.hotbar_slots[f'slot_{num}'][2] = 0
                        inventory.hotbar_slots[f'slot_{num}'][3] = 0
                    if inventory.hotbar_slots[f'slot_{num}'][1].collidepoint(pos):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.selector_pos = inventory.hotbar_slots[f'slot_{num}'][1]
                            self.selected = True
                            self.declick = False
                            self.select_one_location = [3, num]
                            self.click_count = 0
                            self.selected_item = inventory.hotbar_slots[f'slot_{num}'][2]
                for num in range(1,11):
                    if crafting.slots[f'slot_{num}'][2] <= 0 or crafting.slots[f'slot_{num}'][3] <= 0:
                        crafting.slots[f'slot_{num}'][2] = 0
                        crafting.slots[f'slot_{num}'][3] = 0
                    if crafting.slots[f'slot_{num}'][1].collidepoint(pos):
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            self.selector_pos = crafting.slots[f'slot_{num}'][1]
                            self.selected = True
                            self.declick = False
                            self.select_one_location = [4, num]
                            self.click_count = 0
                            self.selected_item = crafting.slots[f'slot_{num}'][2]

        elif self.selected == True and self.click_count > 4:
            screen.blit(self.img, self.selector_pos)
            #draw text here
            img = font.render(item_data[str(self.selected_item)][0], True, white)
            txt_rect = img.get_rect()
            txt_rect.centerx = 300
            txt_rect.centery = 500
            screen.blit(img, txt_rect)
            if event.type == pygame.MOUSEBUTTONUP:
                self.declick_two = True
            if self.declick_two == True:
                if key[pygame.K_DELETE]:
                    if self.select_one_location[0] == 1:
                        inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                        inventory.slots[f'slot_{self.select_one_location[1]}'][3] = 0
                    elif self.select_one_location[0] == 2: 
                        inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                        inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] = 0
                    elif self.select_one_location[0] == 3: 
                        inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] =0
                        inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] = 0
                    elif self.select_one_location[0] == 4:  
                        crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                        crafting.slots[f'slot_{self.select_one_location[1]}'][3] = 0  
                    self.selected = False
                    self.declick = False
                    self.click_count = 0
                else:
                    for num in range(1,21):
                        if inventory.slots[f'slot_{num}'][1].collidepoint(pos):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.select_one_location[0] == 1:
                                    if inventory.slots[f'slot_{self.select_one_location[1]}'][1] != inventory.slots[f'slot_{num}'][1]:
                                        if inventory.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.slots[f'slot_{num}'][2]:
                                             if inventory.slots[f'slot_{num}'][2] == 0:
                                                if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                    inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                                    if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                        inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                                else:
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                             else:
                                                inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                        elif inventory.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.slots[f'slot_{num}'][2]:
                                               if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.slots[f'slot_{num}'][2])][2] == True:
                                                  inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                                  if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                      inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                               elif item_data[str(inventory.slots[f'slot_{num}'][2])][2] == False:
                                                    inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                               else:
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 2: 
                                    if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] != inventory.slots[f'slot_{num}'][2]:
                                         if inventory.slots[f'slot_{num}'][2] == 0:
                                            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                inventory.slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                                if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                    inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                            else:
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                         else:
                                            inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                            inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] == inventory.slots[f'slot_{num}'][2]:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.slots[f'slot_{num}'][2])][2] == True:
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                              if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                  inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           elif item_data[str(inventory.slots[f'slot_{num}'][2])][2] == False:
                                                inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                           else:
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 3: 
                                    if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] != inventory.slots[f'slot_{num}'][2]:
                                         if inventory.slots[f'slot_{num}'][2] == 0:
                                            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                inventory.slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                                if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                    inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                            else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                         else:
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] == inventory.slots[f'slot_{num}'][2]:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.slots[f'slot_{num}'][2])][2] == True:
                                              inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                              if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                  inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           elif item_data[str(inventory.slots[f'slot_{num}'][2])][2] == False:
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                           else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 4: 
                                    if self.select_one_location[1] == 10:
                                        if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.slots[f'slot_{num}'][2]:
                                             if inventory.slots[f'slot_{num}'][2] == 0:
                                                 crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                 crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                                 self.crafted = True
                                        elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.slots[f'slot_{num}'][2]:
                                               if item_data[str(inventory.slots[f'slot_{num}'][2])][2] == False:
                                                   pass
                                               else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]
                                                   self.crafted = True
                                    else:
                                        if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.slots[f'slot_{num}'][2]:
                                             if inventory.slots[f'slot_{num}'][2] == 0:
                                                if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                    inventory.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                                    if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                        crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                                else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                             else:
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                        elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.slots[f'slot_{num}'][2]:
                                               if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.slots[f'slot_{num}'][2])][2] == True:
                                                  crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                                  if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                      crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                               elif item_data[str(inventory.slots[f'slot_{num}'][2])][2] == False:
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                               else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]
                                if self.crafted == True:
                                    for num in range(1, 10):
                                        if crafting.slots[f'slot_{num}'][3] > 0:
                                            crafting.slots[f'slot_{num}'][3] -= 1
                                    self.crafted = False
                                self.selected = False
                                self.declick = False
                                self.click_count = 0
                    for num in range(1,5):
                        if inventory.armour_slots[f'slot_{num}'][1].collidepoint(pos):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.select_one_location[0] == 1:
                                    if inventory.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.armour_slots[f'slot_{num}'][2]:
                                        if inventory.armour_slots[f'slot_{num}'][2] == 0:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                               inventory.armour_slots[f'slot_{num}'][2] = inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                               if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           else:
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                        else:
                                           inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                           inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.armour_slots[f'slot_{num}'][2]:
                                          if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == True:
                                             inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.armour_slots[f'slot_{num}'][3] + 1
                                             if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                 inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                          elif item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == False:
                                               inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                          else:
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.armour_slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 2 and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][1] != inventory.armour_slots[f'slot_{num}'][1]: 
                                    if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] != inventory.armour_slots[f'slot_{num}'][2]:
                                        if inventory.armour_slots[f'slot_{num}'][2] == 0:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                               inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.armour_slots[f'slot_{num}'][3] + 1
                                               if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                   inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           else:
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                        else:
                                           inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                           inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] == inventory.armour_slots[f'slot_{num}'][2]:
                                          if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == True:
                                             inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.armour_slots[f'slot_{num}'][3] + 1
                                             if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                 inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                          elif item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == False:
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                          else:
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] + inventory.armour_slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 3: 
                                    if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] != inventory.armour_slots[f'slot_{num}'][2]:
                                         if inventory.armour_slots[f'slot_{num}'][2] == 0:
                                            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                inventory.armour_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.slots[f'slot_{num}'][3] + 1
                                                if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                    inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                            else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                         else:
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] == inventory.armour_slots[f'slot_{num}'][2]:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == True:
                                              inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.armour_slots[f'slot_{num}'][3] + 1
                                              if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                  inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           elif item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == False:
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                           else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] + inventory.armour_slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 4:  
                                    if self.select_one_location[1] == 10:
                                        if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.armour_slots[f'slot_{num}'][2]:
                                             if inventory.armour_slots[f'slot_{num}'][2] == 0:
                                                 crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                 crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                                 self.crafted = True
                                        elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.armour_slots[f'slot_{num}'][2]:
                                               if item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == False:
                                                   pass
                                               else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.armour_slots[f'slot_{num}'][3]
                                                   self.crafted = True
                                    else:
                                        if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.armour_slots[f'slot_{num}'][2]:
                                             if inventory.armour_slots[f'slot_{num}'][2] == 0:
                                                if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                    inventory.armour_slots[f'slot_{num}'][2] = crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.armour_slots[f'slot_{num}'][3] + 1
                                                    if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                        crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                                else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                             else:
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                        elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.armour_slots[f'slot_{num}'][2]:
                                               if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == True:
                                                  crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.armour_slots[f'slot_{num}'][3] + 1
                                                  if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                      crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                               elif item_data[str(inventory.armour_slots[f'slot_{num}'][2])][2] == False:
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.armour_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.armour_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                               else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.slots[f'slot_{num}'][3]                                            
                                if self.crafted == True:
                                    for num in range(1, 10):
                                        if crafting.slots[f'slot_{num}'][3] > 0:
                                            crafting.slots[f'slot_{num}'][3] -= 1
                                    self.crafted = False
                                self.selected = False
                                self.declick = False
                                self.click_count = 0
                    for num in range(1,6):
                        if inventory.hotbar_slots[f'slot_{num}'][1].collidepoint(pos):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.select_one_location[0] == 1:
                                    if self.select_one_location[0] == 1:
                                        if inventory.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.hotbar_slots[f'slot_{num}'][2]:
                                             if inventory.hotbar_slots[f'slot_{num}'][2] == 0:
                                                if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                    inventory.hotbar_slots[f'slot_{num}'][2] = inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                                    if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                        inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                                else:
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                             else:
                                                inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                        elif inventory.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.hotbar_slots[f'slot_{num}'][2]:
                                               if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == True:
                                                  inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                                  if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                      inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                               elif item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == False:
                                                    inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                               else:
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.hotbar_slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 2: 
                                    if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] != inventory.hotbar_slots[f'slot_{num}'][2]:
                                        if inventory.hotbar_slots[f'slot_{num}'][2] == 0:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                               inventory.hotbar_slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                               if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                   inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           else:
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                        else:
                                           inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                           inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] == inventory.hotbar_slots[f'slot_{num}'][2]:
                                          if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == True:
                                             inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                             if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                 inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                          elif item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == False:
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                          else:
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] + inventory.hotbar_slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 3 and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][1] != inventory.hotbar_slots[f'slot_{num}'][1]: 
                                    if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] != inventory.hotbar_slots[f'slot_{num}'][2]:
                                         if inventory.hotbar_slots[f'slot_{num}'][2] == 0:
                                            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                                if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                    inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                            else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                         else:
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] == inventory.hotbar_slots[f'slot_{num}'][2]:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == True:
                                              inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                              if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                  inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           elif item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == False:
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                           else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] + inventory.hotbar_slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 4:  
                                    if self.select_one_location[1] == 10:
                                        if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.hotbar_slots[f'slot_{num}'][2]:
                                             if inventory.hotbar_slots[f'slot_{num}'][2] == 0:
                                                 crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                 crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                                 self.crafted = True
                                        elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.hotbar_slots[f'slot_{num}'][2]:
                                               if item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == False:
                                                   pass
                                               else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.hotbar_slots[f'slot_{num}'][3]
                                                   self.crafted = True
                                    else:
                                        if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != inventory.hotbar_slots[f'slot_{num}'][2]:
                                             if inventory.hotbar_slots[f'slot_{num}'][2] == 0:
                                                if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                    inventory.hotbar_slots[f'slot_{num}'][2] = crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                                    if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                        crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                                else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                             else:
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                        elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == inventory.hotbar_slots[f'slot_{num}'][2]:
                                               if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == True:
                                                  crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, inventory.hotbar_slots[f'slot_{num}'][3] + 1
                                                  if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                      crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                               elif item_data[str(inventory.hotbar_slots[f'slot_{num}'][2])][2] == False:
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                               else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], inventory.hotbar_slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], inventory.hotbar_slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + inventory.hotbar_slots[f'slot_{num}'][3]
                                if self.crafted == True:
                                    for num in range(1, 10):
                                        if crafting.slots[f'slot_{num}'][3] > 0:
                                            crafting.slots[f'slot_{num}'][3] -= 1
                                    self.crafted = False
                                self.selected = False
                                self.declick = False
                                self.click_count = 0
                    for num in range(1,10):
                        if crafting.slots[f'slot_{num}'][1].collidepoint(pos):
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                if self.select_one_location[0] == 1:
                                    if inventory.slots[f'slot_{self.select_one_location[1]}'][2] != crafting.slots[f'slot_{num}'][2]:
                                        if crafting.slots[f'slot_{num}'][2] == 0:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                               crafting.slots[f'slot_{num}'][2] = inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                               if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                   inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           else:
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                        else:
                                           inventory.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                           inventory.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.slots[f'slot_{self.select_one_location[1]}'][2] == crafting.slots[f'slot_{num}'][2]:
                                          if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(crafting.slots[f'slot_{num}'][2])][2] == True:
                                             inventory.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                             if inventory.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                 inventory.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                          elif item_data[str(crafting.slots[f'slot_{num}'][2])][2] == False:
                                               inventory.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.slots[f'slot_{self.select_one_location[1]}'][3]
                                          else:
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = 0, inventory.slots[f'slot_{self.select_one_location[1]}'][3] + crafting.slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 2: 
                                   if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] != crafting.slots[f'slot_{num}'][2]:
                                        if crafting.slots[f'slot_{num}'][2] == 0:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                               crafting.slots[f'slot_{num}'][2] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               crafting.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = inventory.slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                               if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                   inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           else:
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                        else:
                                           inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                           inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                   elif inventory.slots[f'slot_{self.select_one_location[1]}'][2] == crafting.slots[f'slot_{num}'][2]:
                                          if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(crafting.slots[f'slot_{num}'][2])][2] == True:
                                             inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                             if inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                 inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                          elif item_data[str(crafting.slots[f'slot_{num}'][2])][2] == False:
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.armour_slots[f'slot_{num}'][2], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.armour_slots[f'slot_{num}'][3], inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3]
                                          else:
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][2]   
                                              inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = 0, inventory.armour_slots[f'slot_{self.select_one_location[1]}'][3] + crafting.slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 3:
                                    if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] != crafting.slots[f'slot_{num}'][2]:
                                         if crafting.slots[f'slot_{num}'][2] == 0:
                                            if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                crafting.slots[f'slot_{num}'][2] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                                if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                    inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                            else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                         else:
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                            inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                    elif inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] == crafting.slots[f'slot_{num}'][2]:
                                           if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(crafting.slots[f'slot_{num}'][2])][2] == True:
                                              inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                              if inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                  inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                           elif item_data[str(crafting.slots[f'slot_{num}'][2])][2] == False:
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                                inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3]
                                           else:
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][2]   
                                               inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = 0, inventory.hotbar_slots[f'slot_{self.select_one_location[1]}'][3] + crafting.slots[f'slot_{num}'][3]
                                elif self.select_one_location[0] == 4 and crafting.slots[f'slot_{self.select_one_location[1]}'][1] != crafting.slots[f'slot_{num}'][1]:  
                                    if self.select_one_location[1] == 10:
                                        pass
                                    else:
                                        if crafting.slots[f'slot_{self.select_one_location[1]}'][2] != crafting.slots[f'slot_{num}'][2]:
                                             if crafting.slots[f'slot_{num}'][2] == 0:
                                                if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1:
                                                    crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                                    if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                        crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                                else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                             else:
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                crafting.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                        elif crafting.slots[f'slot_{self.select_one_location[1]}'][2] == crafting.slots[f'slot_{num}'][2]:
                                               if key[pygame.K_LSHIFT] or key[pygame.K_RSHIFT] and crafting.slots[f'slot_{self.select_one_location[1]}'][3] > 1 and item_data[str(crafting.slots[f'slot_{num}'][2])][2] == True:
                                                  crafting.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{self.select_one_location[1]}'][3] - 1, crafting.slots[f'slot_{num}'][3] + 1
                                                  if crafting.slots[f'slot_{self.select_one_location[1]}'][3] == 0:
                                                      crafting.slots[f'slot_{self.select_one_location[1]}'][2] = 0
                                               elif item_data[str(crafting.slots[f'slot_{num}'][2])][2] == False:
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = crafting.slots[f'slot_{num}'][2], crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                    crafting.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = crafting.slots[f'slot_{num}'][3], crafting.slots[f'slot_{self.select_one_location[1]}'][3]
                                               else:
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][2], crafting.slots[f'slot_{num}'][2] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][2]   
                                                   crafting.slots[f'slot_{self.select_one_location[1]}'][3], crafting.slots[f'slot_{num}'][3] = 0, crafting.slots[f'slot_{self.select_one_location[1]}'][3] + crafting.slots[f'slot_{num}'][3]
                                if self.crafted == True:
                                   for num in range(1, 10):
                                       if crafting.slots[f'slot_{num}'][3] > 0:
                                           crafting.slots[f'slot_{num}'][3] -= 1
                                   self.crafted = False
                                self.selected = False
                                self.declick = False
                                self.click_count = 0
        self.click_count += 1



class InputBox:
    def __init__(self, x, y, w, h, active_colour, inactive_colour, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.x = x
        self.rect.centerx = x
        self.rect.centery = y
        self.defult_y = y
        self.colour_active = active_colour
        self.colour_inactive = inactive_colour
        self.color = colour_inactive
        self.text = text
        self.txt_surface = font.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.colour_active if self.active else self.colour_inactive
        
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_DELETE:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.mod & pygame.KMOD_CTRL:
                    if event.key == pygame.K_v:
                        pasted = pyperclip.paste()
                        self.text += str(pasted)
                    elif event.key == pygame.K_c:
                        pyperclip.copy(self.text)
                    elif event.key == pygame.K_x:
                        pyperclip.copy(self.text)
                        self.text = ''
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = font.render(self.text, True, self.color)
    def update(self, scroll_amount):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.y = self.defult_y - scroll_amount
        self.rect.w = width
        self.rect.centerx = self.x
        return self.text

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)
        
class Button():
    def __init__(self, x, y, defult_image, hover_image, text, colour):
        self.defult_image = defult_image
        self.hover_image = hover_image
        self.image = self.defult_image
        self.defult_rect = self.defult_image.get_rect()
        self.hover_rect = self.hover_image.get_rect()
        self.defult_rect.centerx = x 
        self.defult_rect.centery = y 
        self.hover_rect.centerx = x 
        self.hover_rect.centery = y 
        self.rect = self.defult_rect
        self.clicked = False
        self.text = text
        self.colour = colour
        self.txt_surface = font.render(self.text, True, self.colour)
        self.text_width = self.txt_surface.get_width()
        self.defulty = self.rect.centery
    
    def draw(self, scroll_amount):
        self.rect.centery = self.defulty - scroll_amount
        action = False
        #get mouse position
        pos = pygame.mouse.get_pos()
        #check mouse over and click conditions
        if self.rect.collidepoint(pos):
            self.image = self.hover_image
            self.rect = self.hover_rect
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
        else:
            self.image = self.defult_image
            self.rect = self.defult_rect
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        #draw button
        screen.blit(self.image, self.rect)
        screen.blit(self.txt_surface, (self.rect.centerx - (self.text_width / 2), self.rect.centery - 15))
        return action
    def reset_rect(self):
        self.rect = self.defult_rect

class Select_World():
    def __init__(self):
        self.selector_img = pygame.image.load('game_files/imgs/gui/world_selector_box.png')
        self.selected_img = pygame.image.load('game_files/imgs/gui/world_selected.png')
        self.world_num = 0
        self.world_select_bg = pygame.image.load('game_files/imgs/gui/world_selection_bg.png')
        #self.world_select_bg = pygame.transform.scale(world_select_bg, (tile_size * 29, tile_size * 20))
        self.world_select_bg_rect = self.world_select_bg.get_rect()
        self.world_select_bg_rect.centerx = 300
        self.world_select_bg_rect.centery = 300
        self.world_1_rect = self.selector_img.get_rect()
        self.world_1_rect.centerx = 300
        self.world_1_rect.centery = self.world_select_bg_rect.centery - 128
        self.world_2_rect = self.selector_img.get_rect()
        self.world_2_rect.centerx = 300
        self.world_2_rect.centery = self.world_select_bg_rect.centery - 64
        self.world_3_rect = self.selector_img.get_rect()
        self.world_3_rect.centerx = 300
        self.world_3_rect.centery = self.world_select_bg_rect.centery + 64
        self.world_4_rect = self.selector_img.get_rect()
        self.world_4_rect.centerx = 300
        self.world_4_rect.centery = self.world_select_bg_rect.centery + 128
    def update(self):
        pos = pygame.mouse.get_pos()
        if self.world_1_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 1:
                self.world_num = 0
            else:
                self.world_num = 1
        elif self.world_2_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 2:
                self.world_num = 0
            else:
                self.world_num = 2
        elif self.world_3_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 3:
                self.world_num = 0
            else:
                self.world_num = 3
        elif self.world_4_rect.collidepoint(pos) and pygame.mouse.get_pressed()[0] == 1:
            if self.world_num == 4:
                self.world_num = 0
            else:
                self.world_num = 4
        screen.blit(self.world_select_bg, (self.world_select_bg_rect.x, self.world_select_bg_rect.y))
        screen.blit(self.selector_img, (self.world_1_rect.x, self.world_1_rect.y))
        screen.blit(self.selector_img, (self.world_2_rect.x, self.world_2_rect.y))
        screen.blit(self.selector_img, (self.world_3_rect.x, self.world_3_rect.y))
        screen.blit(self.selector_img, (self.world_4_rect.x, self.world_4_rect.y))
        if self.world_num == 1:
            screen.blit(self.selected_img, (self.world_1_rect.x, self.world_1_rect.y))
        elif self.world_num == 2:
            screen.blit(self.selected_img, (self.world_2_rect.x, self.world_2_rect.y))
        elif self.world_num == 3:
            screen.blit(self.selected_img, (self.world_3_rect.x, self.world_3_rect.y))
        elif self.world_num == 4:
            screen.blit(self.selected_img, (self.world_4_rect.x, self.world_4_rect.y))
        return self.world_num

class Scroll_Bar():
    def __init__(self, length):
        image_unpressed = pygame.image.load('game_files/imgs/menu/scroll_bar.png')
        image_pressed = pygame.image.load('game_files/imgs/menu/scroll_bar_pressed.png')
        self.image_unpressed = pygame.transform.scale(image_unpressed, (tile_size * 1, tile_size * length))
        self.image_pressed = pygame.transform.scale(image_pressed, (tile_size * 1, tile_size * length))
        self.image = image_unpressed
        self.rect = self.image_unpressed.get_rect()
        self.rect.x = 600 - self.rect.width
        self.rect.y = 0
        self.scroll_wheel = 0
        self.scroll_count = 0
        self.clicked = False
        self.scroll_distence = 0
    def get_scroll_wheel(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_wheel = event.y
        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
    def update(self):
        pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] == 1 and self.rect.collidepoint(pos):
            self.clicked = True
        if self.clicked == True:
            self.image = self.image_pressed
            self.rect.centery = pos[1]
        else:
            self.image = self.image_unpressed     
        self.rect.centery += (-5 * scroll_sensitivity) * self.scroll_wheel
        if self.scroll_count <= 5:
            self.scroll_count += 1
        else:
            self.scroll_count = 0
            self.scroll_wheel = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600
        elif self.rect.top < 0:
            self.rect.top = 0
        screen.blit(self.image, self.rect)
        self.scroll_distence = self.rect.top
        return self.scroll_distence
class Slider():
    def __init__(self, x, y, length, knob_ratio, amount):
        self.length = int(length)
        slider_knob_img = pygame.image.load('game_files/imgs/menu/slider_knob.png')
        self.knob_img = pygame.transform.scale(slider_knob_img, (tile_size *2.5, tile_size * 2.5))
        slider_centre_img = pygame.image.load('game_files/imgs/menu/slider_centre.png')
        self.slider_centre_img = pygame.transform.scale(slider_centre_img, (tile_size *2, tile_size * 2))
        slider_left_img = pygame.image.load('game_files/imgs/menu/slider_end.png')
        self.slider_left_img = pygame.transform.scale(slider_left_img, (tile_size *2, tile_size * 2))
        self.slider_right_img = pygame.transform.flip(self.slider_left_img, 180, 0)
        self.rect = pygame.Rect(x, y, (tile_size * 2 * length), (tile_size * 2))
        self.knob_rect = self.knob_img.get_rect()
        self.knob_rect.centery = self.rect.centery
        self.knob_rect.centerx = self.rect.x + (knob_ratio * self.rect.width)
        self.defulty = self.rect.centery
        self.clicked = False
        self.distance = abs((self.rect.x) - self.knob_rect.centerx) 
        self.slider_amount = 0
        self.amount = amount
        self.ratio = knob_ratio
    def get_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONUP:
            self.clicked = False
    def update(self, scroll_amount):
        pos = pygame.mouse.get_pos()
        self.rect.y = self.defulty - scroll_amount
        self.knob_rect.centery = self.rect.centery
        screen.blit(self.slider_left_img, (self.rect.left, self.rect.y))
        screen.blit(self.slider_right_img, (self.rect.right - (tile_size * 2), self.rect.y))
        for num in range(1, self.length - 1):
            screen.blit(self.slider_centre_img, (self.rect.left + (tile_size * 2 * num), self.rect.y))
        if pygame.mouse.get_pressed()[0] == 1 and self.knob_rect.collidepoint(pos):
            self.clicked = True
        if self.clicked == True:
            self.knob_rect.centerx = pos[0]
        if self.knob_rect.centerx > self.rect.right:
            self.knob_rect.centerx = self.rect.right
        elif self.knob_rect.centerx < self.rect.left:
            self.knob_rect.centerx = self.rect.left
        screen.blit(self.knob_img, (self.knob_rect.x, self.knob_rect.y))
        self.distance = abs((self.rect.x) - self.knob_rect.centerx)
        self.ratio = self.distance / self.rect.width
        self.slider_amount = self.amount * self.ratio
        return self.slider_amount
            

#set input boxes
# settings_bg_colour, settings_bg_colour
world_name_input = InputBox(300, 180, 100, 30, colour_active, colour_inactive)
seed_input = InputBox(300, 250, 100, 30, colour_active, colour_inactive)
world_name_change = InputBox(300, 200, 100, 30, colour_active, colour_inactive) 
world_name_change_ingame = InputBox(350, 60, 100, 30, colour_active, colour_inactive) 
devtools_code = InputBox(350, 1050, 100, 30, settings_bg_colour_active, settings_bg_colour) 
#set classes
hotbar = Hotbar()
player = Player(293, 315)
inventory = Inventory()
crafting = Crafting()
selector = Selector()
select_world = Select_World()

#set buttons
back_to_game = Button(300, 220, button_img, button_hover_img, "Back to game", white)
ingame_settings_button = Button(300, 300, button_img, button_hover_img, "Settings", white)
save_and_quit_button = Button(300, 380, button_img, button_hover_img, "Save and Quit", white)
respawn_button = Button(300, 340, button_img, button_hover_img, "Respawn", white)
save_and_quit_button_dead = Button(300, 260, button_img, button_hover_img, "Save and Quit", white)
peaceful_button = Button(400, 350, button_img, button_hover_img, "Peaceful", white)
hostile_button = Button(200, 350, button_img, button_hover_img, "Hostile", white)
generate_world_button = Button(300, 450, button_img, button_hover_img, "Generate", white)
play_button = Button(300, 220, button_img, button_hover_img, "Play", white)
play_selected_button = Button(150, 550, button_img, button_hover_img, "Play", white)
create_button = Button(450, 550, button_img, button_hover_img, "Create", white)
select_back_button = Button(100, 50, button_img, button_hover_img, "Back", white)
delete_world_button = Button(300, 450, button_img, button_hover_img, "Delete World", white)
world_one_settings = Button(select_world.world_1_rect.right + 32, select_world.world_1_rect.centery, button_settings, button_settings_hover, "", white)
world_two_settings = Button(select_world.world_2_rect.right + 32, select_world.world_2_rect.centery, button_settings, button_settings_hover, "", white)
world_three_settings = Button(select_world.world_3_rect.right + 32, select_world.world_3_rect.centery, button_settings, button_settings_hover, "", white)
world_four_settings = Button(select_world.world_4_rect.right + 32, select_world.world_4_rect.centery, button_settings, button_settings_hover, "", white)
delete_yes_button = Button(400, 300, button_img, button_hover_img, "Yes", white)
delete_no_button = Button(200, 300, button_img, button_hover_img, "No", white)
settings_button = Button(300, 320, button_img, button_hover_img, "Settings", white)
quit_button = Button(300, 420, button_img, button_hover_img, "Quit", white)
how_to_play_button = Button(300, 400, button_img, button_hover_img, "Quit", white)
controls_button = Button(tile_size * 4, tile_size * 6, button_settings_game, button_settings_game, "Controls", white)
audio_settings_button = Button(tile_size * 4, tile_size * 10, button_settings_game, button_settings_game, "Audio", white)
back_settings_button = Button(tile_size * 4, tile_size * 2, button_settings_game, button_settings_game, "Back", white)
graphics_settings_button = Button(tile_size * 4, tile_size * 14, button_settings_game, button_settings_game, "Graphics", white)
credits_settings_button = Button(tile_size * 4, tile_size * 18, button_settings_game, button_settings_game, "Credits", white)
sfx_on_button = Button(400, 100, switch_on, switch_on, "", white)
sfx_off_button = Button(400, 100, switch_off, switch_off, "", white)
music_on_button = Button(400, 200, switch_on, switch_on, "", white)
music_off_button = Button(400, 200, switch_off, switch_off, "", white)
back_settings_button_ingame = Button(tile_size * 4, tile_size * 2, button_settings_game, button_settings_game, "Back", white)
world_settings_ingame = Button(tile_size * 4, tile_size * 6, button_settings_game, button_settings_game, "World", white)
controls_button_ingame = Button(tile_size * 4, tile_size * 10, button_settings_game, button_settings_game, "Controls", white)
audio_settings_button_ingame = Button(tile_size * 4, tile_size * 14, button_settings_game, button_settings_game, "Audio", white)
hostile_button_ingame = Button(230, 180, button_img, button_hover_img, "Hostile", white)
peaceful_button_ingame = Button(470, 180, button_img, button_hover_img, "Peaceful", white)
graphics_settings_button_ingame = Button(tile_size * 4, tile_size * 18, button_settings_game, button_settings_game, "Graphics", white)
coords_on_button = Button(420, 100, switch_on, switch_on, "", white)
coords_off_button = Button(420, 100, switch_off, switch_off, "", white)
#set scroll bars - max length 37
controls_scroll_bar = Scroll_Bar(7)
devtools_controls_scroll_bar = Scroll_Bar(1)
audio_settings_scroll_bar = Scroll_Bar(37)

#set sliders
scroll_sense = Slider(200, 20, 8, scroll_sense_ratio, 2)

#main game loop
run = True
while run == True:
    if game_state == 1 or game_state == 0 or game_state == -1 or game_state == 2 or game_state == 3 or game_state == 6 or game_state == 7 or game_state == 8:
        true_scroll[0] += (player.rect.x - true_scroll[0] + (tile_size // 2) - 300) / 5
        true_scroll[1] += (player.rect.y - true_scroll[1] - (tile_size) - 300) / 5
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        
        #load chunks
        grass_rects = []
        water_rects = []
        drop_map = []
        chunk_border_rects = []
        for y in range(7):
            for x in range(7):
                target_x = x - 1 + int(round(scroll[0] / (chunk_size * 16)))
                target_y = y - 1 + int(round(scroll[1] / (chunk_size * 16))) 
                target_chunk = str(target_x) + ':' + str(target_y)
                if target_chunk not in game_map: #check if chunk exists
                    game_map[target_chunk] = generate_chunks(target_x, target_y, world_seed)
                for tile in game_map[target_chunk]:
                    if chunk_borders_debug == True:
                        if game_map[target_chunk].index(tile) == 0:
                            border_topx = tile[0][0] * 16 - scroll[0]
                            border_topy = tile[0][1] * 16 - scroll[1]
                        if game_map[target_chunk].index(tile) == 0:
                            border_bottomx = tile[0][0] * 16 -scroll[0]
                            border_bottomy = tile[0][1] * 16 -scroll[1]
                    screen.blit(tile_index[tile[1]], (tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                    if tile[1] in [1]:
                        grass_rects.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],16,16), target_chunk, tile])
                        drop_map.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],16,16), target_chunk, tile])
                    if tile[1] in [2]:
                        water_rects.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],16,16), target_chunk, tile])
                        drop_map.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],16,16), target_chunk, tile])
                if chunk_borders_debug == True:
                    chunk_border_rects.append(pygame.Rect(border_topx, border_topy, abs(border_topx - border_bottomx), abs(border_topy - border_bottomy)))
        #load chunks interactable
        tree_rects = []
        rock_rects = []
        item_rects = []
        for y in range(7):
            for x in range(7):
                target_x = x - 1 + int(round(scroll[0] / (chunk_size * 16)))
                target_y = y - 1 + int(round(scroll[1] / (chunk_size * 16))) 
                target_chunk = str(target_x) + ':' + str(target_y)
                if target_chunk not in game_map_interactables: #check if chunk exists
                    game_map_interactables[target_chunk] = generate_chunks_interactables(target_x, target_y, world_seed, game_map)
                for tile in game_map_interactables[target_chunk]:
                    if tile[1] != 0:
                        screen.blit(tile_index_interactables[tile[1]], (tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1]))
                    if tile[1] in [1]:
                        tree_rects.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],tile_index_interactables[tile[1]].get_width(),tile_index_interactables[tile[1]].get_height()), tile, target_chunk])
                    if tile[1] in [2]:
                        rock_rects.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],tile_index_interactables[tile[1]].get_width(),tile_index_interactables[tile[1]].get_height()), tile, target_chunk])
                    if tile[1] in [3, 4, 5, 6, 7, 8, 9, 10]:
                        item_rects.append([pygame.Rect(tile[0][0]*16-scroll[0],tile[0][1]*16-scroll[1],tile_index_interactables[tile[1]].get_width(),tile_index_interactables[tile[1]].get_height()), tile, target_chunk])
        if debug == True:
            for tile in tree_rects:
                pygame.draw.rect(screen, (255, 255, 255), tile[0], 2)
            for tile in rock_rects:
                pygame.draw.rect(screen, (255, 255, 255), tile[0], 2)
            for tile in item_rects:
                pygame.draw.rect(screen, (255, 255, 255), tile[0], 2)
        if debug_menu == True and game_state == 0:
            debug_menu_show(target_chunk)
         

    #event handler
    for event in pygame.event.get():
        handle_music(event, playlist, music)
        if event.type == pygame.QUIT:
            run = False #if press x, end game loop
        if event.type == pygame.KEYDOWN:
            if game_state == 0:
                if event.key == pygame.K_e: 
                    game_state = 1
                elif event.key == pygame.K_ESCAPE:
                    game_state = 2
                if event.key == pygame.K_f:
                    debug = not debug
                if event.key == pygame.K_LSHIFT:
                    debug_menu = not debug_menu
                if event.key == pygame.K_c:
                    chunk_borders_debug = not chunk_borders_debug
            elif game_state == 1:
                if event.key == pygame.K_e:
                    game_state = 0
                elif event.key == pygame.K_ESCAPE:
                    game_state = 2
            elif game_state == 2:
                if event.key == pygame.K_ESCAPE:
                    game_state = 0
        if game_state == 0:
            player.get_event(event)
        elif game_state == 3:
            world_name_input.handle_event(event)
            seed_input.handle_event(event)
        elif game_state == 8:
            world_name_change.handle_event(event)
        elif game_state == 9:
            if settings_state == 1:
                if devtools_keybinds == False:
                    controls_scroll_bar.get_scroll_wheel(event)
                else:
                    devtools_controls_scroll_bar.get_scroll_wheel(event)
                scroll_sense.get_clicked(event)
                devtools_code.handle_event(event)
            elif settings_state == 2:
                audio_settings_scroll_bar.get_scroll_wheel(event)
        elif game_state == 10:
            if ingame_settings_state == 1:
                world_name_change_ingame.handle_event(event)
    #print player stuff
    if game_state == 0:
        for entity in entities:
            entity[1].update()
        for projectile in projectiles:
            projectile[1].update()
        if player.dead == True:
            game_state = -1
        player.update()
        hotbar.update()
        player.use_item(hotbar.hotbar_slots, hotbar.selector_slot)
        player.armour()
        player.health()
        spawn_entities()
        if coords_on == True:
            draw_text(str(scroll), font, white, 10, 10)
        if save_timer == 1000:
            save_world(world_num, game_map, game_map_interactables, inventory.slots, inventory.armour_slots, inventory.hotbar_slots, player.hearts['health_count'], true_scroll, player.rect.x, player.rect.y, player.direction)
            save_timer = 0
        else:
            save_timer += 1
    elif game_state == 1:
        screen.blit(inventory_bg, (0,0))
        inventory.update()
        crafting.update()
        selector.update()
    elif game_state == -1:
        screen.blit(respawn_bg, (0,0))
        if respawn_button.draw(0):
            player.respawn()
            game_state = 0
        if save_and_quit_button_dead.draw(0):
            save_world(world_num, game_map, game_map_interactables, inventory.slots, inventory.armour_slots, inventory.hotbar_slots, player.hearts['health_count'], true_scroll, player.rect.x, player.rect.y, player.direction)
            world_seed = 0
            game_map = {}
            game_map_interactables = {}
            true_scroll = [0, 0]
            player.rect.x = 293
            player.rect.y = 315
            game_state = 7
    elif game_state == 2:
        screen.blit(inventory_bg, (0,0))
        if save_and_quit_button.draw(0):
            save_world(world_num, game_map, game_map_interactables, inventory.slots, inventory.armour_slots, inventory.hotbar_slots, player.hearts['health_count'], true_scroll, player.rect.x, player.rect.y, player.direction)
            world_seed = 0
            game_map = {}
            game_map_interactables = {}
            true_scroll = [0, 0]
            player.rect.x = 293
            player.rect.y = 315
            game_state = 7
        if back_to_game.draw(0):
            game_state = 0
        if ingame_settings_button.draw(0):
            world_name_change_ingame.text = world_names[world_num]
            world_name_settings_ingame = world_names[world_num]
            settings_difficulty_ingame = world_difficulties[world_num]
            game_state = 10
    elif game_state == 3:
        if select_back_button.draw(0):
            game_state = 7
        world_name_generating = world_name_input.update(0)
        world_name_input.draw(screen)
        draw_text('World Name:', font, white, 210, 140)
        seed_generating = seed_input.update(0)
        seed_input.draw(screen)
        draw_text('Seed:', font, white, 210, 210)
        if creation_difficulty == 0:
            screen.blit(button_selected, peaceful_button.rect)
            screen.blit(peaceful_button.txt_surface, (peaceful_button.rect.centerx - (peaceful_button.text_width / 2), peaceful_button.rect.centery - 15))
            if hostile_button.draw(0):
                hostile_button.reset_rect()
                creation_difficulty = 1
        elif creation_difficulty == 1:
            screen.blit(button_selected, hostile_button.rect)
            screen.blit(hostile_button.txt_surface, (hostile_button.rect.centerx - (hostile_button.text_width / 2), hostile_button.rect.centery - 15))
            if peaceful_button.draw(0):
                peaceful_button.reset_rect()
                creation_difficulty = 0
        if generate_world_button.draw(0):
            generating_world = True
            world_name_input.text = ''
            seed_input.text = ''
            game_state = 4
    elif game_state == 4:
        if len(seed_generating) == 0:
            seed_generating = random.randint(-100000,1000000)
        generate_world(world_num, world_name_generating, seed_generating, creation_difficulty)
        temp_armour = {}
        for num in range(1, 5):
            temp_armour[f'slot_{num}'] = [0, 0, 0, 0]
        temp_inventory = {}
        for num in range(1, 26):
            temp_inventory[f'slot_{num}'] = [0, 0, 0, 0]
        temp_hotbar = {}
        for num in range(1, 6):
            temp_hotbar[f'slot_{num}'] = [0, 0, 0, 0]
        save_world(world_num, {}, {}, temp_inventory, temp_armour, temp_hotbar, 20, [0,0], 293, 315, 2)
        game_state = 5
    elif game_state == 5:
        entities = []
        game_map_interactables = {}
        game_map_interactables = load_world(world_num)
        game_state = 0
    elif game_state == 6:
        #print title screen
        screen.blit(logo, logo_rect)
        draw_text('Food Wars V1.0', font, white, 5, 570)
        if play_button.draw(0):
            game_state = 7
        if settings_button.draw(0):
            game_state = 9
        if quit_button.draw(0):
            run = False
    elif game_state == 7:
        world_num = select_world.update()
        if select_back_button.draw(0):
            game_state = 6
        if world_num != 0 and world_generated[world_num] == True:
            if play_selected_button.draw(0):
                game_state = 5
        else:
            screen.blit(button_selected, play_selected_button.rect)
            draw_text(play_selected_button.text, font, white, (play_selected_button.rect.centerx - (play_selected_button.text_width / 2)), play_selected_button.rect.centery - 15)

        if world_num != 0 and world_generated[world_num] == False:
            if create_button.draw(0):
               game_state = 3
        else:
            screen.blit(button_selected, create_button.rect)
            draw_text(create_button.text, font, white, (create_button.rect.centerx - (create_button.text_width / 2)), create_button.rect.centery - 15)
        if world_one_settings.draw(0):
            if world_generated[1] == True:
                world_num = 1
                game_state = 8
                world_name_change.text = world_names[world_num]
                settings_difficulty = world_difficulties[world_num]
        if world_two_settings.draw(0):
            if world_generated[2] == True:
                world_num = 2
                game_state = 8
                world_name_change.text = world_names[world_num]
                settings_difficulty = world_difficulties[world_num]
        if world_three_settings.draw(0):
            if world_generated[3] == True:
                world_num = 3
                game_state = 8
                world_name_change.text = world_names[world_num]
                settings_difficulty = world_difficulties[world_num]
        if world_four_settings.draw(0):
            if world_generated[4] == True:
                world_num = 4
                game_state = 8
                world_name_change.text = world_names[world_num]
                settings_difficulty = world_difficulties[world_num]
        if world_generated[1] == True:
            draw_text(world_names[1], font, white, select_world.world_1_rect.x + 70, select_world.world_1_rect.y)
            if world_difficulties[1] == 0: 
                draw_text('Peaceful', font_difficulty, white, select_world.world_1_rect.x + 70, select_world.world_1_rect.y + 35)
            if world_difficulties[1] == 1: 
                draw_text('Hostile', font_difficulty, white, select_world.world_1_rect.x + 70, select_world.world_1_rect.y + 35)
        else:
            draw_text('World 1', font, white, select_world.world_1_rect.x + 70, select_world.world_1_rect.y)
        if world_generated[2] == True:
            draw_text(world_names[2], font, white, select_world.world_2_rect.x + 70, select_world.world_2_rect.y)
            if world_difficulties[2] == 0: 
                draw_text('Peaceful', font_difficulty, white, select_world.world_2_rect.x + 70, select_world.world_2_rect.y + 35)
            if world_difficulties[2] == 1: 
                draw_text('Hostile', font_difficulty, white, select_world.world_2_rect.x + 70, select_world.world_2_rect.y + 35)
        else:
            draw_text('World 2', font, white, select_world.world_2_rect.x + 70, select_world.world_2_rect.y)
        if world_generated[3] == True:
            draw_text(world_names[3], font, white, select_world.world_3_rect.x + 70, select_world.world_3_rect.y)
            if world_difficulties[3] == 0: 
                draw_text('Peaceful', font_difficulty, white, select_world.world_3_rect.x + 70, select_world.world_3_rect.y + 35)
            if world_difficulties[3] == 1: 
                draw_text('Hostile', font_difficulty, white, select_world.world_3_rect.x + 70, select_world.world_3_rect.y + 35)
        else:
            draw_text('World 3', font, white, select_world.world_3_rect.x + 70, select_world.world_3_rect.y)
        if world_generated[4] == True:
            draw_text(world_names[4], font, white, select_world.world_4_rect.x + 70, select_world.world_4_rect.y)
            if world_difficulties[4] == 0: 
                draw_text('Peaceful', font_difficulty, white, select_world.world_4_rect.x + 70, select_world.world_4_rect.y + 35)
            if world_difficulties[4] == 1: 
                draw_text('Hostile', font_difficulty, white, select_world.world_4_rect.x + 70, select_world.world_4_rect.y + 35)
        else:
           draw_text('World 4', font, white, select_world.world_4_rect.x + 70, select_world.world_4_rect.y)     
    elif game_state == 8:
        if delete_state == 0:
            draw_text('Seed: '+ str(world_seeds[world_num]), font, white, 200, 250)     
            world_name_settings = world_name_change.update(0)
            world_name_change.draw(screen)
            draw_text('World Name:', font, white, 235, 150)     
            if settings_difficulty == 0:
                screen.blit(button_selected, peaceful_button.rect)
                draw_text(peaceful_button.text, font, white, (peaceful_button.rect.centerx - (peaceful_button.text_width / 2)), peaceful_button.rect.centery - 15)
                if hostile_button.draw(0):
                    hostile_button.reset_rect()
                    settings_difficulty = 1
            elif settings_difficulty == 1:
                screen.blit(button_selected, hostile_button.rect)
                draw_text(hostile_button.text, font, white, (hostile_button.rect.centerx - (hostile_button.text_width / 2)), hostile_button.rect.centery - 15)
                if peaceful_button.draw(0):
                    peaceful_button.reset_rect()
                    settings_difficulty = 0
            if select_back_button.draw(0):
                world_names[world_num] = world_name_settings
                world_difficulties[world_num] = settings_difficulty
                with open(f'game_files/world_data/world_{world_num}/name/world_name.json', "w") as file:
                    json.dump(world_name_settings, file)
                with open(f'game_files/world_data/world_{world_num}/difficulty/difficulty.json', "w") as file:
                    json.dump(settings_difficulty, file)
                game_state = 7
            if delete_world_button.draw(0):
                delete_state = 1
        elif delete_state == 1:
            draw_text("Are you sure you want to delete?", font, white, 130, 200)
            if delete_yes_button.draw(0):
                delete_state = 0
                world_generated[world_num] = False
                with open(f'game_files/world_data/world_{world_num}/generated/generated.json', "w") as file:
                    json.dump(False, file)
                    game_state = 7
            if delete_no_button.draw(0):
                delete_state = 0
    elif game_state == 9:
        #audio, video, keybinds,
        screen.blit(settings_bg, (0, 0))
        if back_settings_button.draw(0):
            settings = [sfx, music, scroll_sense.ratio, coords_on]
            with open('game_files/settings/settings.json', "w") as file:
                json.dump(settings, file)
            game_state = 6
        if settings_state != 2:
            if audio_settings_button.draw(0):
                settings_state = 2
        else:
            screen.blit(button_settings_selected, (audio_settings_button.rect.x, audio_settings_button.rect.y))
            screen.blit(audio_settings_button.txt_surface, (audio_settings_button.rect.centerx - (audio_settings_button.text_width / 2), audio_settings_button.rect.centery - 15))
            audio_scroll = audio_settings_scroll_bar.update()
            draw_text('Sound Effects', font, white, 200, 85 - audio_scroll)
            draw_text('Music', font, white, 200, 185 - audio_scroll)
            if sfx == True:
                if sfx_on_button.draw(audio_scroll):
                    sfx = False
            else:
                if sfx_off_button.draw(audio_scroll):
                    sfx = True
            if music == True:
                if music_on_button.draw(audio_scroll):
                    music = False
            else:
                if music_off_button.draw(audio_scroll):
                    music = True
        if settings_state != 1:
            if controls_button.draw(0):
                settings_state = 1
        else:
             screen.blit(button_settings_selected, (controls_button.rect.x, controls_button.rect.y))
             screen.blit(controls_button.txt_surface, (controls_button.rect.centerx - (controls_button.text_width / 2), controls_button.rect.centery - 15))
             if devtools_keybinds == False:
                 controls_scroll = controls_scroll_bar.update()
             else:
                 controls_scroll = 1.1 * devtools_controls_scroll_bar.update()
             scroll_sensitivity = scroll_sense.update(controls_scroll)
             draw_text('Walk Forward', font, white, 200, 100 - controls_scroll)
             draw_text('Scroll Sensitivity', font, white, 200, 5 - controls_scroll)
             screen.blit(keybinds_display, (160, 80 - controls_scroll))
             screen.blit(keybinds_display, (160, 144 - controls_scroll))
             screen.blit(keybinds_display, (160, 208 - controls_scroll))
             screen.blit(keybinds_display, (160, 272 - controls_scroll))
             screen.blit(keybinds_display, (160, 336 - controls_scroll))
             screen.blit(keybinds_display, (160, 400 - controls_scroll))
             screen.blit(keybinds_display, (160, 464 - controls_scroll))
             screen.blit(keybinds_display, (160, 528 - controls_scroll))             
             screen.blit(keybinds_display, (160, 592 - controls_scroll))             
             screen.blit(keybinds_display, (160, 656 - controls_scroll))             
             screen.blit(keybinds_display, (160, 720 - controls_scroll))            
             screen.blit(keybinds_display, (160, 784 - controls_scroll))
             screen.blit(keybinds_display, (160, 848 - controls_scroll)) 
             screen.blit(keybinds_display, (160, 912 - controls_scroll))             
             screen.blit(keybinds_display, (160, 976 - controls_scroll))           
             screen.blit(keybinds_display, (160, 1090 - controls_scroll))             
             screen.blit(keybinds_display, (160, 1154 - controls_scroll))           
             draw_text('Walk Forward', font, white, 200, 100 - controls_scroll)
             draw_text('W', font, white, 515, 100 - controls_scroll)
             draw_text('Walk Left', font, white, 200, 164 - controls_scroll)
             draw_text('A', font, white, 515, 164 - controls_scroll)
             draw_text('Walk Backwards', font, white, 200, 228 - controls_scroll)
             draw_text('S', font, white, 515, 228 - controls_scroll)
             draw_text('Walk Right', font, white, 200, 292 - controls_scroll)
             draw_text('D', font, white, 515, 292 - controls_scroll)
             draw_text('Run', font, white, 200, 356 - controls_scroll)
             draw_text('R', font, white, 515, 356 - controls_scroll)            
             draw_text('Break Block', font, white, 200, 420 - controls_scroll)
             draw_text('Q', font, white, 515, 420 - controls_scroll)
             draw_text('Open Inventory', font, white, 200, 484 - controls_scroll)
             draw_text('E', font, white, 515, 484 - controls_scroll)
             draw_text('Pause Game', font, white, 200, 548 - controls_scroll)
             draw_text('ESC', font, white, 505, 548 - controls_scroll)
             draw_text('Hotbar Slot 1', font, white, 200, 612 - controls_scroll)
             draw_text('1', font, white, 515, 612 - controls_scroll)
             draw_text('Hotbar Slot 2', font, white, 200, 676 - controls_scroll)
             draw_text('2', font, white, 515, 676 - controls_scroll)
             draw_text('Hotbar Slot 3', font, white, 200, 740 - controls_scroll)
             draw_text('3', font, white, 515, 740 - controls_scroll)
             draw_text('Hotbar Slot 4', font, white, 200, 804 - controls_scroll)
             draw_text('4', font, white, 515, 804 - controls_scroll)
             draw_text('Hotbar Slot 5', font, white, 200, 868 - controls_scroll)
             draw_text('5', font, white, 515, 868 - controls_scroll)
             draw_text('Take 1 From Stack', font, white, 200, 932 - controls_scroll)
             draw_text('Shift', font, white, 500, 932 - controls_scroll)
             draw_text('Delete Item', font, white, 200, 996 - controls_scroll)
             draw_text('DEL', font, white, 505, 996 - controls_scroll)
             draw_text('Debug Menu', font, white, 200, 1110 - controls_scroll)
             draw_text('SHIFT', font, white, 500, 1110 - controls_scroll)
             draw_text('Hitboxes', font, white, 200, 1174 - controls_scroll)
             draw_text('F', font, white, 515, 1174 - controls_scroll)
             devtools_code.update(controls_scroll)
             devtools_code.draw(screen)
             test = str(devtools_code.text) == 'FZ673TW'
             if test:
                 devtools_keybinds = True
             else:
                 devtools_keybinds = False
             
        if settings_state != 4:
            if graphics_settings_button.draw(0):
                settings_state = 4
        else:
            screen.blit(button_settings_selected, (graphics_settings_button.rect.x, graphics_settings_button.rect.y))
            screen.blit(graphics_settings_button.txt_surface, (graphics_settings_button.rect.centerx - (graphics_settings_button.text_width / 2), graphics_settings_button.rect.centery - 15))
            draw_text('Show Coordinates', font, white, 170, 85)
            if coords_on == True:
                if coords_on_button.draw(0):
                    coords_on = False
            elif coords_on == False:
                if coords_off_button.draw(0):
                    coords_on = True
        if settings_state != 5:
            if credits_settings_button.draw(0):
                settings_state = 5
        else:
            screen.blit(button_settings_selected, (credits_settings_button.rect.x, credits_settings_button.rect.y))
            screen.blit(credits_settings_button.txt_surface, (credits_settings_button.rect.centerx - (credits_settings_button.text_width / 2), credits_settings_button.rect.centery - 15))
            draw_text('Font:', font, white, 140, 5)
            draw_text('Find lisence text at', font, white, 140, 25)
            draw_text('game_files/fonts/medieval', font, white, 140, 45)
            draw_text('-sharp-font/info.txt', font, white, 140, 65)
    elif game_state == 10:
        #audio, video, keybinds,
        screen.blit(settings_bg, (0, 0))
        if back_settings_button_ingame.draw(0):
            world_names[world_num] = world_name_settings_ingame
            world_difficulties[world_num] = settings_difficulty_ingame
            with open(f'game_files/world_data/world_{world_num}/name/world_name.json', "w") as file:
                json.dump(world_name_settings_ingame, file)
            with open(f'game_files/world_data/world_{world_num}/difficulty/difficulty.json', "w") as file:
                json.dump(settings_difficulty_ingame, file)
            settings = [sfx, music, scroll_sense.ratio, coords_on]
            with open('game_files/settings/settings.json', "w") as file:
                json.dump(settings, file)
            game_state = 0
        if ingame_settings_state != 3:
            if audio_settings_button_ingame.draw(0):
                ingame_settings_state = 3
        else:
            screen.blit(button_settings_selected, (audio_settings_button_ingame.rect.x, audio_settings_button_ingame.rect.y))
            screen.blit(audio_settings_button_ingame.txt_surface, (audio_settings_button_ingame.rect.centerx - (audio_settings_button_ingame.text_width / 2), audio_settings_button_ingame.rect.centery - 15))
            audio_scroll = audio_settings_scroll_bar.update()
            draw_text('Sound Effects', font, white, 200, 185 - audio_scroll)
            draw_text('Music', font, white, 200, 85 - audio_scroll)
            if sfx == True:
                if sfx_on_button.draw(audio_scroll):
                    sfx = False
            else:
                if sfx_off_button.draw(audio_scroll):
                    sfx = True
            if music == True:
                if music_on_button.draw(audio_scroll):
                    music = False
            else:
                if music_off_button.draw(audio_scroll):
                    music = True
        if ingame_settings_state != 2:
            if controls_button_ingame.draw(0):
                ingame_settings_state = 2
        else:
             screen.blit(button_settings_selected, (controls_button_ingame.rect.x, controls_button_ingame.rect.y))
             screen.blit(controls_button_ingame.txt_surface, (controls_button_ingame.rect.centerx - (controls_button_ingame.text_width / 2), controls_button_ingame.rect.centery - 15))
             controls_scroll = controls_scroll_bar.update()
             scroll_sensitivity = scroll_sense.update(controls_scroll)
             draw_text('Scroll Sensitivity', font, white, 200, 5 - controls_scroll)
             screen.blit(keybinds_display, (160, 80 - controls_scroll))
             screen.blit(keybinds_display, (160, 144 - controls_scroll))
             screen.blit(keybinds_display, (160, 208 - controls_scroll))
             screen.blit(keybinds_display, (160, 272 - controls_scroll))
             screen.blit(keybinds_display, (160, 336 - controls_scroll))
             screen.blit(keybinds_display, (160, 400 - controls_scroll))
             screen.blit(keybinds_display, (160, 464 - controls_scroll))
             screen.blit(keybinds_display, (160, 528 - controls_scroll))             
             screen.blit(keybinds_display, (160, 592 - controls_scroll))             
             screen.blit(keybinds_display, (160, 656 - controls_scroll))             
             screen.blit(keybinds_display, (160, 720 - controls_scroll))            
             screen.blit(keybinds_display, (160, 784 - controls_scroll))
             screen.blit(keybinds_display, (160, 848 - controls_scroll)) 
             screen.blit(keybinds_display, (160, 912 - controls_scroll))             
             screen.blit(keybinds_display, (160, 976 - controls_scroll))           
             draw_text('Walk Forward', font, white, 200, 100 - controls_scroll)
             draw_text('W', font, white, 515, 100 - controls_scroll)
             draw_text('Walk Left', font, white, 200, 164 - controls_scroll)
             draw_text('A', font, white, 515, 164 - controls_scroll)
             draw_text('Walk Backwards', font, white, 200, 228 - controls_scroll)
             draw_text('S', font, white, 515, 228 - controls_scroll)
             draw_text('Walk Right', font, white, 200, 292 - controls_scroll)
             draw_text('D', font, white, 515, 292 - controls_scroll)
             draw_text('Run', font, white, 200, 356 - controls_scroll)
             draw_text('R', font, white, 515, 356 - controls_scroll)            
             draw_text('Break Block', font, white, 200, 420 - controls_scroll)
             draw_text('Q', font, white, 515, 420 - controls_scroll)
             draw_text('Open Inventory', font, white, 200, 484 - controls_scroll)
             draw_text('E', font, white, 515, 484 - controls_scroll)
             draw_text('Pause Game', font, white, 200, 548 - controls_scroll)
             draw_text('ESC', font, white, 505, 548 - controls_scroll)
             draw_text('Hotbar Slot 1', font, white, 200, 612 - controls_scroll)
             draw_text('1', font, white, 515, 612 - controls_scroll)
             draw_text('Hotbar Slot 2', font, white, 200, 676 - controls_scroll)
             draw_text('2', font, white, 515, 676 - controls_scroll)
             draw_text('Hotbar Slot 3', font, white, 200, 740 - controls_scroll)
             draw_text('3', font, white, 515, 740 - controls_scroll)
             draw_text('Hotbar Slot 4', font, white, 200, 804 - controls_scroll)
             draw_text('4', font, white, 515, 804 - controls_scroll)
             draw_text('Hotbar Slot 5', font, white, 200, 868 - controls_scroll)
             draw_text('5', font, white, 515, 868 - controls_scroll)
             draw_text('Take 1 From Stack', font, white, 200, 932 - controls_scroll)
             draw_text('Shift', font, white, 500, 932 - controls_scroll)
             draw_text('Delete Item', font, white, 200, 996 - controls_scroll)
             draw_text('DEL', font, white, 505, 996 - controls_scroll)

        if ingame_settings_state != 1:
            if world_settings_ingame.draw(0):
                ingame_settings_state = 1
        else:
            screen.blit(button_settings_selected, (world_settings_ingame.rect.x, world_settings_ingame.rect.y))
            screen.blit(world_settings_ingame.txt_surface, (world_settings_ingame.rect.centerx - (world_settings_ingame.text_width / 2), world_settings_ingame.rect.centery - 15))
            draw_text('Seed: '+ str(world_seeds[world_num]), font, white, 290, 100)     
            world_name_settings_ingame = world_name_change_ingame.update(0)
            world_name_change_ingame.draw(screen)
            draw_text('World Name:', font, white, 260, 20)     
            if settings_difficulty_ingame == 0:
                screen.blit(button_selected, peaceful_button_ingame.rect)
                draw_text(peaceful_button_ingame.text, font, white, (peaceful_button_ingame.rect.centerx - (peaceful_button_ingame.text_width / 2)), peaceful_button_ingame.rect.centery - 15)
                if hostile_button_ingame.draw(0):
                    hostile_button_ingame.reset_rect()
                    settings_difficulty_ingame = 1
            elif settings_difficulty_ingame == 1:
                screen.blit(button_selected, hostile_button_ingame.rect)
                draw_text(hostile_button_ingame.text, font, white, (hostile_button_ingame.rect.centerx - (hostile_button_ingame.text_width / 2)), hostile_button_ingame.rect.centery - 15)
                if peaceful_button_ingame.draw(0):
                    peaceful_button_ingame.reset_rect()
                    settings_difficulty_ingame = 0
        if ingame_settings_state != 4:
            if graphics_settings_button_ingame.draw(0):
                ingame_settings_state = 4
        else:
            screen.blit(button_settings_selected, (graphics_settings_button_ingame.rect.x, graphics_settings_button_ingame.rect.y))
            screen.blit(graphics_settings_button_ingame.txt_surface, (graphics_settings_button_ingame.rect.centerx - (graphics_settings_button_ingame.text_width / 2), graphics_settings_button_ingame.rect.centery - 15))
            draw_text('Show Coordinates', font, white, 170, 85)
            if coords_on == True:
                if coords_on_button.draw(0):
                    coords_on = False
            elif coords_on == False:
                if coords_off_button.draw(0):
                    coords_on = True

            
    clock.tick(fps)
    #refresh the screen
    pygame.display.update()    
pygame.quit()