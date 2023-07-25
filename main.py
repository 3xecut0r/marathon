import random
from os import listdir

import pygame as pg
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pg.init()

FPS = pg.time.Clock()

screen = width, heigth = 800, 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font = pg.font.SysFont('Verdana', 20)

main_surface = pg.display.set_mode(screen)

IMGS_PATH = 'goose'

# player = pg.Surface((20, 20))
# player.fill(WHITE)
player_imgs = [pg.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
# player = pg.image.load('player.png').convert_alpha()
player = player_imgs[0]
player_rect = player.get_rect()
player_speed = 5


def create_enemy():
    # enemy = pg.Surface((20, 20))
    # enemy.fill(RED)
    resolution2 = 50, 25
    enemy = pg.transform.scale(pg.image.load('enemy.png').convert_alpha(), resolution2)
    enemy_rect = pg.Rect(width, random.randint(0, heigth), *enemy.get_size())
    enemy_speed = random.randint(2, 5)
    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    # bonus = pg.Surface((20, 20))
    # bonus.fill(GREEN)
    resolution = 50, 75
    bonus = pg.transform.scale(pg.image.load('bonus.png').convert_alpha(), resolution)
    bonus_rect = pg.Rect(random.randint(0, width), 5, *bonus.get_size())
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]

bg = pg.transform.scale(pg.image.load('background.png').convert(), screen)
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENEMY = pg.USEREVENT + 1
pg.time.set_timer(CREATE_ENEMY, 2500)

CREATE_BONUS = pg.USEREVENT + 2
pg.time.set_timer(CREATE_BONUS, 3500)

CHANGE_IMG = pg.USEREVENT + 3
pg.time.set_timer(CHANGE_IMG, 125)

img_index = 0

scores = 0

enemies = []
bonuses = []

is_working = True

while is_working:

    FPS.tick(64)

    for event in pg.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())

        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        
        
        if event.type == CHANGE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            player = player_imgs[img_index]
            
        
    pressed_keys = pg.key.get_pressed()

    # if player_rect.bottom >= heigth or player_rect.top <= 0:
    #     player_speed[1] = -player_speed[1]
    #     player.fill(BLUE)

    # if player_rect.right >= width or player_rect.left <= 0:
    #     player_speed[0] = -player_speed[0]
    #     player.fill(GREEN)

    # main_surface.fill(WHITE)
    
    # main_surface.blit(bg, (0, 0))
    
    bgX -= bg_speed
    bgX2 -= bg_speed
    
    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))
    
    if bgX < -bg.get_width():
        bgX = bg.get_width()
        
    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(player, player_rect)
    
    main_surface.blit(font.render(str(scores), True, BLACK), (width - 25, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
            
        
        if player_rect.colliderect(enemy[1]):
            is_working = False
     
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])
         
        if bonus[1].bottom >= heigth:
            bonuses.pop(bonuses.index(bonus))
            
        
        if player_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressed_keys[K_DOWN] and not player_rect.bottom >= heigth:
        player_rect = player_rect.move(0, player_speed)

    if pressed_keys[K_UP] and not player_rect.top <= 0:
        player_rect = player_rect.move(0, -player_speed)

    if pressed_keys[K_RIGHT] and not player_rect.right >= width:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_keys[K_LEFT] and not player_rect.left <= 0:
        player_rect = player_rect.move(-player_speed, 0)
    
    # main_surface.fill((155, 155, 155))
    pg.display.flip()
