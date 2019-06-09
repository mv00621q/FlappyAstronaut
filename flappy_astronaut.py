#!venv/bin/python3.7

# Copyright 2018 Yannick Kirschen. All rights reserved.
# Use of this source code is governed by the GNU-GPL
# license that can be found in the LICENSE file.

# Date created: Nov. 12, 2018


from sense_hat import SenseHat
from random import randint
from time import sleep

# Init and reset
sense = SenseHat()
sense.clear()
sense.set_rotation(180)
sense.low_light = True
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
matrix = [[BLUE for column in range(8)] for row in range(8)]

game_over = False

# Pixel of Astronaut
y = 0


def flatten(m):
    return [pixel for row in m for pixel in row]


def pipe(m):
    """
    Creates a new pipe a matrix.

    Parameters:
        m: Matrix to create a new pipe in

    Returns:
        A new pipe in the matrix with a random gap in it
    """
    for row in m:
        row[-1] = RED
    return gap(m)


def gap(m):
    """
    Puts a random gap in the right pipe of a matrix.

    Parameters:
        m: Matrix to put a gap in

    Returns:
        The matrix with a gap in the right pipe
    """
    g = randint(1, 5)
    m[g][-1] = BLUE
    m[g + 1][-1] = BLUE
    return m


def move_pipes(m):
    """
    Moves all pipes in a matrix one pixel to the left.

    Returns:
        The matrix itself
    """
    for row in m:
        for pixel in range(7):
            row[pixel] = row[pixel + 1]
        row[-1] = BLUE
    return m


def draw_astronaut(event):
    """
    Draws the astronaut.

    Parameters:
        event: Event of the SenseHAT
    """
    global y
    global game_over
    sense.set_pixel(0, y, BLUE)

    if event.action == 'pressed':
        if event.direction == 'down' and y > 0:
            y -= 1
        elif event.direction == 'up' and y < 7:
            y += 1
    elif event.direction == 'middle':
        game_over = False
    sense.set_pixel(0, y, YELLOW)


def check_collision(m):
    return m[y][0] == RED


if __name__ == '__main__':
    sense.stick.direction_any = draw_astronaut

    while not game_over:
        matrix = pipe(matrix)
        if check_collision(matrix):
            game_over = True
            break
        for i in range(3):
            sense.set_pixels(flatten(matrix))
            matrix = move_pipes(matrix)
            sense.set_pixel(0, y, YELLOW)
            if check_collision(matrix):
                game_over = True
                break
            sleep(0.6)

    sense.show_message('Game Over')
    sense.clear()
    exit()
