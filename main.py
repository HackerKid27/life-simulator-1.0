import pygame
from random import randint as rand
import math as m
import time as t


from pygame.locals import (
    QUIT,
    K_ESCAPE,
    KEYDOWN
)

pygame.init()

MALE_CARN = pygame.USEREVENT + 1
FEMALE_CARN = pygame.USEREVENT + 2

class Carnivore(pygame.sprite.Sprite):
    def __init__(self):
        super(Carnivore, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect()
        self.dir = rand(0, 179)
        self.speed = rand(2, 5)
        
    def update(self):
        if rand(1, 20) == 20:
            self.dir += rand(-45, 45)
        x_update = m.cos(self.dir*(m.pi/180))*self.speed
        y_update = m.sin(self.dir*(m.pi/180))*self.speed
        self.rect.move_ip(x_update, y_update)
        if self.rect.left < 0:
            self.rect.left = 0
            self.dir += 180
        if self.rect.right > 1000:
            self.rect.right = 1000
            self.dir += 180
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dir += 180
        if self.rect.bottom >= 750:
            self.rect.bottom = 750
            self.dir += 180
        if t.time()-self.life >= self.life_span:
            self.kill()

        
class MaleCarn(Carnivore):
    
    def __init__(self):
        super(MaleCarn, self).__init__()
        self.surf.fill((255,0,0))
        self.life = t.time()
        self.life_span = rand(10, 30)
        
    def update(self):
        super(MaleCarn, self).update()

class FemaleCarn(Carnivore):
    
    def __init__(self):
        super(FemaleCarn, self).__init__()
        self.surf.fill((255,255,0))
        self.pregnant = False
        self.life = t.time()
        self.life_span = rand(10, 30)
        
    def update(self):
        super(FemaleCarn, self).update()
        if pygame.sprite.spritecollideany(self, male_carns):
            if not self.pregnant:
                self.pregnant = True
                self.conception = t.time()
                self.due = rand(2, 7)
        if self.pregnant and t.time()-self.conception >= self.due:
            self.birth()
        

    def birth(self):
        if rand(1, 7) < 4:
            pygame.event.post(pygame.event.Event(MALE_CARN))
        else:
            pygame.event.post(pygame.event.Event(FEMALE_CARN))
        self.pregnant = False


screen = pygame.display.set_mode((1000, 750))
screen.fill((0,0,0))

organisms = pygame.sprite.Group()
carnivores = pygame.sprite.Group()
male_carns = pygame.sprite.Group()
female_carns = pygame.sprite.Group()


adam = MaleCarn()
eve = FemaleCarn()
male_carns.add(adam)
female_carns.add(eve)
carnivores.add(adam, eve)
organisms.add(adam, eve)


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == MALE_CARN:
            new_carn = MaleCarn()
            male_carns.add(new_carn)
            carnivores.add(new_carn)
            organisms.add(new_carn)
        elif event.type == FEMALE_CARN:
            new_carn = FemaleCarn()
            female_carns.add(new_carn)
            carnivores.add(new_carn)
            organisms.add(new_carn)


    screen.fill((0,0,0))

    for entity in organisms:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()