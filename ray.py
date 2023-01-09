#Raycasting test
from time import sleep
import pygame as pg
from numba import jit
from math import sin, cos, sqrt


DIM = (1200, 800)

canvas = pg.Surface(DIM)
screen = pg.display.set_mode(DIM)
pg.display.set_caption("Ray caster")

canvas.fill((100,200,255))

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
		self.angle = angle
	

	def update_pos(self, nx, ny):
		self.x1, self.y1 = nx, ny


	def find_end(self, lines):

		#line : [(x1, y1), (x2, y2)]
		#check ray collision by finding the collision point of 2 lines

		self.x2 = cos(self.angle) * self.cast_dist + self.x1
		self.y2 = sin(self.angle) * self.cast_dist + self.y1
		
		collisions = []

		intersect = False
		for line in range(len(lines)):

			lx1 = lines[line][0][0]
			ly1 = lines[line][0][1]

			lx2 = lines[line][1][0]
			ly2 = lines[line][1][1]

			#get collide point
			collide = intersection(self.x1, self.y1, self.x2, self.y2, lx1, ly1, lx2, ly2)
			#print(collidePos)
			
			if collide != None:
				
				collisions.append(collide)

				#[(x,y), (x,y)]


		#finde shortest distance collision to get first line hit:

		shortest = self.cast_dist + 1
		index = None

		for coll in range(len(collisions)):

			xl = (collisions[coll][0] - self.x1) ** 2
			yl = (collisions[coll][1] - self.y1) ** 2

			length = sqrt(xl + yl)

			if shortest > length:
				shortest = length
				index = coll
		try:		
			#print(collisions)
			self.x2 = collisions[index][0]
			self.y2 = collisions[index][1]

		except:
			pass

	def render(self, surface, x_offsett, y_offsett):
		pg.draw.line(surface, (100,100,100), (self.x1 + x_offsett, self.y1 + y_offsett), (self.x2 + y_offsett, self.y2 + y_offsett))


@jit # ray calculation
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


def create_rays(x1, y1) -> list:

	angle = 1
	rays = []
	#ray angle: fix
	for r in range(round(360 / angle)):
		ray = Ray(x1, y1, 1000, r * angle)

		#ray array
		rays.append(ray)

	return rays



###			MAP			###
game_map = [

	((50,200), (500,200)),
	((100, 100,), (600,50)),
	((500,300), (500,1000)),
	((600,10), (400,500)),
	((330,300), (300, 330))

	]


def draw_map(line_map):
	for l in range(len(line_map)):

		#map line
		x1 = game_map[l][0][0]
		print(x1)
		y1 = game_map[l][0][1]

		x2 = game_map[l][1][0]
		y2 = game_map[l][1][1]


		pg.draw.line(canvas, 'green', (x1, y1), (x2, y2))




def main() -> None:

	running = True

	rays = create_rays(0,0)

 
	mouse_pos = pg.mouse.get_pos()

	print(mouse_pos)

	while (running):


		#clear last frame
		canvas.fill((20, 30, 40))
		
		#Start of frame:


		#Mouse position -> tupple
		mouse_pos = pg.mouse.get_pos()

		for r in range(len(rays)):
			rays[r].update_pos(mouse_pos[0], mouse_pos[1])

			rays[r].find_end(game_map)

			rays[r].render(canvas , 0, 0)


		draw_map(game_map)

		#end of frame

		for event in pg.event.get():
			if event.type == pg.QUIT:
				running = False

		screen.blit(canvas, (0,0))
		pg.display.flip()
		sleep(1/60)


if __name__ == "__main__":
	main()


