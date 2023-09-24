import pygame
from pygame.locals import *

import tetris


def calculate_best_placement(FIELD, BLOCK: tetris.Block):
    tmp = list()
    tmp.append(K_SPACE)
    return tmp