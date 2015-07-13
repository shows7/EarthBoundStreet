import os
import sys
import pygame
from random import randint
from random import choice
 
 
SCREEN_WIDTH, SCREEN_HEIGHT = SCREEN_SIZE = (800,600)

CAR_TYPES = ['images/pytruck.png','images/escargo_truck.png',
            'images/jerk_truck.png','images/runaway_car.png','images/taxi_truck.png']

COLORS = {'RED':(255,0,0),
         'BLUE':(0,0,255),
         'GREEN':(0,255,0),
         'BLACK':(0,0,0),
         'WHITE':(255,255,255)}
 

class Player(pygame.sprite.Sprite):    
    def __init__(self, pos):
        self.sheet = pygame.image.load('images/ness_sprites.png')
        self.sheet.set_clip(pygame.Rect(0, 0, 52, 76))
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.rect = self.image.get_rect(topleft=pos)
        self.alive = True
        self.frame = 0
        self.left_states = { 0: (0, 76, 52, 76), 1: (52, 76, 52, 76), 2: (156, 76, 52, 76) }
        self.right_states = { 0: (0, 152, 52, 76), 1: (52, 152, 52, 76), 2: (156, 152, 52, 76) }
        self.up_states = { 0: (0, 228, 52, 76), 1: (52, 228, 52, 76), 2: (156, 228, 52, 76) }
        self.down_states = { 0: (0, 0, 52, 76), 1: (52, 0, 52, 76), 2: (156, 0, 52, 76) }
        self.injured = False
        self.cooldown = 1000
        self.speed = 10
        self.bump_speed = 10
 
    def get_frame(self, frame_set):
        self.frame += 1
        if self.frame > (len(frame_set) - 1):
            self.frame = 0
        return frame_set[self.frame]
 
    def clip(self, clipped_rect):
        if type(clipped_rect) is dict:
            self.sheet.set_clip(pygame.Rect(self.get_frame(clipped_rect)))
        else:
            self.sheet.set_clip(pygame.Rect(clipped_rect))
        return clipped_rect
       
    def update(self, direction):
        if direction == 'left':
            self.clip(self.left_states)
            self.rect.x -= 10
        if direction == 'right':
            self.clip(self.right_states)
            self.rect.x += self.speed
        if direction == 'up':
            self.clip(self.up_states)
            self.rect.y -= self.speed
        if direction == 'down':
            self.clip(self.down_states)
            self.rect.y += self.speed
 
        if direction == 'stand_left':
            self.clip(self.left_states[0])
        if direction == 'stand_right':
            self.clip(self.right_states[0])
        if direction == 'stand_up':
            self.clip(self.up_states[0])
        if direction == 'stand_down':
            self.clip(self.down_states[0])
 
        self.image = self.sheet.subsurface(self.sheet.get_clip())
        self.check_status()

    def check_collision(self, cars):
        if pygame.sprite.spritecollideany(self, cars):
            self.injured = True
            self.image = pygame.image.load("images/nessthekidshocked.png")
            self.rect.x += self.bump_speed
            self.last_updated = pygame.time.get_ticks()
 
    def check_status(self):
        if self.injured:
            now = pygame.time.get_ticks()
            if now-self.last_updated >= self.cooldown:
                self.image = self.sheet.subsurface(self.sheet.get_clip())
                self.injured = False
                self.last_updated = now

        self.check_pos()

    def check_pos(self):
        if self.rect.x < 0:
            self.alive = False

        if self.rect.x > SCREEN_WIDTH - 32:
            self.alive = False
        
        if self.rect.y < 240:
            self.alive = False
 
        if self.rect.y > 435:
            self.alive = False

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            game_over = True
 
        if event.type == pygame.KEYDOWN:
           
            if event.key == pygame.K_LEFT:
                self.update('left')
            if event.key == pygame.K_RIGHT:
                self.update('right')
            if event.key == pygame.K_UP:
                self.update('up')
            if event.key == pygame.K_DOWN:
                self.update('down')
 
        if event.type == pygame.KEYUP:  
 
            if event.key == pygame.K_LEFT:
                self.update('stand_left')            
            if event.key == pygame.K_RIGHT:
                self.update('stand_right')
            if event.key == pygame.K_UP:
                self.update('stand_up')
            if event.key == pygame.K_DOWN:
                self.update('stand_down')


