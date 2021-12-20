import pygame as pg
import sys
import math
from random import choice, random
from os import path
from settings import *
from sprites import *
from tilemap import *

# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = WIDTH
    BAR_HEIGHT = 10
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if pct > 0.66:
        col = GREEN
    elif pct > 0.33:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, BLACK, outline_rect, 2)

class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 4, 2048) #音樂
        pg.init()#初始化(節約資源用)
        self.screen = pg.display.set_mode((WIDTH, HEIGHT)) #螢幕大小
        pg.display.set_caption(TITLE) #視窗名
        self.clock = pg.time.Clock() #FPS
        self.load_data() #觸發load_data

    def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
        font = pg.font.SysFont(font_name,size,False,False)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(**{align: (x, y)})
        self.screen.blit(text_surface, text_rect)
 
    """""""""""
    這裡是主程式
    """""""""""

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.player = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.water = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.mob_bullets = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        #for row, tiles in enumerate(self.map.data):
        #    for col, tile in enumerate(tiles):
        #        if tile == '1':
        #            Wall(self, col, row) #1=Wall
        #        if tile == 'M':
        #            Mob(self, col, row) #M=敵人
        #        if tile == 'P':
        #            self.player = Player(self, col, row) #=玩家起始點
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_object.name == 'enemy':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name == 'water':
                Aqua(self, tile_object.x, tile_object.y,
                         tile_object.width, tile_object.height)
            if tile_object.name in ['health','fire','hand','spear','arrow','slash','rock']:
                Item(self, obj_center, tile_object.name)
        self.camera = Camera(self.map.width, self.map.height) #tilemap => Camera
        self.draw_debug = False
        self.paused = False

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000.0
            self.events() #觸發event
            if not self.paused:
                self.update() #觸發各自的update
            self.draw() #觸發draw

    """""""""""
    這裡是主程式
    """""""""""
    def load_data(self): #圖片導入
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        map_folder = path.join(game_folder, 'map_thing')
        music_folder = path.join(game_folder, 'music')
        self.map = TiledMap(path.join(map_folder, 'map01.tmx'))
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))
        self.player_imgs = {'hand':pg.image.load(path.join(img_folder, PLAYER_IMG['hand']['player_img'] )).convert_alpha(),
                              'fire':pg.image.load(path.join(img_folder, PLAYER_IMG['fire']['player_img'] )).convert_alpha(),
                              'spear':pg.image.load(path.join(img_folder, PLAYER_IMG['spear']['player_img'] )).convert_alpha(),
                              'arrow':pg.image.load(path.join(img_folder, PLAYER_IMG['arrow']['player_img'] )).convert_alpha(),
                              'slash':pg.image.load(path.join(img_folder, PLAYER_IMG['slash']['player_img'] )).convert_alpha(),
                              'rock':pg.image.load(path.join(img_folder, PLAYER_IMG['rock']['player_img'] )).convert_alpha()} 
        self.bullet_images = {'hand':pg.image.load(path.join(img_folder, WEAPONS['hand']['bullet_img'] )).convert_alpha(),
                              'fire':pg.image.load(path.join(img_folder, WEAPONS['fire']['bullet_img'] )).convert_alpha(),
                              'spear':pg.image.load(path.join(img_folder, WEAPONS['spear']['bullet_img'] )).convert_alpha(),
                              'arrow':pg.image.load(path.join(img_folder, WEAPONS['arrow']['bullet_img'] )).convert_alpha(),
                              'slash':pg.image.load(path.join(img_folder, WEAPONS['slash']['bullet_img'] )).convert_alpha(),
                              'rock':pg.image.load(path.join(img_folder, WEAPONS['rock']['bullet_img'] )).convert_alpha()} 
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha() #敵人圖片
        self.mob_bullet_img = pg.image.load(path.join(img_folder, MOB_BULLET_IMG)).convert_alpha() #敵人武器
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha() #敵人屍體
        self.splat = pg.transform.scale(self.splat, (64, 64)) #敵人屍體大小
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder, ITEM_IMAGES[item])).convert_alpha()
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def quit(self):
        pg.quit()
        sys.exit()

    def events(self):#被run觸發的event
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def update(self): #被run觸發的計算
        self.all_sprites.update() #導過去sprite.py的update
        self.camera.update(self.player)#畫面更新
        hits = pg.sprite.spritecollide(self.player, self.items, False)#撿拾物品
        for hit in hits:
            if hit.type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type == 'fire':
                hit.kill()
                self.player.weapon = 'fire'
            if hit.type == 'spear':
                hit.kill()
                self.player.weapon = 'spear'
            if hit.type == 'arrow':
                hit.kill()
                self.player.weapon = 'arrow'
            if hit.type == 'rock':
                hit.kill()
                self.player.weapon = 'rock'
            if hit.type == 'slash':
                hit.kill()
                self.player.weapon = 'slash'

        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect) #玩家對敵人碰撞
        if hits:
            for hit in hits:
                self.player.health -= MOB_DAMAGE #碰撞傷害
                hit.vel = vec(0, 0)
                if self.player.health <= 0:
                    self.playing = False
            self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot) #擊退.方向
        
        hits = pg.sprite.spritecollide(self.player, self.mob_bullets, True, collide_hit_rect) #玩家對火焰碰撞
        if hits:
            for hit in hits:
                self.player.health -= MOB_BULLET_DAMAGE #武器傷害
                hit.vel = vec(0, 0)
                if self.player.health <= 0:
                    self.playing = False
            self.player.pos += vec(MOB_BULLET_KNOCKBACK, 0).rotate(-hits[0].rot) #擊退.方向
        
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)#(敵人，武器，敵人扣血，武器消失)
        for hit in hits:
            hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            hit.vel = vec(0, 0)
        
    def draw(self):#被run觸發的draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)#畫面底色
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        if self.draw_debug:
            for aqua in self.water:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(aqua.rect), 1)
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        # HUD functions
        draw_player_health(self.screen, 0, HEIGHT-10 , self.player.health / PLAYER_HEALTH)
        self.draw_text('Enemy: {}'.format(len(self.mobs)), "comicsans", 30, WHITE, WIDTH - 10, 10, align="topright")
        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", "comicsans" , 50 , WHITE, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

g = Game()
g.show_start_screen()

"""""""""
觸發主程式的迴圈
"""""""""

while True:
    g.new()
    g.run()
    g.show_go_screen()

"""""""""
觸發主程式的迴圈
"""""""""