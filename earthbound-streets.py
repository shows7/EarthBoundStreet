import pygame
from random import randint
from random import choice
import time
pygame.init()
 
COLORS = {'WHITE' : (255,255,255),
'BLACK' : (0,0,0),
'GREEN':(0,255,0),
'GRAY' :(177,179,188)}
 
SCREEN_WIDTH , SCREEN_HEIGHT = SCREEN_SIZE = (800, 600)

NESS_SPRITES = ['images/nessthekid.png',
'images/nessthekidshocked.png','images/nessthekidwalking .png']

CAR_TYPES = ['images/escargo_truck.png','images/jerk_truck.png',
            'images/taxi_truck.png','images/runaway_car.png','images/pytruck.png']

DIRECT_DICT = {pygame.K_a : (-1, 0), pygame.K_d : ( 1, 0),
               pygame.K_w : ( 0,-1), pygame.K_s : ( 0, 1)}



class Player(pygame.sprite.Sprite):
    injured = False
    change_x = 0
    change_y = 0
    speed = 5
    cars = None
    sprite = None
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([35,50])
        self.rect = self.image.get_rect()
        self.image.fill(COLORS['BLACK'])
        self.image.set_colorkey(COLORS['BLACK'])
        self.sprite = pygame.image.load(NESS_SPRITES[0])
        self.sprite.set_colorkey(COLORS['WHITE'])
    
    def update(self,keys):
        for key in DIRECT_DICT:
            if keys[key]:
                self.rect.x += self.speed*DIRECT_DICT[key][0]
                self.rect.y += self.speed*DIRECT_DICT[key][1]
        self.check_status()

    def check_status(self):
        car_hit_list = pygame.sprite.spritecollide(self,self.cars,False)
 
        for car in car_hit_list:
            self.injured = True
            self.sprite = pygame.image.load(NESS_SPRITES[1])
            self.sprite.set_colorkey(COLORS['WHITE'])
            self.last = pygame.time.get_ticks()
            self.rect.x += 20
            self.check_collision()
        self.check_pos()

    def check_collision(self):
        if self.injured == True:
            cooldown = 2500
            now = pygame.time.get_ticks()
            if now-self.last >= cooldown:
                self.sprite = pygame.image.load(NESS_SPRITES[0])
                self.sprite.set_colorkey(COLORS['WHITE'])
                self.injured = False
                last = now
    def check_pos(self):
        if self.rect.x < 0:
            pygame.quit()
            quit()

        if self.rect.x > SCREEN_WIDTH - 32:
            pygame.quit()
            quit()
        if self.rect.y < 263:
            pygame.quit()
            quit()
 
        if self.rect.y > 460:
            pygame.quit()
            quit()

    def draw(self, surface):
        surface.blit(self.sprite,self.rect)
        self.sprite.set_colorkey(COLORS['WHITE'])
 
class Vehicle(pygame.sprite.Sprite):
    length = 75
    width = 50
    def __init__(self, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([50,10])
        self.image.fill(COLORS['WHITE'])
        self.sprite = pygame.image.load(choice(CAR_TYPES))
        self.rect = self.image.get_rect()
        self.speed = randint(3, 11)
    
    def update(self):
        self.rect.x += self.speed
        self.check_reset()
    
    def check_reset(self):
        if self.rect.x > SCREEN_WIDTH:
            self.sprite = pygame.image.load(choice(CAR_TYPES))
            self.rect = self.image.get_rect()
            self.speed = randint(3, 11)

    def draw(self, screen):
        surface.blit(self.sprite,self.rect)

class App():
    def __init__(self):
        self.done = False
        self.player = Player()
        self.player.rect.y = 430
        self.player.rect.x = 380
        self.cars = self.make_cars()
        self.player.cars = self.cars
 
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.onnet = pygame.image.load('images/backgrouund.jpg').convert()

    def update(self):
        keys = pygame.key.get_pressed() 
        self.player.update(keys)
        self.cars.update()

    def render(self):
        self.screen.blit(self.onnet,(0,0))
        self.player.draw(self.screen)
        self.cars.draw(self.screen)
        pygame.display.update()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                done = True

    def main_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
            self.render()
            self.clock.tick(self.fps)

 
    def make_cars(self):
        self.cars = pygame.sprite.OrderedUpdates()
        for y in range(300, 550, 50):
            Vehicle((randint(-300,-75),y), self.cars)
        return self.cars

def main():
    pygame.display.set_mode(SCREEN_SIZE)
    App().main_loop()
    pygame.quit()
    quit()

if __name__ == '__main__':
    main()