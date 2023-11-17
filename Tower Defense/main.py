import pygame as pg
import constants as c

# initialize pygame
pg.init()

# create clock
clock = pg.time.Clock()

# create game window
screen = pg.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))

# game loop
run = True
while run:

    clock.tick(60)

    # event handler
    for event in pg.event.get():
        # quit program
        if event.type == pg.QUIT:
            run = False

pg.quit()
