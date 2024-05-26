import turtle
import random
import time
import copy

# Parameters
rows, cols = 45, 45
seed_size = 35
cell_size = 15
cell_color = "#f5e0f8"
color_background = '#302f30'
color_grid = '#484949'

# Setup turtle
screen = turtle.Screen()
screen.title("life 🌿")
screen.bgcolor(color_background)

t = turtle.Turtle()
t.speed(0)  # Fastest drawing speed
t.pencolor(color_grid)

# Hide the turtle cursor
t.hideturtle()

# Turn off the animation
screen.tracer(0)


def draw_square(t, size):
    for _ in range(4):
        t.forward(size)
        t.right(90)


def draw_grid(t, rows, cols, size):
    t.penup()
    start_x = -(cols // 2) * size
    start_y = (rows // 2) * size
    t.goto(start_x, start_y)
    t.pendown()

    for row in range(rows):
        for col in range(cols):
            draw_square(t, size)
            t.forward(size)
        t.penup()
        t.goto(start_x, start_y - (row + 1) * size)
        t.pendown()
        t.setheading(0)


draw_grid(t, rows, cols, cell_size)


def generate_init_data(size):
    return [[0 for _ in range(size)] for _ in range(size)]


game_data = generate_init_data(rows)


def paint_cell(row, col, size, color):
    start_x = -(cols // 2) * size
    start_y = (rows // 2) * size
    x = start_x + col * size
    y = start_y - row * size

    t.penup()
    t.goto(x, y)
    t.pendown()

    t.fillcolor(color)
    t.begin_fill()
    draw_square(t, size)
    t.end_fill()


def seed(grid_length, seed_area_size, cell_size):
    grid_center = grid_length // 2
    start_cell = grid_center - seed_area_size // 2

    for i in range(seed_area_size):
        for j in range(seed_area_size):
            game_data[start_cell + i][start_cell +
                                      j] = int(round(random.random()))


def evolve(game_data):
    new_game_data = copy.deepcopy(game_data)
    for y in range(rows):
        for x in range(rows):
            neighbours_amount = get_neighbours_amount(game_data, y, x)

            # underpopulation
            if (neighbours_amount < 2):
                new_game_data[y][x] = 0
            # overpopulation
            if (neighbours_amount > 3):
                new_game_data[y][x] = 0
            # reproduction
            if (neighbours_amount == 3):
                new_game_data[y][x] = 1

    return new_game_data


def render_game_data():
    size = len(game_data)
    for i in range(size):
        for j in range(size):
            color = cell_color if game_data[i][j] == 1 else color_background
            paint_cell(i, j, cell_size, color)


def get_data_for_cell(data, x, y):
    if x < 0 or x > len(data) - 1:
        return 0
    if y < 0 or y > len(data) - 1:
        return 0

    return data[y][x]


def get_neighbours_amount(data, row, col):
    x = col
    y = row

    tl = get_data_for_cell(data, x-1, y-1)
    tc = get_data_for_cell(data, x, y-1)
    tr = get_data_for_cell(data, x+1, y-1)
    cl = get_data_for_cell(data, x-1, y)
    cr = get_data_for_cell(data, x+1, y)
    bl = get_data_for_cell(data, x-1, y+1)
    bc = get_data_for_cell(data, x, y+1)
    br = get_data_for_cell(data, x+1, y+1)

    return tl + tc + tr + cl + cr + bl + bc + br


seed(rows, seed_size, cell_size)
# Initial rendering
render_game_data()
screen.update()

while True:
    t.clear()
    new_data = evolve(game_data)
    game_data = new_data
    render_game_data()
    screen.update()
