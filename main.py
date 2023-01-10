#Testing
from config import * 
import numpy as np

import pygame as pg
from debug import Debug_menu
from ray import Ray, Light
from debug import Debug_menu


#render surfaces:
canvas = pg.Surface(CANVAS_DIM)
#shader surface
shader = pg.Surface(CANVAS_DIM, pg.SRCALPHA, 32)




screen = pg.display.set_mode(WINDOW_DIM)
pg.display.set_caption("Ray caster")
screen.fill((100,200,255))
pg.display.flip()
shader = shader.convert_alpha()




class Entity(object):

	#Common entity class

	def __init__(self, name, speed) -> None:
		
		self.sprite = PLAYER
		self.speed = speed
		self.scale = (4, 4)
		self.vel = 0
		self.air_time = 0
		self.is_jumping = True
		self.rect = PLAYER.get_rect()
		self.facing = True
		self.run_count = 1


	def render(self) -> None:
		#select right sprite from list
		canvas.blit(self.sprite, (self.rect.x - SCROLL[0], self.rect.y - SCROLL[1]))


	def move(self) -> None:

		#Get pressed keys
		keys = pg.key.get_pressed()
		#Check what keys are pressed and save them in move_vector
		move_vector = [0,0]
		#left and right
		if keys[ord('a')]:
			move_vector[0] -= 1
			self.facing = False

		if keys[ord('d')]:
			move_vector[0] -= -1
			self.facing = False
			

		if keys[ord('w')]:
			move_vector[1] += -1
			self.facing = True

		if keys[ord('s')]:
			move_vector[1] += 1
			self.facing = True



		#collision testing do mathematically: intersection of line and parabola
		self.rect.x += move_vector[0] * self.speed
		self.rect.y += move_vector[1] * self.speed



class Tile(object):

	#Basic tile obsticle object class

	def __init__(self, x, y) -> None:
		self.x = x
		self.y = y
		self.size = TILE_SIZE
		self.sprite = TILE
		self.rect = pg.Rect((self.x * self.size, self.y * self.size,), (self.size, self.size))


	def render(self) -> None:
		shader.blit(self.sprite, (self.x * self.size - SCROLL[0], self.y * self.size - SCROLL[1]))

	def get_lines(self):

		#get a list of lines making up tile

		top = ((self.x * TILE_SIZE, self.y* TILE_SIZE), (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE))

		bottom = ((self.x * TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE), (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE))

		left = ((self.x * TILE_SIZE, self.y * TILE_SIZE), (self.x * TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE))

		right = ((self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE), (self.x * TILE_SIZE + TILE_SIZE, self.y * TILE_SIZE + TILE_SIZE))

		return [top, bottom, left, right]



def collision_test(rect_1, rect_2):
	if rect_1.colliderect(rect_2):
		return True





def loop(entities, tiles, line_map) -> None:
	#Main game loop
	running = True
	clock = pg.time.Clock()
	debug = Debug_menu()
	fps = 'None'

	test_light = Light(0,0, line_map)

	while running:

		pol = []

		#clear last frame:
		canvas.fill((20,30,40))
		shader.fill(0)

		canvas.blit(BACK_GROUND,(0,0))
		#Move player
		entities[0].move()

		#render entities
		for entity in range(len(entities)):
			entities[entity].render()


		#	RAY CASTING
		#mouse_pos = pg.mouse.get_pos()

		#test_light.update(mouse_pos[0], mouse_pos[1])
		test_light.update(entities[0].rect.x,entities[0].rect.y)
		


		test_light.render_light(canvas)	

		#draw map outlines

		#render tiles
		for tile in range(len(tiles)):
			tiles[tile].render()


		for line in range(len(line_map)):
			#print(line_map[line][1])
			pg.draw.line(shader, (0,60,50), (line_map[line][0][0], line_map[line][0][1]), (line_map[line][1][0], line_map[line][1][1]))

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False
	
		#add shader layer on top of canvas		
		canvas.blit(shader,(0,0))

		scaled = pg.transform.scale(canvas, WINDOW_DIM)
		screen.blit(scaled,(0,0))
		debug.render(screen, fps)
		pg.display.flip()
		fps = f"FPS: {str(int(clock.get_fps()))}"
		clock.tick(FPS)



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
	
	player = Entity('player', speed = 1)
	entities.append(player)
	mouse_pos = pg.mouse.get_pos()
	print(mouse_pos)

	loop(entities, tiles, line_map)


if __name__ == "__main__":
	main()
