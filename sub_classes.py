# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GA-cricles/sub classes
# Purpose:     educational
#
# Author:      Wisketchy Dobrov
#
# Copyright:   (c)2015
# Licence:     The BSD 3-Clause License
#-------------------------------------------------------------------------------
import pygame
import sys
import os
##path = sys.path.append(os.path.join(sys.path[0], '\img'))

path = os.path.dirname(__file__) + '\\img\\'

class Wall(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Wall, self).__init__(*groups)
        self.image = pygame.image.load(path + 'wall.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
##        print self.image.get_size()


class Finish(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Finish, self).__init__(*groups)
        self.image = pygame.image.load(path + 'finish.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
##        print self.image.get_size()

