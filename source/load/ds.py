import pygame as pg
from pygame.locals import FULLSCREEN, DOUBLEBUF, QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN
import source.load.constant as const

flags = FULLSCREEN | DOUBLEBUF

pg.init()
pg.event.set_allowed([QUIT, KEYDOWN, KEYUP, MOUSEBUTTONDOWN])
pg.display.set_caption("Funky Friday at Home")

clock = pg.time.Clock()
screen = pg.display.set_mode((const.WIDTH, const.HEIGHT))