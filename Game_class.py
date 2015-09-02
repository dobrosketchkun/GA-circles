# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GA-cricles/Game class
# Purpose:     educational
#
# Author:      Wisketchy Dobrov
#
# Copyright:   (c)2015
# Licence:     The BSD 3-Clause License
#-------------------------------------------------------------------------------
import pygame
import time
import os
from Genetics import *
from Adopters import *
from gac_variables import *
from Model import *

path = os.path.dirname(__file__) + '\\Resources\\img\\'

class Game(object):
    def __init__(self, raw_gene):
        self.raw_gene = raw_gene
        self.quit = None

    def main(self, screen):
        clock = pygame.time.Clock()

        background = pygame.image.load(path + 'background.png')
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.fins = pygame.sprite.Group()

        self.wall = [Wall(i,self.walls) for i in find_coor(WALL)]
        self.ball = Ball(self.raw_gene, self.sprites)
        self.finish = Finish(find_coor(FINISH)[0], self.fins)

        self.clock1 = time.time()
        while 1:
            dt = clock.tick(30)
            self.clock2 = time.time()


            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    return

            # Обновляем все группы спрайтов, и переносим всё на экран
            self.sprites.update(dt / 1000., self)
            self.walls.update(dt / 1000.)
            self.fins.update(dt / 1000.)
            screen.blit(background, (0, 0))
            self.walls.draw(screen)
            self.sprites.draw(screen)
            self.fins.draw(screen)
            pygame.display.flip()


            self.ball.dis_to_fin = math.sqrt((self.ball.rect.x - self.finish.rect.x)**2 + (self.ball.rect.y - self.finish.rect.y)**2)
            self.d_clock = self.clock2 - self.clock1

            if self.d_clock > ROUND_TIME:
                print 'Too late!', self.ball.dis_to_fin
                #print self.ball.dis_to_fin
                self.quit = 1
                break

            if self.ball.done:
                print "Tah-dah!", self.d_clock
                #print self.d_clock
                self.quit = 1
                break
