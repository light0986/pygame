import pygame
import os
import random
import time
pygame.font.init()

WIDTH, HEIGHT = 500,700
WIN = pygame.display.set_mode((WIDTH,HEIGHT))#視窗大小
pygame.display.set_caption("PNG Space Game")#視窗名
WHITE = (255,255,255)#背景顏色
BLACK = (0,0,0)

pygame.init()
pygame.mixer.init()


#player 
PLAYER_SHIP_IMG = pygame.image.load(os.path.join("pygame_img","370780-200.png"))
PLAYER_SHIP = pygame.transform.scale(PLAYER_SHIP_IMG,(50,50))#player大小

#enemy
ENEMY_SHIP1_IMG = pygame.image.load(os.path.join("pygame_img","unnamed.png"))
ENEMY_SHIP2_IMG = pygame.image.load(os.path.join("pygame_img","unnamed.png"))
ENEMY_SHIP3_IMG = pygame.image.load(os.path.join("pygame_img","unnamed.png"))
ENEMY_SHIP4_IMG = pygame.image.load(os.path.join("pygame_img","unnamed.png"))
ENEMY_SHIP5_IMG = pygame.image.load(os.path.join("pygame_img","unnamed.png"))

ENEMY_SHIP1 = pygame.transform.scale(ENEMY_SHIP1_IMG,(50,50))#enemy1大小
ENEMY_SHIP2 = pygame.transform.scale(ENEMY_SHIP2_IMG,(50,50))#enemy1大小
ENEMY_SHIP3 = pygame.transform.scale(ENEMY_SHIP3_IMG,(50,50))#enemy1大小
ENEMY_SHIP4 = pygame.transform.scale(ENEMY_SHIP4_IMG,(50,50))#enemy1大小
ENEMY_SHIP5 = pygame.transform.scale(ENEMY_SHIP5_IMG,(50,50))#enemy1大小

#laser
PLATER_LASER_IMG = pygame.image.load(os.path.join("pygame_img","dot_PNG29.png"))
ENEMY_SHIP1_LASER_IMG = pygame.image.load(os.path.join("pygame_img","dot_PNG29.png"))
ENEMY_SHIP2_LASER_IMG = pygame.image.load(os.path.join("pygame_img","dot_PNG29.png"))
ENEMY_SHIP3_LASER_IMG = pygame.image.load(os.path.join("pygame_img","dot_PNG29.png"))
ENEMY_SHIP4_LASER_IMG = pygame.image.load(os.path.join("pygame_img","dot_PNG29.png"))
ENEMY_SHIP5_LASER_IMG = pygame.image.load(os.path.join("pygame_img","dot_PNG29.png"))

PLATER_LASER = pygame.transform.scale(PLATER_LASER_IMG,(8,8))#子彈大小
ENEMY_SHIP1_LASER = pygame.transform.scale(ENEMY_SHIP1_LASER_IMG,(10,10))#子彈大小
ENEMY_SHIP2_LASER = pygame.transform.scale(ENEMY_SHIP2_LASER_IMG,(20,20))#子彈大小
ENEMY_SHIP3_LASER = pygame.transform.scale(ENEMY_SHIP3_LASER_IMG,(30,30))#子彈大小
ENEMY_SHIP4_LASER = pygame.transform.scale(ENEMY_SHIP4_LASER_IMG,(40,40))#子彈大小
ENEMY_SHIP5_LASER = pygame.transform.scale(ENEMY_SHIP5_LASER_IMG,(50,50))#子彈大小

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    
    def draw(self, window):
        window.blit(self.img, (self.x+21, self.y+21))
    
    def move(self, vel):
        self.y += vel
    
    def off_screen(self, height):
        return not(self.y <= height and self.y >= -60)
    
    def collision(self, obj):
        return collode(self, obj)

class Ship:
    COOLDOWN = 30
    def __init__(self,x,y,health=100,score=0):
        self.x = x
        self.y = y
        self.health = health
        self.score = score
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
    
    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -=10
                pygame.mixer.music.load('./pygame_img/qfrmy-dckrk.ogg') 
                pygame.mixer.music.play() 
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x,self.y,self.laser_img)
            pygame.mixer.music.load('./pygame_img/k1lyj-jsvto.ogg')
            pygame.mixer.music.play()
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

class Player(Ship):
    def __init__(self, x, y, health=100 , score=0):
        super().__init__(x, y, health ,score)
        self.ship_img = PLAYER_SHIP
        self.laser_img = PLATER_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.score = score
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.score +=1 #加一分
                        if self.health <= 99:
                            self.health +=1 #補血
                        if laser in self.lasers:
                            self.lasers.remove(laser)

    def draw(self, window):
        super().draw(window)
        self.healthbar(window)
        self.scorelabel(window)
    
    def healthbar(self,window): #血條
        pygame.draw.rect(window,(0,0,0),(148,665,202,20))
        pygame.draw.rect(window,(255,255,255),(149,666,((self.health/self.max_health)*200),18))
    
    def scorelabel(self,window): #顯示分數
        score_font = pygame.font.SysFont("comicsans",30)
        score_label = score_font.render(f"Score:{self.score}", 1, (0,0,0))
        window.blit(score_label,(2,32))



