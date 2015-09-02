# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        GA-cricles
# Purpose:     educational
#
# Author:      Wisketchy Dobrov
#
# Copyright:   (c)2015
# Licence:     The BSD 3-Clause License
#-------------------------------------------------------------------------------

import pygame, sys
import random
from gac_variables import *
from Genetics import *
#from other_functions import *
from Adopters import *
from Game_class import *
from Model import *



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