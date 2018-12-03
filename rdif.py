from drawBot import *

# Reaction-diffusion

##################################################

# hobeaux A
# RES = 200
# FRAMES = 10000
# FEED = 0.056
# KILL = 0.063
# TICK = 1
# dA = 1
# dB = 0.5

RES = 100
FRAMES = 101
FEED = 0.05
KILL = 0.0635
TICK = 1
dA = 0.25
dB = 0.125

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
            # a = agar, b = bacteria, c = clean (no feed distributed in C cells)
            CELLS[row].append({ 'a': 0, 'b': 0, 'c': 1 })

# Seed specific area with chem B
def Seed():
    print("Seeding base chemicals...")

    global CELLS

    dish = BezierPath()
    dish.text("X", font="M74.2 Bold Micro", fontSize = 125, align='center', offset=(RES/2,8))
    seed = BezierPath()
    seed.text("·", font="Hobeaux BD Regular", fontSize = 50, align='center', offset=(RES/2,30))
    for row in range(RES):
        for col in range(RES):
            if dish.pointInside((row,col)):
                CELLS[row][col]['a'] = 1
                CELLS[row][col]['c'] = 0
            if seed.pointInside((row,col)) and CELLS[row][col]['c'] == 0:
                CELLS[row][col]['b'] = 1

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
            fill(Constrain(2 * CELLS[row][col]['b'], 0, 1), 0, Constrain(2 * CELLS[row][col]['a'], 0, 1))
            rect(row, col, 1, 1)

# Run updates for each cell
def Tick():
    global CELLS, CELLS_NEW
    CELLS_NEW = CELLS

    for row in range(1, RES - 1):
        for col in range(1, RES - 1):
            if CELLS[row][col]['c'] > 0:
                continue

            a = CELLS[row][col]['a']
            b = CELLS[row][col]['b']

            CELLS_NEW[row][col]['a'] = a + (dA * Laplace(row, col, 'a')) - (a * b**2) + (FEED * (1 - a)) * TICK
            CELLS_NEW[row][col]['b'] = b + (dB * Laplace(row, col, 'b')) + (a * b**2) - ((KILL + FEED) * b) * TICK

            CELLS_NEW[row][col]['a'] = Constrain(CELLS_NEW[row][col]['a'], 0, 1)
            CELLS_NEW[row][col]['b'] = Constrain(CELLS_NEW[row][col]['b'], 0, 1)

    CELLS = CELLS_NEW

Setup()
#newPage(RES,RES)
Seed()

for frame in range(FRAMES):
    print("Processing states for frame " + str(frame + 1))
    Tick()
    if frame % 100 == 0:
        newPage(RES,RES)
        Render()

# newPage(RES,RES)
# Render()

print("Saving final output...")
saveImage("export.gif")
print("Done!")
