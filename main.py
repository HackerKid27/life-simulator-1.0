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

class Carnivore(pygame.sprite.Sprite):
    def __init__(self, parent=None):
        super(Carnivore, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect()
        self.dir = rand(0, 179)
        self.life = t.time()
        if parent != None:
            self.speed = rand(parent.speed - 2, parent.speed + 2)
            self.life_span = rand(parent.life_span - 10, parent.life_span +10)
        else:
            self.speed = rand(2, 5)
            self.life_span = rand(10, 30)        
        
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
    
    def __init__(self, parent=None):
        super(MaleCarn, self).__init__()
        self.surf.fill((255,0,0))
        
    def update(self):
        super(MaleCarn, self).update()


class FemaleCarn(Carnivore):
    
    def __init__(self, parent=None):
        super(FemaleCarn, self).__init__()
        self.surf.fill((255,255,0))
        self.pregnant = False
        
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
            new_carn = MaleCarn(self)
            male_carns.add(new_carn)
            carnivores.add(new_carn)
            organisms.add(new_carn)
        else:
            new_carn = FemaleCarn(self)
            female_carns.add(new_carn)
            carnivores.add(new_carn)
            organisms.add(new_carn)
        self.pregnant = False


class Herbivore(pygame.sprite.Sprite):
    def __init__(self, parent=None):
        super(Herbivore, self).__init__()
        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect()
        self.dir = rand(0, 179)
        self.life = t.time()
        if parent != None:
            self.speed = rand(parent.speed - 2, parent.speed + 2)
            self.life_span = rand(parent.life_span - 10, parent.life_span +10)
        else:
            self.speed = rand(2, 5)
            self.life_span = rand(10, 30)        
        
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

        
class MaleHerb(Herbivore):
    
    def __init__(self, parent=None):
        super(MaleHerb, self).__init__()
        self.surf.fill((0,0,255))
        
    def update(self):
        super(MaleHerb, self).update()


class FemaleHerb(Herbivore):
    
    def __init__(self, parent=None):
        super(FemaleHerb, self).__init__()
        self.surf.fill((0,255,0))
        self.pregnant = False
        
    def update(self):
        super(FemaleHerb, self).update()
        if pygame.sprite.spritecollideany(self, male_herbs):
            if not self.pregnant:
                self.pregnant = True
                self.conception = t.time()
                self.due = rand(2, 7)
        if self.pregnant and t.time()-self.conception >= self.due:
            self.birth()        

    def birth(self):
        if rand(1, 7) < 4:
            new_herb = MaleHerb(self)
            male_herbs.add(new_herb)
            herbivores.add(new_herb)
            organisms.add(new_herb)
        else:
            new_herb = FemaleHerb(self)
            female_herbs.add(new_herb)
            herbivores.add(new_herb)
            organisms.add(new_herb)
        self.pregnant = False


screen = pygame.display.set_mode((1000, 750))
screen.fill((0,0,0))

organisms = pygame.sprite.Group()
carnivores = pygame.sprite.Group()
herbivores = pygame.sprite.Group()
male_carns = pygame.sprite.Group()
female_carns = pygame.sprite.Group()
male_herbs = pygame.sprite.Group()
female_herbs = pygame.sprite.Group()


tiger = MaleCarn()
tigeress = FemaleCarn()
buck = MaleHerb()
doe = FemaleHerb()
male_carns.add(tiger)
female_carns.add(tigeress)
male_herbs.add(buck)
female_herbs.add(doe)
carnivores.add(tiger, tigeress)
herbivores.add(buck, doe)
organisms.add(tiger, tigeress, buck, doe)


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    screen.fill((0,0,0))

    for entity in organisms:
        entity.update()
        screen.blit(entity.surf, entity.rect)

    pygame.display.flip()