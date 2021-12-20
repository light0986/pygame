import pygame,sys
import time
from math import *
pygame.font.init()
pygame.init()
screen=pygame.display.set_mode((800,700))
screen.fill((255,255,255))
missile=pygame.image.load('./missile/370780-200.png').convert_alpha()
x1,y1=100,600 #飛彈的初始發射位置
velocity=800 #飛彈速度
time=1/1000 #每個時間片的長度
clock=pygame.time.Clock()
old_angle=0
score_font = pygame.font.SysFont("comicsans",30)

while True:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()


    clock.tick(60)#時間延遲

    screen.fill((255,255,255))

    x,y=pygame.mouse.get_pos() #獲取滑鼠位置，滑鼠就是需要打擊的目標

    score_label = score_font.render(str(x)+","+str(y), 1, (0,0,0))

    screen.blit(score_label,(2,6))
    
    distance=sqrt(pow(x1-x,2)+pow(y1-y,2)) #兩點距離公式

    section=velocity*time #每個時間片需要移動的距離

    sina=(y1-y)/distance

    cosa=(x-x1)/distance

    angle=atan2(y-y1,x-x1) #兩點線段的弧度值

    x1,y1=(x1+section*cosa,y1-section*sina)

    d_angle = degrees(angle) #弧度轉角度

    screen.blit(missile, (x1-missile.get_width(), y1-missile.get_height()/2)) #顯示

    dis_angle=d_angle-old_angle #dis_angle就是到下一個位置需要改變的角度

    old_angle=d_angle #更新初始角度

    pygame.display.update()

    


