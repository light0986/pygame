import pygame as pg
import pytweening as tween
from random import *
from math import *
from settings import *
from tilemap import collide_hit_rect
import pytweening as tween
from itertools import chain
vec = pg.math.Vector2 #向量座標

def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

def collide_with_water(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):#玩家類別
    def __init__(self, game, x, y): #主宣告 
        self._layer = TWO_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.weapon = 'hand'
        self.image = game.player_imgs[self.weapon]
        self.rect = self.image.get_rect()#玩家圖片的(0,0)座標
        self.hit_rect = PLAYER_HIT_RECT #玩家觸碰面積大小
        self.hit_rect.center = self.rect.center #觸碰中心=圖片中心(座標)
        self.vel = vec(0,0) #本位座標
        self.pos = vec(x, y) #目標座標(碰撞判定用)
        self.rot = 0
        self.last_shot = 0
        self.health = PLAYER_HEALTH #玩家血量 
        #self.damaged = False

    def get_keys(self): #按鍵觸發
        self.vel = vec(0, 0) #初始本位做標判定(0,0)
        keys = pg.key.get_pressed() #按鍵事件

        if keys[pg.K_SPACE]:
            self.shoot()
                
        else:       
            if keys[pg.K_a]:
                self.vel = vec(-PLAYER_SPEED, 0).rotate(0) #玩家向左走

            if keys[pg.K_d]:
                self.vel = vec(PLAYER_SPEED, 0).rotate(0) #玩家向右走

            if keys[pg.K_w]:
                self.vel = vec(0, -PLAYER_SPEED).rotate(0) #玩家向上走

            if keys[pg.K_s]:
                self.vel = vec(0, PLAYER_SPEED).rotate(0) #玩家向下走
        
            if keys[pg.K_a] and keys[pg.K_w]:
                self.vel = vec(-PLAYER_SPEED, -PLAYER_SPEED).rotate(0) #玩家座標x增加=向前走

            if keys[pg.K_d] and keys[pg.K_w]:
                self.vel = vec(PLAYER_SPEED, -PLAYER_SPEED).rotate(0) #玩家座標x增加=向前走

            if keys[pg.K_s] and keys[pg.K_d]:
                self.vel = vec(PLAYER_SPEED, PLAYER_SPEED).rotate(0) #玩家座標x增加=向前走

            if keys[pg.K_a] and keys[pg.K_s]:
                self.vel = vec(-PLAYER_SPEED, PLAYER_SPEED).rotate(0) #玩家座標x減少=向後走      

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.weapon]['rate']:
            self.last_shot = now
            dir = vec(1, 0).rotate(-self.rot) 
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.weapon]['kickback'], 0).rotate(-self.rot)
            for i in range(WEAPONS[self.weapon]['bullet_count']):
                spread = uniform(-WEAPONS[self.weapon]['spread'], WEAPONS[self.weapon]['spread'])
                Bullet(self.game, pos, dir.rotate(spread), WEAPONS[self.weapon]['damage'])

    def get_Mouse(self):#抓取玩家位置轉角度
        rot = self.rot
        x,y = pg.mouse.get_pos() #滑鼠座標Ａ
        x1,y1 = WIDTH/2,HEIGHT/2 #圖片第一點中心座標Ｂ
        if y < HEIGHT/2:
            x2,y2 = WIDTH,HEIGHT/2 #圖片零度角座標Ｃ，求ＢＡ，ＢＣ夾角
        else:
            x2,y2 = 0,HEIGHT/2

        BAx = x1-x
        BAy = y1-y
        BCx = x1-x2
        BCy = y1-y2
        BAxBC = (BAx*BCx)+(BAy*BCy)#向量
        distance=sqrt((BAx*BAx)+(BAy*BAy))*sqrt((BCx*BCx)+(BCy*BCy))
        cosＡ = (BAxBC/distance)
        if y<HEIGHT/2:
            self.Angal = degrees(acos(cosA))
        else:
            self.Angal = degrees(acos(cosA))+180

        self.Angal = self.Angal - rot

    def update(self): #碰撞觸發計算
        self.get_keys()
        self.get_Mouse()
        self.rot = (self.rot +self.Angal) % 360
        self.image = pg.transform.rotate(self.game.player_imgs[self.weapon], self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x') #撞牆
        collide_with_water(self, self.game.water, 'x') #撞水
        self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y') #撞牆
        collide_with_water(self, self.game.water, 'y') #撞水
        self.rect.center = self.hit_rect.center
    
    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH
    
class Mob(pg.sprite.Sprite):#敵人
    def __init__(self, game, x, y):
        self._layer = TWO_LAYER
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH #敵人血量
        self.speed = choice(MOB_SPEED)
        self.target = game.player

    def avoid_mobs(self):
        for mob in self.game.mobs:
            if mob != self:
                dist = self.pos - mob.pos
                if 0 < dist.length() < AVOID_RADIUS:
                    self.acc += dist.normalize()

    def shot_chance(self):
        chance = randint(1,500)
        if chance <= MOB_SHUT_CHANCE:
            dir = vec(1, 0).rotate(-self.rot)
            pos = self.pos + MOB_BARREL_OFFSET.rotate(-self.rot) #槍口位置判定
            Mob_Bullet(self.game, pos, dir)
            self.vel = vec(-MOB_KICKBACK, 0).rotate(-self.rot)
    
    def update(self): #敵人移動判斷
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < DETECT_RADIUS**2: #視野
            self.shot_chance() 
            self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            self.avoid_mobs()
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.hit_rect.centerx = self.pos.x
            collide_with_walls(self, self.game.walls, 'x') #撞牆
            collide_with_water(self, self.game.water, 'x') #撞水
            self.hit_rect.centery = self.pos.y
            collide_with_walls(self, self.game.walls, 'y') #撞牆
            collide_with_water(self, self.game.water, 'y') #撞水
            self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            self.game.map_img.blit(self.game.splat, self.pos - vec(32, 32))
    
    def draw_health(self):
        if self.health > 66:
            col = GREEN
        elif self.health > 33:
            col = YELLOW
        else:
            col = RED
        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)

