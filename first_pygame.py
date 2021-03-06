import pygame,math,sys
from pygame.locals import *
screen = pygame.display.set_mode((1024,768))
clock=pygame.time.Clock()

class Carsprite(pygame.sprite.Sprite):
    MAX_FORWARD_SPEED = 10
    MAX_REVERSE_SPEED = 10
    ACCELERATION = 2
    TURN_SPEED = 5

    def __init__(self,image,position):
        pygame.sprite.Sprite.__init__(self)
        self.src_image = pygame.image.load(image)
        self.position=position
        self.speed=self.direction=0
        self.k_left=self.k_right=self.k_down = self.k_up = 0

    def update(self, deltat):

        self.speed += (self.k_up + self.k_down)

        if self.speed> self.MAX_FORWARD_SPEED:
            self.speed=self.MAX_FORWARD_SPEED
        if self.speed< -self.MAX_REVERSE_SPEED:
            self.speed=-self.MAX_REVERSE_SPEED

        self.direction += (self.k_right + self.k_left )
        x,y = self.position
        rad=self.direction *math.pi /180
        x += -self.speed*math.sin(rad)
        y += -self.speed*math.cos(rad)

        self.position = (x,y)
        self.image = pygame.transform.rotate(self.src_image,self.direction)
        self.rect = self.image.get_rect()
        self.rect.center=self.position

class PadSprite(pygame.sprite.Sprite):
    
    normal = pygame.image.load('car.jpg')
    hit= pygame.image.load('hit.jpg')
    def __init__(self,position):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(self.normal.get_rect())
        self.rect.center = position

    def update(self,hit_dict):
        self.image = self.normal
        for car in hit_dict:
            if self in hit_dict[car]: self.image = self.hit
            #else: self.image = self.normal

pads = [
    PadSprite((200,200)),
    PadSprite((800,200)),
    PadSprite((200,600)),
    PadSprite((800,600)),
    ]

pad_group=pygame.sprite.RenderPlain(*pads)


rect=screen.get_rect()
car=Carsprite('normal.png',rect.center)
car_group=pygame.sprite.RenderPlain(car)
while 1:

    deltat= clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event,'key'): continue
        down = event.type == KEYDOWN
        if event.key == K_RIGHT: car.k_right = down*-5
        elif event.key == K_LEFT: car.k_left = down*5
        elif event.key == K_UP: car.k_up=down *2
        elif event.key == K_DOWN: car.k_down=down*-2
        elif event.key == K_ESCAPE : sys.exit(0)
    
    screen.fill((255,255,255))
    car_group.update(deltat)
    collisions = pygame.sprite.groupcollide(car_group,pad_group,False,False)
    pad_group.update(collisions)
    pad_group.draw(screen)
    car_group.draw(screen)
    pygame.display.flip()
    
