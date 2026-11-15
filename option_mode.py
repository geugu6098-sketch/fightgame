import os
from pathlib import Path

from pico2d import (
    SDL_BUTTON_LEFT,
    SDL_MOUSEBUTTONDOWN,
    SDL_QUIT,
    get_events,
    load_font,
    load_image,
)

import game_config


_options_image = None
_exit_button_image = None
_exit_button_font = None
_exit_button_width = 240
_exit_button_height = 72
_exit_button_margin = 12
_exit_button_center_x = _exit_button_margin + _exit_button_width // 2
_exit_button_center_y = (
    game_config.SCREEN_HEIGHT - _exit_button_margin - _exit_button_height // 2
)


def init():
    global _options_image, _exit_button_image, _exit_button_font
    screen_path = Path(__file__).resolve().parent / "resources" / "screen"
    font_path = Path(os.environ["WINDIR"]) / "Fonts" / "malgun.ttf"
    _options_image = load_image(str(screen_path / "main_select.png"))
    _exit_button_image = load_image(str(screen_path / "button.png"))
    _exit_button_font = load_font(str(font_path), 20)


def finish():
    global _options_image, _exit_button_image, _exit_button_font
    _options_image = None
    _exit_button_image = None
    _exit_button_font = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_MOUSEBUTTONDOWN and event.button == SDL_BUTTON_LEFT:
            mouse_y = game_config.SCREEN_HEIGHT - event.y
            button_left = _exit_button_center_x - _exit_button_width // 2
            button_right = _exit_button_center_x + _exit_button_width // 2
            button_bottom = _exit_button_center_y - _exit_button_height // 2
            button_top = _exit_button_center_y + _exit_button_height // 2
            if (
                button_left <= event.x <= button_right
                and button_bottom <= mouse_y <= button_top
            ):
                return "select"
    return None


def draw():
    if _options_image is None or _exit_button_image is None or _exit_button_font is None:
        raise RuntimeError("Option mode has not been initialized.")
    _options_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    _exit_button_image.draw(
        _exit_button_center_x,
        _exit_button_center_y,
        _exit_button_width,
        _exit_button_height,
    )
    _exit_button_font.draw(
        _exit_button_center_x - 30,
        _exit_button_center_y,
        "나가기",
        (255, 255, 255),
    )
