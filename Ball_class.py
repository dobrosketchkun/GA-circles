# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GA-cricles/Ball class
# Purpose:     educational
#
# Author:      Wisketchy Dobrov
#
# Copyright:   (c)2015
# Licence:     The BSD 3-Clause License
#-------------------------------------------------------------------------------

from gac_functions import *
from gac_variables import *
import Image, ImageDraw
import pygame
import os
path = os.path.dirname(__file__) + '\\img\\'

class Ball(pygame.sprite.Sprite):
    def __init__(self, raw_gene, *groups):
        super(Ball, self).__init__(*groups)
        self.done = 0
        if BALL_IMAGE_OPTION == 'random':

            self.color = RGB_gene_gen()
            (R,G,B) = int(self.color[0:8],2), int(self.color[9:17],2), int(self.color[18:26],2)
            self.file_name = path + '!' + hashlib.md5(str((R,G,B))).hexdigest() + '.ball'
            circle_img(32,self.file_name,(R,G,B))

            self.image = pygame.image.load(self.file_name)

            self.rect = pygame.rect.Rect(find_coor(BALL)[0], self.image.get_size())
        if BALL_IMAGE_OPTION == 'ball':
            self.image = pygame.image.load(path + 'ball.png')

            self.rect = pygame.rect.Rect(find_coor(BALL)[0], self.image.get_size())

        #self.raw_gene = gene_gen(random.randint(5,20))
        self.raw_gene = raw_gene
        self.dir_list = dir_gene_dec(self.raw_gene)

        #print self.dir_list

        self.dis_to_fin = None
##        [['down', 40], ['down', 28], ['up', 37], ['down', 44], ['left', 2],['up', 20],['down', 40],['left', 20]]]

    def update(self, dt, game):
        last = self.rect.copy()

        # Описание управления вручную
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT]:
            self.rect.x -= 300 * dt
        if key[pygame.K_RIGHT]:
            self.rect.x += 300 * dt
        if key[pygame.K_UP]:
            self.rect.y -= 300 * dt
        if key[pygame.K_DOWN]:
            self.rect.y += 300 * dt

        # Описание управление через гены направления
        if self.dir_list > 0:

            try:
                i = self.dir_list[0]
            ##############################
                if i[0] == 'up':
                    if i[1] > 0:
                        self.rect.y -= 10
                        i[1] = i[1] - 1
                    if i[1] == 0:
                        self.dir_list.remove(i)
            ##############################
                if i[0] == 'down':
                    if i[1] > 0:
                        self.rect.y += 10
                        i[1] = i[1] - 1
                    if i[1] == 0:
                        self.dir_list.remove(i)
            ##############################
                if i[0] == 'left':
                    if i[1] > 0:
                        self.rect.x -= 10
                        i[1] = i[1] - 1
                    if i[1] == 0:
                        self.dir_list.remove(i)
            ##############################
                if i[0] == 'right':
                    if i[1] > 0:
                        self.rect.x += 10
                        i[1] = i[1] - 1
                    if i[1] == 0:
                        self.dir_list.remove(i)
            ##############################
            except:
                pass
        else:
            pass


        # Обработка коллизий со спрайтами из группы walls
        new = self.rect
        for cell in pygame.sprite.spritecollide(self, game.wall, False):
            cell = cell.rect
            if last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if last.bottom <= cell.top and new.bottom > cell.top:
                new.bottom = cell.top
            if last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom
        for cell in pygame.sprite.spritecollide(self, game.fins, False):
            self.done = 1

