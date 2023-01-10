import pygame as pg

SCROLL = (0,0)

WINDOW_DIM = (1350, 900)
CANVAS_DIM = (150, 100)

TILE_SIZE = 16

RAY_CAST_LENGTH = 160

G_CONST = 8

FPS = 60

screen = pg.display.set_mode(WINDOW_DIM)
pg.display.set_caption("Ray caster")
pg.display.flip()


TILE = pg.transform.scale(pg.image.load('lib/test.png'), (TILE_SIZE, TILE_SIZE)).convert()
PLAYER = pg.transform.scale(pg.image.load('lib/yellow_square.png'), (4, 4)).convert()
LIGHT = pg.transform.scale(pg.image.load('lib/light.png'), (40, 40))
BACK_GROUND = pg.transform.scale(pg.image.load('lib/stone.png'), (CANVAS_DIM)).convert()