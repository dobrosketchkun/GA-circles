# -*- coding: utf-8 -*-

import pygame, sys
import tmx
import random, hashlib
import Image, ImageDraw
import time
import re
import math
from operator import itemgetter


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#     СЕКТОР ГЛОБАЛЬНЫХ ПЕРЕМЕННЫХ
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

MAP_FILE = 'map.map'
WALL_BLOCK_SIZE = 32
ROUND_TIME = 10
WALL = '#'
BALL = "B"
FINISH = 'F'




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#           СЕКТОР ФУНКЦИЙ
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


def circle_img(size, file_name, color):
    """
    Генерирует изображение размера size, с прозрачным фоном и кругом,
    диаметром size-1 и цветом color. Сохраняет в file_name (т.е. оно должно
    содержать расширение)
    """
    image = Image.new('RGBA', (size, size), (255,255,255,0))
    draw = ImageDraw.Draw(image)
    draw.ellipse((0, 0, size - 1, size - 1), fill = color, outline ='black')
    image.save(file_name, 'PNG')



def RGB_gene_gen():
    """
    Генереривет последовательность 1 и 0, длиной 26 символов (т.е. 3*8)
    Т.к., приправильном разбитии можно это превратить в рандомный RGB-цвет
    """
    rgb_gene = ''
    for i in range(26):
        rgb_gene += random.choice('01')
    return rgb_gene


def gene_gen(number_of_genes):
    """
    Генерирует последовательность из 1 и 0, кратную 9
    """
    gene = ''
    for i in range(number_of_genes*9):
        gene += random.choice('01')
    return gene


def dir_gene_dec(gene):
    """
    Декодирует последовательность гена в лист формата [[направление, число],...]
    Делит последовательно на куски по девять символов - первые два символа-
    это направление, остальные - число.
    """

    lg = re.findall('.'*9, gene)

    def dir_enc(x):
        for i in [['left', '00'],['right', '01',], ['up', '10'], ['down','11']]:
            if x in i:
                x = i[0]
        return x

    return [[dir_enc(i[0:2]),int(i[3:9],2)] for i in lg]



def find_coor(what):
    """
    Проходит по листу-карте и собирает координаты в формате[(x,y),(...),...]
    """
    with open(MAP_FILE) as f:
        lines = f.read().splitlines()

    some_map =  [[i] for i in lines]
    block_size = WALL_BLOCK_SIZE
    wall_coor_list = []  #
    for row in range(len(some_map)):
        for text in some_map[row]:
            wall_row = []
            for i in range(len(text)):
                if text[i] == what:
                    wall_row.append((i * block_size,  row * block_size))
        wall_coor_list.append(wall_row)
    return [item for sublist in wall_coor_list for item in sublist]



def map_size():
    """
    Выдаёт размер карты из расчёт элементов в ней и размера блока, в формате (x, y)
    """
    with open(MAP_FILE) as f:
        lines = f.read().splitlines()
    return ( max([len(i) for i in lines])*WALL_BLOCK_SIZE, len(lines)*WALL_BLOCK_SIZE)




#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#           СЕКТОР КЛАССОВ
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




class Ball(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super(Ball, self).__init__(*groups)
        self.done = 0

        self.color = RGB_gene_gen()
        (R,G,B) = int(self.color[0:8],2), int(self.color[9:17],2), int(self.color[18:26],2)
        self.file_name = '!' + hashlib.md5(str((R,G,B))).hexdigest() + '.png'
        circle_img(32,self.file_name,(R,G,B))

        self.image = pygame.image.load(self.file_name)

        self.rect = pygame.rect.Rect(find_coor(BALL)[0], self.image.get_size())
        self.raw_gene = gene_gen(random.randint(5,20))
        self.dir_list = dir_gene_dec(self.raw_gene)

        print self.dir_list

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



class Wall(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Wall, self).__init__(*groups)
        self.image = pygame.image.load('wall.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
##        print self.image.get_size()


class Finish(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Finish, self).__init__(*groups)
        self.image = pygame.image.load('finish.png')
        self.rect = pygame.rect.Rect(location, self.image.get_size())
##        print self.image.get_size()


class Game(object):
    def main(self, screen):
        clock = pygame.time.Clock()

        background = pygame.image.load('background.png')
        self.sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.fins = pygame.sprite.Group()

        self.wall = [Wall(i,self.walls) for i in find_coor(WALL)]
        self.ball = Ball(self.sprites)
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
                print 'Too late!'
                print self.ball.dis_to_fin
                self.quit = 1
                break

            if self.ball.done:
                print "Tah-dah!"
                print self.d_clock
                self.quit = 1
                break


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode(map_size())

    list_of_games = []
    list_of_scores = []

    for i in range(5):
        list_of_games.append(Game())
    for g in list_of_games:

        g.main(screen)
        if g.quit:
            list_of_scores.append([g.d_clock, g.ball.dis_to_fin])

    print list_of_scores
    pygame.quit()
    sys.exit()