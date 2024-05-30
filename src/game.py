from icecream import ic

import pygame as pg
import os
from config import *
import path
from board import Board
from gametime import Gametime


# Global variables
screen = None
clock = None
running = None
dt = None
element_pngs = None
board = None


def init():
    global screen, clock, running, dt, element_pngs

    # Pygame setup
    pg.init()
    screen = pg.display.set_mode((SCRW, SCRH), pg.SCALED)
    pg.display.set_caption(CAPTION)
    clock = pg.time.Clock()
    running = True
    dt = 0

    # Load file names
    element_pngs = []
    for file_name in os.listdir(path.ELEMENTS):
        element_pngs.append(pg.image.load(path.ELEMENTS + file_name))


def draw_element_btns():
    global element_pngs
    for i in range(len(element_pngs)):
        screen.blit(pg.transform.scale(element_pngs[i], (ELMS, ELMS)), \
                    (MARGIN + ELMS * i, SCRH - MARGIN - ELMS))


def draw_gauge_btns():
    global board, screen
    font = pg.font.Font(path.FONT['zh-cn'], GAUS)
    for gauge in AVAILABLE_GAUGES:
        img = font.render(f"{gauge}U", True, TXTC_SELECTED if board.gauge == gauge else TXTC)
        screen.blit(img, (SCRW - MARGIN + GPAD * GAUGE_BTN_POSITION[gauge][0], \
                          SCRH + (MARGIN + GAUB) * GAUGE_BTN_POSITION[gauge][1]))


def draw_gametime_btn():
    global gametime, screen
    font = pg.font.Font(path.FONT['zh-cn'], GTIS)
    img = font.render(f"{gametime.clock:.2f}", True, TXTC_SELECTED if gametime.isPaused else TXTC)
    screen.blit(img, (SCRW - MARGIN - GPAD * TIME_LMUL, SCRH - MARGIN - GAUB))
    img = font.render("s", True, TXTC_SELECTED if gametime.isPaused else TXTC)
    screen.blit(img, (SCRW - MARGIN - GPAD * TIME_RMUL, SCRH - MARGIN - GAUB))


def draw_screen():
    global screen
    screen.fill(BGRC)
    draw_element_btns()
    draw_gauge_btns()
    draw_gametime_btn()


def main():
    global running, dt, board, gametime

    init()

    # Prepare game objects
    board = Board()
    gametime = Gametime(0, False)

    while running:
        # TODO show info when pointing to a button

        # Poll for events
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                running = False
                ic("Game quit on demand~")
            if event.type == pg.KEYDOWN and event.key in board.ACTIVE_KEYS:
                res = board.press(pg.key.get_pressed())
                if res == FLIP_GAMETIME:
                    gametime.isPaused = not gametime.isPaused
                elif res == APPLY_ELEMENT:
                    pass # TODO apply element
            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                res = board.click(x, y)
                if res == FLIP_GAMETIME:
                    gametime.isPaused = not gametime.isPaused

        # Wipe away anything from last frame; then draw current frame
        draw_screen()

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pg.display.flip()

        dt = clock.tick(FPS) / MS_IN_A_SEC
        gametime.update(dt)

    pg.quit()


if __name__ == '__main__':
    main()

# TODO Glow up the icon when selecting it