class Vehicle(pygame.sprite.Sprite):
    screen = None
    pos = None
    def __init__(self, pos, *groups):
        pygame.sprite.Sprite.__init__(self)
        self.sprite = pygame.image.load(choice(CAR_TYPES)).convert()
        self.image = pygame.Surface(self.sprite.get_rect().size)
        self.image.fill((255,255,255))
        self.sprite.set_colorkey(COLORS['WHITE'])
        self.rect = self.image.get_rect(bottomleft=pos)
        self.pos = pos
        self.speed = randint(3, 11)
    
    def update(self):
        self.rect.x += self.speed
        self.draw(self.screen)
        self.check_reset()
    
    def check_reset(self):
        if self.rect.x > SCREEN_WIDTH:
            self.sprite = pygame.image.load(choice(CAR_TYPES))
            self.sprite.set_colorkey(COLORS['WHITE'])
            self.rect = self.image.get_rect(bottomleft=self.pos)
            self.speed = randint(3, 11)

    def draw(self, surface):
        surface.blit(self.sprite,self.rect)
 
class App(object):
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.done = False
        self.player = Player((430,380))
        self.background = pygame.image.load('images/backgrouund.jpg')
        self.vehicle_list = pygame.sprite.OrderedUpdates()
        self.current_sound = 'soundtrack/Onnet.wav'
        self.force_stop = False
        self.game_end = Game_End(self.screen)
        self.already_done = False
        self.fps = 24
 
    def main_loop(self):
        while not self.done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done = True
        
            self.player.handle_event(event)
            self.player.check_collision(self.vehicle_list)
            self.screen.blit(self.background, (0,0))
            self.screen.blit(self.player.image, self.player.rect)
            self.vehicle_list.update()

            if self.player.alive == False:
                self.game_end.event_handler(event)
                self.force_stop = True
                self.current_sound = 'soundtrack/StandUpStrong.wav'
                self.draw_text()

            
            self.handle_music(self.current_sound)


            pygame.display.update()
            self.clock.tick(self.fps)

 
    def master_loop(self):
            self.make_cars()
            self.main_loop()

    def draw_text(self):
        if self.player.alive == False:
            self.game_end.draw_text()


    def handle_music(self,current_sound):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(current_sound)
            pygame.mixer.music.play(-1)

        if self.player.alive == False and self.already_done == False:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(current_sound)
            pygame.mixer.music.play(-1)
            self.already_done = True


    def make_cars(self):
        for y in range(300, 550, 50):
            vehicle = Vehicle((randint(-300,-75),y), self.vehicle_list)
            vehicle.screen = self.screen
            self.vehicle_list.add(vehicle)

class Game_End():
    def __init__(self,screen):
        self.screen = screen 
        self.death_background = pygame.image.load('images/EB_Game_Over.png').convert()

    def event_handler(self,event):
        self.draw_background()
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                pygame.quit()
                quit()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

    def draw_background(self):
        self.screen.blit(self.death_background,(0,0))

    def draw_text(self):
        gamefont = pygame.font.SysFont('arial', 35)
        text = gamefont.render('You Died!', True, (255, 255, 255))
        stattext = pygame.font.SysFont('arial',30)
        endtext = gamefont.render('Press any button to quit.', True, (255, 255, 255))

        self.screen.blit(text,(350,300))
        self.screen.blit(endtext,(350,400))


 
def main():
    pygame.init()
    pygame.display.set_mode(SCREEN_SIZE)
    icon = pygame.image.load('images/gameicon.png')
    icon.set_colorkey(COLORS['BLACK'])
    pygame.display.set_icon(icon)
    pygame.display.set_caption('EarthBound Street')
    pygame.mixer.init()
    App().master_loop()
    pygame.quit()
    sys.exit()
 
 
if __name__ == "__main__":
    main()