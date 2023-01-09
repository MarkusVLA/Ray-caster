#Raycasting test
from time import sleep
import pygame.font
import pygame as pg
from numba import jit
from math import sin, cos, sqrt, pi

pygame.init()
DIM = (1200, 800)


LIGHT_SCALE = 400

test_canvas = pg.Surface(DIM)
screen = pg.display.set_mode(DIM)
pg.display.set_caption("Ray caster")

test_canvas.fill((100,200,255))
LIGHT = pg.transform.scale(pg.image.load('lib/light_t2.png'), (LIGHT_SCALE, LIGHT_SCALE))
pg.display.flip()

class Debug(object):
	def __init__(self) -> None:
		self.clock = pg.time.Clock()
		self.font = pygame.font.SysFont("Verdana", 11)
		self.text = ""

	def render(self, surface, text):
		self.text = self.font.render(text, True, 'white')
		surface.blit(self.text, (5,5))


class Ray(object):

	def __init__(self, x1, y1, cast_dist, angle, ray_id):

		#starting position
		self.x1 = x1
		self.y1 = y1

		#end position
		self.x2 = 0
		self.y2 = 0

		self.cast_dist = cast_dist
		self.angle = angle * pi/180

		self.ray_id = ray_id


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
	const = 1
	angles = []
	for i in range(int(360 / const)):
		angles.append(i * const)
	rays = []
	#ray angle: fix
	for r in range(len(angles)):
		ray = Ray(x1, y1, LIGHT_SCALE/2 - 1, angles[r], r)

		#ray array
		rays.append(ray)

	#rays = sort_rays(rays)
	return rays


def sort_rays(rays):
	#Sort rays in to correct rendering order
	rays.sort(key = lambda ray: ray.angle, reverse = False)
	return rays


def make_polygon(points, surface, size, pos):
	#points = ((x1,y1), (x2, y2), (x3, y3)), surface, size = (x,y)
	#pg.draw.polygon(surface, (255,255,160), points, width=0)
	new_surf = pg.Surface(size, pg.SRCALPHA, 32)
	new_surf.fill((20,30,40))
	pg.draw.polygon(new_surf, (255,0,0), points, width=0)
	new_surf.set_colorkey((255,0,0))

	#########
	surface.blit(LIGHT, (pos[0] - LIGHT_SCALE/2 , pos[1] - LIGHT_SCALE/2))	
	surface.blit(new_surf, (0,0))



###			MAP			###

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
	rays = create_rays(0,0)

	clock = pg.time.Clock()

	mouse_pos = pg.mouse.get_pos()

	debug = Debug()
	fps = 'begin'
	while (running):

		pol = []

		#clear last frame
		test_canvas.fill((20, 30, 40))
		
		#Start of frame:


		#Mouse position -> tupple
		mouse_pos = pg.mouse.get_pos()

		for r in range(len(rays)):
			#########
			rays[r].update_pos(mouse_pos[0], mouse_pos[1])


			
			rays[r].find_end(game_map)
			#rays[r].render(test_canvas , 0, 0)
			pol.append((rays[r].x2, rays[r].y2))

		make_polygon(pol, test_canvas, DIM,  mouse_pos)

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


