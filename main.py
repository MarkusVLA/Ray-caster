#Testing

import numpy as np
import sys
import pygame as pg
from time import sleep
from ray import *


#ray caster ray length:
CAST_LENGTH = 50
TILE_SIZE = 32

#init pygame display
WINDOW_DIM = (1200, 600)
CANVAS_DIM = (400, 200)

canvas = pg.Surface(CANVAS_DIM)

#Shader surface to draw shader effects on:
shader = pg.Surface(CANVAS_DIM, pg.SRCALPHA, 32)


scroll = [0,0]

screen = pg.display.set_mode(WINDOW_DIM)
pg.display.set_caption("Ray caster")
screen.fill((100,200,255))
pg.display.flip()
shader = shader.convert_alpha()



#textures:
TILE = pg.transform.scale(pg.image.load('lib/test.png'), (TILE_SIZE, TILE_SIZE)).convert()
PLAYER = pg.transform.scale(pg.image.load('lib/test.png'), (4, 4)).convert()
LIGHT = pg.transform.scale(pg.image.load('lib/light.png'), (40, 40))



class Entity(object):

	#Common entity class

	def __init__(self, name, speed) -> None:
		self.name = name
		self.x = 100
		self.y = 50
		self.speed = speed
		self.rect = pg.Rect((self.x, self.y), (8, 8))
		self.velocity = [0, 0]
		self.facing = 'w'
		self.sprite = PLAYER
		self.ray_cast_angle_const = 10

	def render(self) -> None:
		#select right sprite from list
		canvas.blit(self.sprite, (self.x - scroll[0], self.y - scroll[1]))


	def move(self, dx, dy) -> None:

		self.x += dx * self.speed
		#scroll[0] += dx

		self.y += dy * self.speed
		#scroll[1] += dy

	def cast_rays(self):
		pass


class Tile(object):

	#Basic tile obsticle object class

	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y
		self.size = TILE_SIZE
		self.sprite = TILE
		self.rect = pg.Rect((self.x * self.size, self.y * self.size,), (self.size, self.size))


	def render(self) -> None:
		canvas.blit(self.sprite, (self.x * self.size - scroll[0], self.y * self.size - scroll[1]))

	def get_lines(self):

		#get a list of lines making up tile

		top = ((self.x * TILE_SIZE, self.y* TILE_SIZE), (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE))

		bottom = ((self.x * TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE), (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE))

		left = ((self.x * TILE_SIZE, self.y * TILE_SIZE), (self.x * TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE))

		right = ((self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE), (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE))

		return [top, bottom, left, right]





def input_events(player) -> None:

	keys = pg.key.get_pressed()

	if keys[ord('a')]:
		player.move(-1, 0)

	if keys[ord('d')]:
		player.move(1, 0)

	if keys[ord('w')]:
		player.move(0, -1)

	if keys[ord('s')]:
		player.move(0, 1)



def loop(entities, tiles, rays, line_map) -> None:
	#Main game loop
	running = True

	while running:
		#clear last frame:
		canvas.fill((20,30,40))
		shader.fill(0)

		#Move player
		input_events(entities[0])

		#render entities
		for entity in range(len(entities)):
			entities[entity].render()

		#render tiles
		for tile in range(len(tiles)):
			tiles[tile].render()
		#Render lights

		mouse_pos = pg.mouse.get_pos()

		#	RAY CASTING
		for r in range(len(rays)):
			rays[r].update_pos(entities[0].x, entities[0].y)

			rays[r].find_end(line_map)

			rays[r].render(shader, scroll[0], scroll[1])

		#draw map outlines
		for line in range(len(line_map)):
			#print(line_map[line][1])
			pg.draw.line(canvas, (0,100,80), (line_map[line][0][0], line_map[line][0][1]), (line_map[line][1][0], line_map[line][1][1]))

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
	
		#add shader layer on top of canvas		
		canvas.blit(shader,(0,0))

		scaled = pg.transform.scale(canvas, WINDOW_DIM)
		screen.blit(scaled,(0,0))
		pg.display.flip()

		sleep(1/60)


def load_level(level) -> list:

	#add tile objects to tiles array from level file
	tiles = []

	with open(level, "r") as game_level:
		for line in game_level.readlines():
			content = list(line.split(','))
			print(content)
			tile = Tile(int(content[0]),int(content[1]))
			tiles.append(tile)

	return tiles

def draw_line(x1, y1, x2, y2):
	pg.draw.line(canvas, 'green', (x1, y1), (x2, y2))

def main() -> None:

	#setup
	entities = []
	tiles = load_level('test.csv')

	#line map for ray casting
	line_map = []
	for t in range(len(tiles)):
		lines = tiles[t].get_lines()
		for i in range(4):
			line_map.append(lines[i])
	
	print(f"lineMap:\n{line_map}")

	rays = create_rays(0,0)
	player = Entity('player', speed = 3)
	entities.append(player)
	mouse_pos = pg.mouse.get_pos()
	print(mouse_pos)


	loop(entities, tiles, rays, line_map)


if __name__ == "__main__":
	main()
