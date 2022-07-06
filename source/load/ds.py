import pygame
from pygame.locals import *
import source.load.constant as const

flags = FULLSCREEN | DOUBLEBUF

pygame.init()
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])
pygame.display.set_caption("Funky Friday at Home")

clock = pygame.time.Clock()
screen = pygame.display.set_mode((const.WIDTH, const.HEIGHT))