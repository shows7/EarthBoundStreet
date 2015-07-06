import pygame
from random import randint
import time
from itertools import *
pygame.init()
 
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
GREY = (177,179,188)
 
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
 
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
ness = pygame.image.load('images/nessthekid.png').convert()
ness.set_colorkey(WHITE)
ness_standing = pygame.image.load('images/nessthekidstanding.png').convert()
ness_standing.set_colorkey(WHITE)
ness_walking = pygame.image.load('images/nessthekidwalking .png').convert()
ness_walking.set_colorkey(WHITE)
ness_shock = pygame.image.load('images/nessthekidshocked.png')
clock = pygame.time.Clock()
onnet = pygame.image.load('images/backgrouund.jpg').convert()
escargo_truck = pygame.image.load('images/escargo_truck.png').convert()
escargo_truck.set_colorkey(WHITE)
jerk_truck = pygame.image.load('images/jerk_truck.png').convert()
jerk_truck.set_colorkey(WHITE)
taxi_truck = pygame.image.load('images/taxi_truck.png').convert()
taxi_truck.set_colorkey(WHITE)
runaway_five_truck = pygame.image.load('images/runaway_car.png').convert()
runaway_five_truck.set_colorkey(WHITE)
py_truck = pygame.image.load('images/pytruck.png').convert()
py_truck.set_colorkey(WHITE)
game_over_screen = pygame.image.load('images/EB_Game_Over.png').convert()
is_walking_left = False
 
class Player(pygame.sprite.Sprite):
    injured = False
    change_x = 0
    last = None
    last_peace = None
    change_y = 0
    cars = None
    gifts = None
    peace = False
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([35,50])
        self.rect = self.image.get_rect()
    def move(self):
 
        car_hit_list = pygame.sprite.spritecollide(self,self.cars,False)
 
        for car in car_hit_list:
            self.injured = True
            self.last = pygame.time.get_ticks()
            self.rect.x += 250
 
 
        self.rect.x += self.change_x
 
 
        self.rect.y += self.change_y
 
class Vehicle(pygame.sprite.Sprite):
    length = 75
    width = 50
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([self.length,self.width])
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
    def move(self):
        random_num = randint(1,11)
        self.rect.x += random_num
 
def gameover_loop():
    over = False
    screen.fill(BLACK)
 
    while not over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.quit()
                    quit()
 
        screen.blit(game_over_screen,(0,0))
        gamefont = pygame.font.SysFont('arial', 35)
        text = gamefont.render('You Died!', True, (255, 255, 255))
        stattext = pygame.font.SysFont('arial',30)
        statustext = gamefont.render('You lasted %s s or %s ms.' % (game_loop.time_survived * 0.001,game_loop.time_survived), True, (255, 255, 255))
        quittext = pygame.font.SysFont('arial', 35)
        endtext = gamefont.render('Press SPACE to quit.', True, (255, 255, 255))
 
        screen.blit(text,(350,300))
        screen.blit(statustext,(350,400))
        screen.blit(endtext,(350,500))
 
        pygame.display.flip()
        clock.tick(60)
 
 
def go_left(time):
    ness_current = 1
    global ness
    ness_list = [ness_walking,ness_standing]
    current_time = pygame.time.get_ticks()
    now = 0
    cooldown = 1000
    ness = ness_list[ness_current]
    print current_time - game_loop.animation_timer
    if (current_time - game_loop.animation_timer) > 200:
        print 'Changing'
        if ness_current == 0:
            print 'Changing to sprite 1'
            now = pygame.time.get_ticks()
            ness_current = 1
            current_time = now
        elif ness_current == 1:
            print 'Changing to sprite 0'
            if (current_time - game_loop.animation_timer) > 200:
                ness_current = 0
                current_time = now
 
 
        else:
            'Changing to sprite 0 because of sprite reset'
            ness_current = 0
 
    current_time = now
 
 
 
 
 
def stop():
    global ness
    ness = pygame.image.load('images/nessthekid.png').convert()
    ness.set_colorkey(WHITE)
 
car_list = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_list = pygame.sprite.Group()
 
def game_loop():
    now = None
    count = 0
    global ness
    global is_walking_left
    player = Player()
    player.rect.y = 430
    player.rect.x = 380
    game_loop.animation_timer = pygame.time.get_ticks()
    player.cars = car_list
    player_list.add(player)
    car_one = Vehicle()
    car_list.add(car_one)
    car_one.rect.x = -100
    car_one.rect.y = 250
    car_two = Vehicle()
    car_two.rect.x = 100
    car_two.rect.y = 100
    car_list.add(car_two)
    car_two.rect.y = 350
    car_three = Vehicle()
    car_list.add(car_three)
    car_three.rect.x = 600
    car_three.rect.y = randint(270,400)
    car_three.random_num = 100
    car_four = Vehicle()
    car_list.add(car_four)
    car_four.random_num = randint(70,80)
    car_four.rect.x = 150
    car_four.rect.y = 350
    car_five = Vehicle()
    car_five.rect.x = 750
    car_five.rect.y = 395
    car_list.add(car_five)
    car_five.random_num = 1
    car_five.length = 158
    car_five.width = 57
 
    done = False
 
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    game_loop.timing = pygame.time.get_ticks()
                    go_left(1)
                    player.change_x -= 8
                if event.key == pygame.K_d:
                    player.change_x += 8
                if event.key == pygame.K_w:
                    player.change_y -= 8
                if event.key == pygame.K_s:
                    player.change_y += 8
 
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.change_x = 0
                    stop()
                if event.key == pygame.K_d:
                    player.change_x = 0
                if event.key == pygame.K_w:
                    player.change_y = 0
                if event.key == pygame.K_s:
                    player.change_y = 0
       
        screen.fill(WHITE)
        screen.blit(onnet,(0,0))
        score = 0
 
        car_one.move()
        car_two.move()
        car_three.move()
        car_four.move()
        car_five.move()
        for car in car_list:
            if car.rect.x > SCREEN_WIDTH + 75:
                car.rect.x = 0 - 75
 
        if player.rect.x > SCREEN_WIDTH - 50:
            break
           
        if player.rect.x < 0:
            break
        if player.rect.y < 263:
            break
 
        if player.rect.y > 460:
            break
        player.move()
        screen.blit(ness,(player.rect.x,player.rect.y))
        screen.blit(escargo_truck,(car_one.rect.x,car_one.rect.y))
        screen.blit(jerk_truck,(car_three.rect.x,car_three.rect.y))
        screen.blit(taxi_truck,(car_two.rect.x,car_two.rect.y))
        screen.blit(runaway_five_truck,(car_four.rect.x,car_four.rect.y))
        screen.blit(py_truck,(car_five.rect.x,car_five.rect.y))
        if player.injured == True:
            ness = pygame.image.load('images/nessthekidshocked.png').convert()
            ness.set_colorkey(WHITE)
            cooldown = 2500
            now = pygame.time.get_ticks()
            if now-player.last >= cooldown:
                ness = pygame.image.load('images/nessthekid.png').convert()
                ness.set_colorkey(WHITE)
                player.injured = False
                last = now
 
        all_sprites.draw(screen)
        game_loop.time_survived = pygame.time.get_ticks()
 
 
           
       
        pygame.display.flip()
        clock.tick(60)
 
game_loop()
print 'You survived for %s seconds or %s milliseconds' % (game_loop.time_survived * 0.001,game_loop.time_survived)
gameover_loop()