class Bullet(pg.sprite.Sprite): #子彈
    def __init__(self, game, pos, dir, damage):
        self._layer = THREE_LAYER
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups) 
        self.game = game
        self.image = game.bullet_images[game.player.weapon]
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(pos) #宣告兩個值
        self.rect.center = pos #中心座標=兩個值
        self.rot = 0 
        spread = uniform(-WEAPONS[game.player.weapon]['spread'], WEAPONS[game.player.weapon]['spread']) #隨機範圍值
        self.vel = dir.rotate(spread) * WEAPONS[game.player.weapon]['bullet_speed']
        #self.vel = dir * WEAPONS[game.player.weapon]['bullet_speed'] * uniform(0.9, 1.1) #子彈飛行方向與速度
        self.spawn_time = pg.time.get_ticks()
        self.weapon = game.player.weapon
        #self.damage = damage

    def update(self):#玩家子彈存亡判定
        self.pos += self.vel * self.game.dt #vel:[-50~50,-50~50]玩家為中心
        self.rect.center = self.pos #pos=[x,y]地圖位置
        self.rot = (self.vel).angle_to(self.rect.center)
        self.image = pg.transform.rotate(self.game.bullet_images[self.weapon], self.rot-45)
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.water):
            self.alive()
        if pg.time.get_ticks() - self.spawn_time > WEAPONS[self.game.player.weapon]['bullet_lifetime']:
            self.kill()

class Mob_Bullet(pg.sprite.Sprite): #敵人子彈
    def __init__(self, game, pos, dir):
        self._layer = THREE_LAYER
        self.groups = game.all_sprites, game.mob_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_bullet_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_BULLET_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(pos)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.rect.center = pos
        self.rot = 0
        self.spread = uniform(-MOB_GUN_SPREAD, MOB_GUN_SPREAD) #隨機範圍值
        self.vel = dir.rotate(self.spread) * MOB_BULLET_SPEED #子彈飛行方向與速度
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt #當下位置
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0)) #兩點: 玩家位置，現在位置，向量()
        self.acc = vec(1, 0).rotate(-self.rot) #[-1~1,-1~1]
        self.rect.center = self.pos
        self.rot = (self.vel).angle_to(self.rect.center)
        self.image = pg.transform.rotate(self.game.mob_bullet_img, self.rot-45)
        if pg.sprite.spritecollideany(self, self.game.walls):#敵人子彈存亡判定
            self.kill()
        if pg.sprite.spritecollideany(self, self.game.water):
            self.alive()
        if pg.time.get_ticks() - self.spawn_time > MOB_BULLET_LIFETIME:
            self.kill()

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ONE_LAYER
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Water(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ONE_LAYER
        self.groups = game.all_sprites, game.water
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.water_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Aqua(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.water
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.hit_rect = self.rect
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, type):
        self._layer = ONE_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        self.tween = tween.easeInOutSine
        self.step = 0
        self.dir = 1

    def update(self):
        offset = BOB_RANGE * (self.tween(self.step / BOB_RANGE) - 0.5)
        self.rect.centery = self.pos.y + offset * self.dir
        self.step += BOB_SPEED
        if self.step > BOB_RANGE:
            self.step = 0
            self.dir *= -1