class EnemyShip(Ship):
    COLOR_MAP = {
                "E_SHIP1": (ENEMY_SHIP1 , ENEMY_SHIP1_LASER),
                "E_SHIP2": (ENEMY_SHIP2 , ENEMY_SHIP2_LASER),
                "E_SHIP3": (ENEMY_SHIP3 , ENEMY_SHIP3_LASER),
                "E_SHIP4": (ENEMY_SHIP4 , ENEMY_SHIP4_LASER),
                "E_SHIP5": (ENEMY_SHIP5 , ENEMY_SHIP5_LASER)
                }

    def __init__(self,x,y,str1, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[str1]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self,vel):
        self.y += vel
    
    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x-3,self.y,self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1
            
def collode(obj1, obj2):#傷害判定
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x - 25, offset_y)) != None

def main():
    run = True
    FPS = 60
    level = 0
    lives = 5

    with open("./pygame_img/savegame.txt", "rb") as f:#讀取紀錄
        foo = int(f.read())

    main_font = pygame.font.SysFont("comicsans", 50)
    lose_font = pygame.font.SysFont("comicsans", 60)
    foo_font = pygame.font.SysFont("comicsans",30)

    enemies = []
    wave_length = 5
    enemiy_vel = 1 #敵人移動速度
    laser_vel = 5 #子彈速度

    player_vel = 5 #玩家移動速度
    player=Player(220,500)#玩家起始位置
    clock = pygame.time.Clock()
    lose = False
    lose2 = True
    lose_count = 0
    
    def draw_window():
        WIN.fill(WHITE)#背景白色
        lives_label = main_font.render(f"Lives:{lives}", 1, (0,0,0))#黑色生命字
        level_label = main_font.render(f"Level:{level}", 1, (0,0,0))#黑色等級字
        foo_label = foo_font.render(f"High Score:{foo}", 1, (0,0,0))#最高分數

        WIN.blit(lives_label,(10, HEIGHT-lives_label.get_height()- 10))
        WIN.blit(level_label,(WIDTH - level_label.get_width() - 10, HEIGHT-level_label.get_height()- 10))
        WIN.blit(foo_label,(2,6))

        for enemy in enemies:
            enemy.draw(WIN)

        if lose:
            lose_label = lose_font.render("You Lose!!", 1,(0,0,0)) #輸掉遊戲
            WIN.blit(lose_label,(WIDTH/2 - lose_label.get_width()/2,300))
        else:
            player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        draw_window()

        if lives <= 0 or player.health <=0:
            lose = True

        if lose2 and lose :
            pygame.mixer.music.load('./pygame_img/4suvh-piwjo.ogg')
            pygame.mixer.music.play()
            lose2 = False
            
        if lose:
            if lose_count <= 300:
                lose_count += 1

            else:
                run = False
                if player.score >= foo:
                    ps = str(player.score)
                    sv = open("./pygame_img/savegame.txt","w")#存檔
                    sv.write(ps)
                    sv.close()
                
                continue

        if len(enemies) == 0:
            level += 1
            pygame.mixer.music.load('./pygame_img/xhhkb-o06br.ogg')
            pygame.mixer.music.play()
            wave_length += 5
            for i in range(wave_length):
                enemy = EnemyShip(random.randrange(50, WIDTH-100), random.randrange((-1000)-(level*100), -100), random.choice(["E_SHIP1","E_SHIP2","E_SHIP3","E_SHIP4","E_SHIP5"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x > 0:
            player.x -= player_vel #玩家往左
        if keys[pygame.K_RIGHT] and player.x + player.get_width() < WIDTH:
            player.x += player_vel #玩家往右
        if keys[pygame.K_UP] and player.y > 0:
            player.y -= player_vel #玩家往上
        if keys[pygame.K_DOWN] and player.y + player.get_height() < HEIGHT-40:
            player.y += player_vel #玩家往下
        if keys[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies:
            enemy.move(enemiy_vel)
            enemy.move_lasers(laser_vel, player)
            
            if random.randrange(1,500) <= level: #平均兩秒敵人發射武器
                enemy.shoot()

            if collode(enemy, player):
                player.health -= 10 #碰撞掉血
                pygame.mixer.music.load('./pygame_img/qfrmy-dckrk.ogg') 
                pygame.mixer.music.play() 
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                pygame.mixer.music.load('./pygame_img/qfrmy-dckrk.ogg') 
                pygame.mixer.music.play() 
                enemies.remove(enemy)

        
                    
        player.move_lasers(-laser_vel, enemies)#子彈射擊方向

def main_menu():

    title_font = pygame.font.SysFont("comicsans", 50)
    title_font1 = pygame.font.SysFont("comicsans", 30)
    title_font2 = pygame.font.SysFont("comicsans", 20)
    run = True

    while run:
        with open("./pygame_img/savegame.txt", "rb") as f:#讀取紀錄
            foo = int(f.read())
            
        WIN.fill(BLACK)
        title_label = title_font.render("Press any key to begin",1,WHITE)
        title_label1 = title_font1.render("MOVE: up / down / left / right  SHOOT: space",1,WHITE)
        title_label2 = title_font2.render("By Light0986",1,WHITE)
        highscore_label = title_font1.render(f"High Score:{foo}",1,WHITE)
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2,300))
        WIN.blit(title_label1, (WIDTH/2 - (title_label1.get_width()/2),400))
        WIN.blit(title_label2,(400,670))
        WIN.blit(highscore_label, (2,6))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYUP:
                pygame.mixer.music.load('./pygame_img/xhhkb-o06br.ogg')
                pygame.mixer.music.play()
                main()    
    pygame.quit()

main_menu()