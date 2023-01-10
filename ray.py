#Raycasting test
from config import *
import pygame.font
import pygame as pg
from numba import jit
from math import sin, cos, sqrt, pi

from debug import Debug_menu



pygame.init()
DIM = (1200, 800)

test_canvas = pg.Surface(DIM)
screen = pg.display.set_mode(DIM)
pg.display.set_caption("Ray caster")

test_canvas.fill((100,200,255))
LIGHT = pg.transform.scale(pg.image.load('lib/light_t2.png'), (RAY_CAST_LENGTH, RAY_CAST_LENGTH))

pg.display.flip()


class Ray(object):

	def __init__(self, x1, y1, cast_dist, angle):

		#starting position
		self.x1 = x1
		self.y1 = y1

		#end position
		self.x2 = 0
		self.y2 = 0

		self.cast_dist = cast_dist
		self.angle = angle * pi/180


	def update_pos(self, nx, ny):
		self.x1, self.y1 = nx, ny
		

	def find_end(self, lines):

		#line : [(x1, y1), (x2, y2)]
		#check ray collision by finding the collision point of 2 lines

		self.x2 = cos(self.angle) * self.cast_dist + self.x1
		self.y2 = sin(self.angle) * self.cast_dist + self.y1
		
		collisions = []

		for line in range(len(lines)):

			x3 = lines[line][0][0];  y3 = lines[line][0][1]
			x4 = lines[line][1][0];  y4 = lines[line][1][1]

			collide_point = intersection(self.x1, self.y1, self.x2, self.y2, x3, y3, x4, y4)
			
			if collide_point:

				collisions.append(collide_point)

		if len(collisions) == 0:
			return None

		#finde shortest distance collision to get first line hit:

		shortest = self.cast_dist + 1
		index = None

		for coll in range(len(collisions)):

			length = sqrt((collisions[coll][0] - self.x1) ** 2 + (collisions[coll][1] - self.y1) ** 2)

			if shortest > length:
				shortest = length
				index = coll

		self.x2 = collisions[index][0]
		self.y2 = collisions[index][1]


	def render(self, surface, x_offsett, y_offsett):
		pg.draw.line(surface, (100,100,100), (self.x1 + x_offsett, self.y1 + y_offsett), (self.x2 + y_offsett, self.y2 + y_offsett))



class Light(object):
	
	def __init__(self, x, y, line_map):
		self.x = x
		self.y = y
		self.rays = []

		self.init = False
		self.polygon_points = []
		self.line_map = line_map
		#init rays	
		self.create_rays()

	def create_rays(self) -> None:

		angle_const = 2

		for i in range(int(360 / angle_const)):

			ray = Ray(self.x, self.y, RAY_CAST_LENGTH/2, i * angle_const)
			self.rays.append(ray)


	def update(self, nx, ny):
		#update light position and texture mask
		self.x = nx
		self.y = ny

		for ray in range(len(self.rays)):

			self.rays[ray].update_pos(self.x, self.y)
			self.rays[ray].find_end(self.line_map)

			if self.init == False:
				#initialize array when ran for the first time
				self.polygon_points.append((self.rays[ray].x2, self.rays[ray].y2))

			else:
				self.polygon_points[ray] = (self.rays[ray].x2, self.rays[ray].y2)

		self.init = True


	def render_rays(self, surface):

		for r in range(len(self.rays)):

			ray = self.rays[r]
			pg.draw.line(surface, (100,100,100), (ray.x1, ray.y1), (ray.x2, ray.y2))


	def render_polygon(self, surface):
		pg.draw.polygon(surface, (255,255,160), self.polygon_points, width=0)
		

	def render_light(self, surface):

		#points = ((x1,y1), (x2, y2), (x3, y3)), surface, size = (x,y)
		new_surf = pg.Surface(DIM, pg.SRCALPHA, 32)
		#new_surf = pg.Surface(DIM)
		
		new_surf.fill((20,30,40))

		pg.draw.polygon(new_surf, (255,0,0), self.polygon_points, width=0)
		new_surf.set_colorkey((255,0,0))	

		surface.blit(LIGHT, (self.x - RAY_CAST_LENGTH/2 , self.y - RAY_CAST_LENGTH/2))	
		surface.blit(new_surf, (0,0))


@jit(nopython=True) # ray calculation
def intersection(x1, y1, x2, y2, x3, y3, x4, y4):

	#intersection of line segments (x1, y1),(x2, y2) and (x3, y3),(x4, y4)
	de = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
	if de == 0:
		return None
	ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / de
	if ua < 0 or ua > 1:
		return None
	ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / de
	if ub < 0 or ub > 1:
		return None
	x = x1 + ua * (x2-x1)
	y = y1 + ua * (y2-y1)
	return (x,y)




###			     RAY LIB TESTING:             ###  

game_map = [

	((50,200), (500,200)),
	((100, 100,), (600,50)),
	((900,300), (1000,1000)),
	((600,10), (400,500)),
	((330,300), (300, 330))

	]


def draw_map(line_map):
	for l in range(len(line_map)):

		#map line
		x1 = game_map[l][0][0]
		y1 = game_map[l][0][1]

		x2 = game_map[l][1][0]
		y2 = game_map[l][1][1]


		pg.draw.line(test_canvas, 'green', (x1, y1), (x2, y2))




def main() -> None:

	running = True
	#rays = create_rays(0,0)

	clock = pg.time.Clock()

	mouse_pos = pg.mouse.get_pos()


	test_light = Light(0,0, game_map)

	test_light.update(mouse_pos[0], mouse_pos[1])

	debug = Debug_menu()
	fps = 'begin'
	while (running):

		#clear last frame
		test_canvas.fill((10, 10, 10))

		mouse_pos = pg.mouse.get_pos()
		
		test_light.update(mouse_pos[0], mouse_pos[1])


		test_light.render_light(test_canvas)
		#test_light.render_polygon(test_canvas)
		#test_light.render_rays(test_canvas)


		draw_map(game_map)

		debug.render(test_canvas, fps)
		#end of frame

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

		screen.blit(test_canvas, (0,0))
		pg.display.flip()
		#sleep(1/60)
		clock.tick()
		fps = f"FPS: {str(int(clock.get_fps()))}"


if __name__ == "__main__":
	main()


