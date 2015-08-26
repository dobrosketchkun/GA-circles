# -*- coding: utf-8 -*-

import pygame, sys
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
BALL_IMAGE_OPTION = 'ball'



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

#####################################################################################

def RGB_gene_gen():
    """
    Генереривет последовательность 1 и 0, длиной 26 символов (т.е. 3*8)
    Т.к., приправильном разбитии можно это превратить в рандомный RGB-цвет
    """
    rgb_gene = ''
    for i in range(26):
        rgb_gene += random.choice('01')
    return rgb_gene

#####################################################################################

def gene_gen(number_of_genes):
    """
    Генерирует последовательность из 1 и 0, кратную 9
    """
    gene = ''
    for i in range(number_of_genes*9):
        gene += random.choice('01')
    return gene

#####################################################################################

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

#####################################################################################

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

#####################################################################################

def map_size():
    """
    Выдаёт размер карты из расчёт элементов в ней и размера блока, в формате (x, y)
    """
    with open(MAP_FILE) as f:
        lines = f.read().splitlines()
    return ( max([len(i) for i in lines])*WALL_BLOCK_SIZE, len(lines)*WALL_BLOCK_SIZE)

#####################################################################################

def find_best(list_of_scores, genes):
    """
    Возвращает отсортированный лист результатов, с добавленными спереди экземплярами,
    которые пришли на финиш до установленного времени.

    Возвращает список лучших генов. Формат подаваемого листа [[время, расстояние],[..,..],...]
    Длина возвращаемого листа примерно равна длине листа данных ( на самом деле
    длина равна (длина_листа/2 - длина_листа/2%4), для того, чтобы можно было разделить
    этот предварительный лист по парам

    """
    list_enum = list(enumerate(list_of_scores))
    best = [] # сохраняем те, которые за время раунда дошли

    for t in list(enumerate(list_of_scores)):
        if t[1][0] < 10:
            best.append(t)

    los2 = [(i[0],i[1][1]) for i in list_enum]

    l_sorted = sorted(los2, key=itemgetter(1))

    list_3 = [list_enum[i[0]] for i in l_sorted]
    list_4 = list_3[::-1] + best[::-1]
    list_5 =  list_4 [::-1]

    #list_6 = list_5[:(len(list_5)/2 - len(list_5)/2%4)]
    list_6 = list_5[:(len(list_5) - len(list_5)%4)]

    best_genes = []
    for i in list_6:
        for g in list(enumerate(genes)):
            if i[0] in g:
                best_genes.append(g[1])

    return best_genes

#####################################################################################

def mutation(ind, fr_mut = 0.1):
    """
    С заданной вероятностью изменяет случайный символ в последовательности
    из 1 и 0 на противоположенный. При подаче пустой последовательности
    выдаёт 00
    """

    if random.random() < fr_mut:
        if ind == '':
            return '00'
        else:
            try:
                point = random.randint(0, len(ind)-1)
            except:
                point = random.randint(0, len(ind))

        if ind[point] == '1':
            ind = ind[:point] + '0' + ind[(point + 1):]
        else:
            ind = ind[:point] + '1' + ind[(point + 1):]
        return ind
    else:
        return ind

#####################################################################################

def crossingover(ind1,ind2, fr_cross = 0.7, fr_double = 0.5):
    """
    Реализует кроссинговер(одинарный и двойной), делеции и дупликации, с заданной
    вероятностью. Возвращает лист [хромосома1, хромосома2]
    """
    r = float(random.randint(0,100))/100
    #print 'rand', r
    if r <= fr_cross:
        ind1_1 = random.randint(0,len(ind1))
        ind1_2 = random.randint(0,len(ind1))
        ind2_1 = random.randint(0,len(ind2))
        ind2_2 = random.randint(0,len(ind2))

        for i in range(100):
            if random.random() <= fr_double:
                cr_ind1 = ind1[:ind1_1] + ind2[ind2_1:ind2_2] + ind1[ind1_2:]
                cr_ind2 = ind2[:ind2_1] + ind1[ind1_1:ind1_2] + ind2[ind2_2:]
                #print 'f:', [ind1, cr_ind1]
                #print 's', [ind2, cr_ind2]
            else:
                cr_ind1 = ind1[ind1_1:] + ind2[:ind2_1]
                cr_ind2 = ind1[:ind1_1] + ind2[ind2_1:]
                #print 'f:', [ind1, cr_ind1]
                #print 's', [ind2, cr_ind2]
        return [cr_ind1, cr_ind2]
    else:
        return [ind1, ind2]

