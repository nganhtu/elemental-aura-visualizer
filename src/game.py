from icecream import ic

import pygame as pg
import math

from config import *
import path
from board import Board
from gametime import Gametime
from dummy import Dummy


# Global variables
screen = None
clock = None
running = None
dt = None
favicon = None
element_pngs = None
aura_pngs = None
board = None
gametime = None
dummy = None


def init():
    global screen, clock, running, dt, favicon, element_pngs, aura_pngs

    # Pygame setup
    pg.init()
    screen = pg.display.set_mode((SCRW, SCRH), pg.SCALED)
    pg.display.set_caption(CAPTION)
    clock = pg.time.Clock()
    running = True
    dt = 0

    # Load pngs
    favicon = pg.image.load(path.FAVICON)
    pg.display.set_icon(favicon)
    element_pngs = {}
    aura_pngs = {}
    for aura in AURA_NAMES:
        img = pg.image.load(f"{path.AURAS + AURA_NAMES[aura]}.png")
        aura_pngs[aura] = img
        if aura in ELEMENTS:
            element_pngs[aura] = img


def draw_element_btns():
    global element_pngs
    for element in ELEMENTS:
        screen.blit(pg.transform.scale(element_pngs[element], (ELMS, ELMS)),
                    (MARGIN + ELMS * element, SCRH - MARGIN - ELMS))


def draw_gauge_btns():
    global board, screen
    font = pg.font.Font(path.FONT['zh-cn'], GAUS)
    for gauge in AVAILABLE_GAUGES:
        img = font.render(f"{gauge}U", True, TXTC_SELECTED if board.gauge == gauge else TXTC)
        screen.blit(img, (SCRW - MARGIN + GPAD * GAUGE_BTN_POSITION[gauge][0],
                          SCRH + (MARGIN + GAUB) * GAUGE_BTN_POSITION[gauge][1]))


def draw_gametime_btn():
    global gametime, screen
    font = pg.font.Font(path.FONT['zh-cn'], GTIS)
    img = font.render(f"{gametime.clock:.2f}", True, TXTC_SELECTED if gametime.isPaused else TXTC)
    screen.blit(img, (SCRW - MARGIN - GPAD * TIME_LMUL, SCRH - MARGIN - GAUB))
    img = font.render("s", True, TXTC_SELECTED if gametime.isPaused else TXTC)
    screen.blit(img, (SCRW - MARGIN - GPAD * TIME_RMUL, SCRH - MARGIN - GAUB))


def draw_aura_bars():
    global dummy
    # TODO


def draw_division_lines():
    global screen
    for i in range(1, MAX_COEXIST_AURAS_AVAILABLE + 1):
        for x in range(1, math.floor(MAX_AURA_GAUGE_AVAILABLE) + 1):
            pg.draw.rect(screen, RULER_COLOR, pg.Rect(
                x * RULER_W / MAX_AURA_GAUGE_AVAILABLE, RULER_PADDING_H * i,
                RULER_BLINE_W, RULER_BLINE_H))
        for x in range(1, math.ceil(MAX_AURA_GAUGE_AVAILABLE * RULER_LINE_RATIO) + 1):
            pg.draw.rect(screen, RULER_COLOR, pg.Rect(
                x * RULER_W / MAX_AURA_GAUGE_AVAILABLE / RULER_LINE_RATIO, RULER_PADDING_H * i,
                RULER_SLINE_W, RULER_SLINE_H))


def draw_screen():
    global screen
    screen.fill(BGRC)
    draw_element_btns()
    draw_gauge_btns()
    draw_gametime_btn()
    draw_aura_bars()
    draw_division_lines()


def main():
    global running, dt, board, gametime, dummy

    init()

    # Prepare game objects
    play_audio = {audio_name: pg.mixer.Sound(path.AUDIO[audio_name]).play for audio_name in path.AUDIO}
    play_audio.update({sound_name: pg.mixer.Sound(path.SOUND[sound_name]).play for sound_name in path.SOUND})
    board = Board()
    gametime = Gametime()
    dummy = Dummy()

    while running:
        # Poll for events
        for event in pg.event.get():

            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                play_audio['bark.wav']()
                running = False
                ic("Game quit on demand~")

            if event.type == pg.KEYDOWN and event.key in Board.ACTIVE_KEYS:
                res = board.press(pg.key.get_pressed())

                if res == FLIP_GAMETIME:
                    play_audio['open_win.mp3']() if gametime.isPaused else play_audio['close_win.mp3']()
                    gametime.isPaused = not gametime.isPaused

            if event.type == pg.MOUSEBUTTONDOWN:
                x, y = pg.mouse.get_pos()
                res = board.click(x, y)

                if res == FLIP_GAMETIME:
                    play_audio['open_win.mp3']() if gametime.isPaused else play_audio['close_win.mp3']()
                    gametime.isPaused = not gametime.isPaused

                elif res == SET_GAUGE:
                    play_audio['switch_type.mp3']()
                    ic("Gauge is set to~", board.gauge)

                elif res == APPLY_ELEMENT:
                    if board.gauge is None:
                        ic("Gauge is not chosen yet~")  # TODO warning to player
                    else:
                        play_audio['switch_task.mp3']()
                        dummy.affected_by(board.element, board.gauge)

        # Wipe away anything from last frame; then draw current frame
        draw_screen()

        # RENDER YOUR GAME HERE

        # flip() the display to put your work on screen
        pg.display.flip()

        dt = clock.tick(FPS) / MS_IN_A_SEC

        # Update things
        gametime.update(dt)
        if not gametime.isPaused:
            dummy.update(dt)

    pg.quit()


if __name__ == '__main__':
    main()
