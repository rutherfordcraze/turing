from drawBot import *

# Reaction-diffusion

##################################################

RES = 100
FRAMES = 5000
FEED = 0.055
KILL = 0.062
TICK = 1
dA = 1
dB = 0.5

##################################################

CELLS = []
CELLS_NEW = []

# Create the cell arrays
def Setup():
    print("Setting up cell arrays...")

    global CELLS
    for row in range(RES):
        CELLS.append([])
        for col in range(RES):
            CELLS[row].append({ 'a': 1, 'b': 0 })

# Seed specific area with chem B
def Seed():
    print("Seeding base chemicals...")

    global CELLS
    for row in range(20):
        for col in range(20):
            CELLS[row + 40][col + 40]['b'] = 1

    for row in range(10):
        for col in range(10):
            CELLS[row + 70][col + 80]['b'] = 1

# Calculate laplace function weights for local cells
def Laplace(x, y, type):
    sum = 0
    sum += CELLS[x][y][type] * -1
    sum += CELLS[x - 1][y][type] * 0.2
    sum += CELLS[x + 1][y][type] * 0.2
    sum += CELLS[x][y - 1][type] * 0.2
    sum += CELLS[x][y + 1][type] * 0.2
    sum += CELLS[x - 1][y - 1][type] * 0.05
    sum += CELLS[x - 1][y + 1][type] * 0.05
    sum += CELLS[x + 1][y - 1][type] * 0.05
    sum += CELLS[x + 1][y + 1][type] * 0.05
    return sum

def Constrain(value, min_val, max_val):
    return min(max_val, max(min_val, value))

# Draw a rect for each pixel
def Render():
    for row in range(RES):
        for col in range(RES):
            # if CELLS[row][col]['b'] < 0.5:
            #     fill(1)
            # else:
            #     fill(0)
            fill(Constrain(2 * CELLS[row][col]['b'], 0, 1))
            rect(row, col, 1, 1)

# Run updates for each cell
def Tick(frame = 0):
    print("Processing states for tick " + str(frame + 1) + ".")

    global CELLS, CELLS_NEW
    CELLS_NEW = CELLS

    for row in range(1, RES - 1):
        for col in range(1, RES - 1):
            a = CELLS[row][col]['a']
            b = CELLS[row][col]['b']

            CELLS_NEW[row][col]['a'] = a + (dA * Laplace(row, col, 'a')) - (a * b**2) + (FEED * (1 - a)) * TICK
            CELLS_NEW[row][col]['b'] = b + (dB * Laplace(row, col, 'b')) + (a * b**2) - ((KILL + FEED) * b) * TICK

            CELLS_NEW[row][col]['a'] = Constrain(CELLS_NEW[row][col]['a'], 0, 1)
            CELLS_NEW[row][col]['b'] = Constrain(CELLS_NEW[row][col]['b'], 0, 1)

    CELLS = CELLS_NEW

Setup()
Seed()

for frame in range(FRAMES):
    Tick(frame)
    if frame % 50 == 0:
        newPage(RES,RES)
        Render()

# newPage(RES,RES)
# Render()

print("Saving final output...")
saveImage("export.gif")
print("Done!")

# class Grid():

#     def __init__(self, res):
#         self.res = res

#     def getRes(self):
#         return self.res

# grid1 = Grid(101)
# grid2 = Grid(102)

# print("Grid 1 res: ", grid1.getRes())
# print("Grid 2 res: ", grid2.getRes())

# grid2 = grid1
# print("Swapped grids")
# print("Grid 1 res: ", grid1.getRes())
# print("Grid 2 res: ", grid2.getRes())
