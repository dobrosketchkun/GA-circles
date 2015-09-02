# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GA-cricles/Wall class
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
from variables import path
##path = sys.path.append(os.path.join(sys.path[0], '\img'))

path = path + '\\Resources\\img\\'

class Wall(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Wall, self).__init__(*groups)
        self.image = pygame.image.load(path + 'wall.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
##        print self.image.get_size()