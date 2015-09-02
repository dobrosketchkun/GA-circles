# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GA-cricles/genetic functions
# Purpose:     educational
#
# Author:      Wisketchy Dobrov
#
# Copyright:   (c)2015
# Licence:     The BSD 3-Clause License
#-------------------------------------------------------------------------------

import random, hashlib
import re
import math
import Image, ImageDraw
from operator import itemgetter
from variables import *

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