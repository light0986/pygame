import pygame as pg
vec = pg.math.Vector2

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106, 55, 5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 769   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 769  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = WHITE

TILESIZE = 64 #每個格長大小
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 150.0
#PLAYER_IMG = 'player.png'
PLAYER_HIT_RECT = pg.Rect(0, 0, 40, 55) #判定範圍
BARREL_OFFSET = vec(25, 0) #子彈射出位置修正

# player_image
PLAYER_IMG = {}
PLAYER_IMG['hand']={'player_img':'player_hit.png'}
PLAYER_IMG['spear']={'player_img':'player_spear.png'}
PLAYER_IMG['fire']={'player_img':'player_fire.png'}
PLAYER_IMG['arrow']={'player_img':'player_arrow.png'}
PLAYER_IMG['rock']={'player_img':'player_rock.png'}
PLAYER_IMG['slash']={'player_img':'player_slash.png'}

# weapons
WEAPONS = {} 
WEAPONS['hand'] = {'bullet_img': 'Hit.png' , 
                    'bullet_speed': 60, #飛行速度
                    'bullet_lifetime': 100, #存在時間
                    'rate': 600, #CD時間
                    'kickback': 10, #反作用力
                    'spread': 1, #擴散值
                    'damage': 10, #傷害                    
                    'bullet_count': 1} #子彈數量

WEAPONS['spear'] = {'bullet_img': 'spear.png',
                    'bullet_speed': 60, #飛行速度
                    'bullet_lifetime': 100, #存在時間
                    'rate': 600, #CD時間
                    'kickback': 20, #反作用力
                    'spread': 1, #擴散值
                    'damage': 30, #傷害
                    'bullet_count': 1} #子彈數量

WEAPONS['fire'] = {'bullet_img': 'Flame.png',
                    'bullet_speed': 300, #飛行速度
                    'bullet_lifetime': 600, #存在時間
                    'rate': 600, #CD時間
                    'kickback': 0, #反作用力
                    'spread': 30, #擴散值
                    'damage': 1, #傷害  
                    'bullet_count': 5} #子彈數量

WEAPONS['arrow'] = {'bullet_img': 'arrow.png',
                    'bullet_speed': 600, #飛行速度
                    'bullet_lifetime': 600, #存在時間
                    'rate': 1200, #CD時間
                    'kickback': 300, #反作用力
                    'spread': 10, #擴散值
                    'damage': 50, #傷害
                    'bullet_count': 1} #子彈數量

WEAPONS['rock'] = {'bullet_img': 'rock.png',
                    'bullet_speed': 400, #飛行速度
                    'bullet_lifetime': 500, #存在時間
                    'rate': 1200, #CD時間
                    'kickback': 300, #反作用力
                    'spread': 20, #擴散值
                    'damage': 20, #傷害
                    'bullet_count': 2} #子彈數量
                    
WEAPONS['slash'] = {'bullet_img': 'slash.png',
                    'bullet_speed': 60, #飛行速度
                    'bullet_lifetime': 100, #存在時間
                    'rate': 600, #CD時間
                    'kickback': 300, #反作用力
                    'spread': 10, #擴散值
                    'damage': 40, #傷害
                    'bullet_count': 1} #子彈數量

# Mob settings
MOB_IMG = 'Dog.png'
MOB_SPEED = [150, 100, 75, 125]
MOB_HIT_RECT = pg.Rect(0, 0, 10, 10)
MOB_HEALTH = 200
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 500 #敵視範圍

MOBS = {}
MOBS['A'] = {'mob_img':'',
             'mob_speed':'',
             'mob_hit_rect':'',
             'mob_health':'',
             'mob_damage':'',
            }
MOBS['B'] = {'mob_img':'',
             'mob_speed':'',
             'mob_hit_rect':'',
             'mob_health':'',
             'mob_damage':'',
            }

# Mob_Gun settings
MOB_BARREL_OFFSET = vec(33, 0)
MOB_BULLET_HIT_RECT = pg.Rect(0, 0, 10, 10)
MOB_BULLET_IMG = 'arrow.png'
MOB_BULLET_SPEED = 1000 #飛行速度
MOB_BULLET_LIFETIME = 1000 #維持時間
MOB_BULLET_KNOCKBACK = 20
MOB_KICKBACK = 1 #反作用力
MOB_GUN_SPREAD = 10 #擴散值
MOB_BULLET_DAMAGE = 10
MOB_SHUT_CHANCE = 1 

# Layers
ONE_LAYER = 1
TWO_LAYER = 2
THREE_LAYER = 3
FOUR_LAYER = 4
FIVE_LAYER = 5

# Items
ITEM_IMAGES = {'health': 'meat.png',
               'fire': 'Flame.png',
               'hand': 'Hit.png',
               'spear':'spear.png',
               'arrow':'arrow.png',
               'slash':'slash.png',
               'rock':'rock.png'}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

#effect
SPLAT = 'blood.png'

#sounds
BG_MUSIC = 'background.wav'