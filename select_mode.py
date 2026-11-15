import os
from pathlib import Path

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_ESCAPE,
    get_events,
    load_font,
    load_image,
)

import game_config


_select_image = None
_button_image = None
_button_font = None

_menu_items = (
    ("게임하기", 112),
    ("옵션", 56),
    ("조작키 확인", 150),
    ("나가기", 84),
)
_button_width = 420
_button_height = 126
_button_center_x = 850
_button_top_center_y = 570
_button_vertical_spacing = 142


def init():
    global _select_image, _button_image, _button_font
    screen_path = Path(__file__).resolve().parent / "resources" / "screen"
    _select_image = load_image(str(screen_path / "mod_select.png"))
    _button_image = load_image(str(screen_path / "button.png"))
    font_path = Path(os.environ["WINDIR"]) / "Fonts" / "malgun.ttf"
    _button_font = load_font(str(font_path), 28)


def finish():
    global _select_image, _button_image, _button_font
    _select_image = None
    _button_image = None
    _button_font = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return "quit"
    return None


def draw():
    if _select_image is None or _button_image is None or _button_font is None:
        raise RuntimeError("Select mode has not been initialized.")
    _select_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    for index, (label, label_width) in enumerate(_menu_items):
        button_y = _button_top_center_y - index * _button_vertical_spacing
        _button_image.draw(
            _button_center_x,
            button_y,
            _button_width,
            _button_height,
        )
        _button_font.draw(
            _button_center_x - label_width // 2,
            button_y,
            label,
            (255, 255, 255),
        )