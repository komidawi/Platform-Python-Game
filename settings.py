# -*- coding: utf-8 -*-

# COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# GAME SETTINGS
WIDTH = 800
HEIGHT = 640
FPS = 60
TITLE = "COIN COLLECTOR"
BG_IMAGE = 'background.jpg'
TILESIZE = 32

# MUSIC
BG_MUSIC = 'bg_music.mp3'

# SOUNDS
SOUND_EFFECTS = {'coin_gathered': 'coin_gathered.wav',
                 'jump': 'jump.wav',
                 'lvl_complete': 'lvl_complete.wav'}

# HUD SETTINGS
HUD_DIGITS = ['hud_0.png', 'hud_1.png', 'hud_2.png', 'hud_3.png', 'hud_4.png', 
              'hud_5.png', 'hud_6.png', 'hud_7.png', 'hud_8.png', 'hud_9.png']
HUD_X = 'hud_x.png'
HUD_IMAGES = {'hud_coin_gold': 'hud_coins.png'}

# PLAYER SETTINGS
PLAYER_SPEED = 5
PLAYER_ACC = 0.7
PLAYER_FRICTION = -0.12
PLAYER_GRAV = 0.76
PLAYER_IMG = 'player.png' 

# ITEMS
ITEM_IMAGES = {'coin_gold': 'coinGold.png',
               'weight': 'weightChained.png'}
BOB_RANGE = 15
BOB_SPEED = 0.38

# MAPS
MAP_LIST = ['map1.tmx', 'map2.tmx', 'map3.tmx']

# LAYERS
WALL_LAYER = 1
PLAYER_LAYER = 2
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1