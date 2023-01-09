from main import CANVAS_DIM, TILE_SIZE

N = 10

from random import randint
with open('test.csv', 'w') as out:
    for i in range(N):
        out.write(f'{randint(0, int(CANVAS_DIM[0] / TILE_SIZE))},{randint(0, int(CANVAS_DIM[1] / TILE_SIZE))}\n')

print("Done =)")