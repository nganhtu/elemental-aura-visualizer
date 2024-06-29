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
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pg.SCALED)
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
        img = pg.image.load(f"{path.AURAS + AURA_NAMES[aura]}.png")  # not case sensitive
        aura_pngs[aura] = img
        if aura in ELEMENTS:
            element_pngs[aura] = img


def draw_element_btns():
    global element_pngs
    for element in ELEMENTS:
        screen.blit(pg.transform.scale(element_pngs[element], (ELEMENT_ICON_SIZE, ELEMENT_ICON_SIZE)),
                    (MARGIN + ELEMENT_ICON_SIZE * element, SCREEN_HEIGHT - MARGIN - ELEMENT_ICON_SIZE))


def draw_gauge_btns():
    global board, screen
    font = pg.font.Font(path.FONT['zh-cn'], GAUGE_BTN_SIZE)
    for gauge in AVAILABLE_GAUGES:
        text = font.render(f"{gauge}U", True, SELECTED_TEXT_COLOR if board.gauge == gauge else TEXT_COLOR)
        screen.blit(text, (SCREEN_WIDTH - MARGIN + GAUGE_BTN_PADDING * GAUGE_BTN_POSITION[gauge][0],
                           SCREEN_HEIGHT + (MARGIN + GAUGE_BTN_BORDER) * GAUGE_BTN_POSITION[gauge][1]))


def draw_gametime_btn():
    global gametime, screen
    font = pg.font.Font(path.FONT['zh-cn'], GAMETIME_BTN_SIZE)
    text = font.render(f"{gametime.clock:.2f}", True, SELECTED_TEXT_COLOR if gametime.isPaused else TEXT_COLOR)
    screen.blit(text, (SCREEN_WIDTH - MARGIN - GAUGE_BTN_PADDING * TIME_L_MULT,
                       SCREEN_HEIGHT - MARGIN - GAUGE_BTN_BORDER))
    text = font.render("s", True, SELECTED_TEXT_COLOR if gametime.isPaused else TEXT_COLOR)
    screen.blit(text, (SCREEN_WIDTH - MARGIN - GAUGE_BTN_PADDING * TIME_R_MULT,
                       SCREEN_HEIGHT - MARGIN - GAUGE_BTN_BORDER))


def draw_aura_bars_and_descriptions():
    global dummy, screen
    current_ruler = 0
    for aura in dummy.auras:
        current_ruler += 1
        # draw aura bars
        pg.draw.rect(screen, AURA_COLORS[aura.type], pg.Rect(
            0, RULER_PADDING_H * current_ruler,
            aura.gauge * RULER_W / MAX_AURA_GAUGE_AVAILABLE, RULER_H))
        # draw aura descriptions
        font = pg.font.Font(path.FONT['zh-cn'], 30)
        text = font.render(f"{AURA_NAMES[aura.type]} aura, decay rate: {aura.decay_rate:.2f}s, current gauge: {aura.gauge:.2f}U", True, TEXT_COLOR)
        screen.blit(text, (MARGIN, RULER_PADDING_H * (current_ruler - 0.3)))


def draw_division_lines():
    global screen
    for i in range(1, MAX_COEXIST_AURAS_AVAILABLE + 1):
        for x in range(1, math.floor(MAX_AURA_GAUGE_AVAILABLE) + 1):
            pg.draw.rect(screen, RULER_COLOR, pg.Rect(
                x * RULER_W / MAX_AURA_GAUGE_AVAILABLE, RULER_PADDING_H * i,
                RULER_BIG_LINE_W, RULER_BIG_LINE_H))
        for x in range(1, math.ceil(MAX_AURA_GAUGE_AVAILABLE * RULER_LINE_RATIO) + 1):
            pg.draw.rect(screen, RULER_COLOR, pg.Rect(
                x * RULER_W / MAX_AURA_GAUGE_AVAILABLE / RULER_LINE_RATIO, RULER_PADDING_H * i,
                RULER_SMALL_LINE_W, RULER_SMALL_LINE_H))


def draw_screen():
    global screen
    screen.fill(BACKGROUND_COLOR)
    draw_element_btns()
    draw_gauge_btns()
    draw_gametime_btn()
    draw_aura_bars_and_descriptions()
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

        dt = clock.tick(FPS) * MILLISECOND_TO_SECOND

        # Update things
        gametime.update(dt)
        if not gametime.isPaused:
            dummy.update(dt)

    pg.quit()


if __name__ == '__main__':
    main()
