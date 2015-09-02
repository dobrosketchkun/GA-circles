# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GA-cricles/other functions
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