#####################################################################################

def cross(ind1,ind2,fr_mut = 0.1, fr_cross = 0.7, fr_double = 0.5):
    """
    Функация для удобства, реализует скрещивание двух хромосом, с заданными
    вероятностями мутации и кроссинговера/делеции/дупликации.
    Возвращает лист [хромосома1, хромосома2]
    """
    ind1_cr, ind2_cr = crossingover(ind1,ind2)
    return [mutation(ind1_cr), mutation(ind2_cr)]

#####################################################################################

def new_generation(gene_list):
    """
    Генерирует потомство на основе листа генов с чётным количеством членов.
    Из получившихся двух потомков случайным образом выбирается один
    """
    # Разделяем элементы листа по парам
    g1 = gene_list[slice(None, None, 2)]
    g2 = gene_list[1:][slice(None, None, 2)]
    paires = []
    for i in range(len(g1)):
        paires.append([g1[i],g2[i]])

    # Компануем потомство
    new_gen = []
    for i in paires:
        new_gen.append(cross(i[0],i[1]))
##    return new_gen

    really_new_gene = []

    for i in new_gen:
        really_new_gene.append(i[random.randint(0,1)])

    return really_new_gene

#####################################################################################

def length_testing(testing_list, length):
    """
    Проверяет длину листа новых генов. Если она меньше, чем число особей в
    популяции, то добавляет рандомные гены, если больше, то убирает с конца
    нужное количество. При равности длин возвращает лист неизменным.
    """
    if len(testing_list) < length:
        while len(testing_list) < length:
            # Добавляем случаный ген из testing_list
            testing_list.append(testing_list[random.randint(0, len(testing_list)-1)])
            # Добавляем новый случайный ген
            #testing_list.append(gene_gen(random.randint(5,20)))
        else:
            return testing_list

    if len(t) > length:
        while len(testing_list) > length:
            testing_list.remove(testing_list[-1])
        else:
            return testing_list

    else:
        return testing_list

#####################################################################################
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
#           СЕКТОР КЛАССОВ
#
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




class Ball(pygame.sprite.Sprite):
    def __init__(self, raw_gene, *groups):
        super(Ball, self).__init__(*groups)
        self.done = 0
        if BALL_IMAGE_OPTION == 'random':

            self.color = RGB_gene_gen()
            (R,G,B) = int(self.color[0:8],2), int(self.color[9:17],2), int(self.color[18:26],2)
            self.file_name = '!' + hashlib.md5(str((R,G,B))).hexdigest() + '.ball'
            circle_img(32,self.file_name,(R,G,B))

            self.image = pygame.image.load(self.file_name)

            self.rect = pygame.rect.Rect(find_coor(BALL)[0], self.image.get_size())
        if BALL_IMAGE_OPTION == 'ball':
            self.image = pygame.image.load('ball.png')

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
    def __init__(self, raw_gene):
        self.raw_gene = raw_gene
        self.quit = None

    def main(self, screen):
        clock = pygame.time.Clock()

        background = pygame.image.load('background.png')
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


if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode(map_size())

    list_of_games = []
    individuals  = 15
    for i in range(individuals): # количество особей в популяции
        raw_gene = gene_gen(random.randint(5,20))
        list_of_games.append(Game(raw_gene))

    generations = 50 # количество поколений
    for i in range(generations):
        print 'GENERATION', i
        list_of_scores = []
        list_of_genes = []

        for g in list_of_games:
            g.main(screen)

            if g.quit:
                list_of_scores.append([g.d_clock, g.ball.dis_to_fin])
                list_of_genes.append(g.ball.raw_gene)

        best_genes = find_best(list_of_scores,list_of_genes)
        new_gen = new_generation(best_genes) # потомки лучших генов
        really_new_gen = length_testing(new_gen, individuals) # новое поколение, сверной длиной листа, равного количеству особоей в популяции
        for g in range(len(list_of_games)):
            list_of_games[g].raw_gene = really_new_gen[g]


    pygame.quit()
    sys.exit()