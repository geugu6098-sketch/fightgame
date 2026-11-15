import os
from pathlib import Path

from pico2d import SDL_BUTTON_LEFT, SDL_MOUSEBUTTONDOWN, load_font, load_image

import game_config


_BUTTON_WIDTH = 420
_BUTTON_HEIGHT = 126
_BUTTON_CENTER_X = 850
_BUTTON_VERTICAL_SPACING = 142
_FONT_SIZE = 28
_EXIT_BUTTON_WIDTH = 240
_EXIT_BUTTON_HEIGHT = 72
_EXIT_BUTTON_MARGIN = 12
_EXIT_BUTTON_CENTER_X = _EXIT_BUTTON_MARGIN + _EXIT_BUTTON_WIDTH // 2
_EXIT_BUTTON_CENTER_Y = (
    game_config.SCREEN_HEIGHT - _EXIT_BUTTON_MARGIN - _EXIT_BUTTON_HEIGHT // 2
)
_EXIT_FONT_SIZE = 20


def load_assets():
    screen_path = Path(__file__).resolve().parent / "resources" / "screen"
    font_path = Path(os.environ["WINDIR"]) / "Fonts" / "malgunbd.ttf"
    return (
        load_image(str(screen_path / "mod_select.png")),
        load_image(str(screen_path / "button.png")),
        load_font(str(font_path), _FONT_SIZE),
    )


def load_exit_button_assets():
    screen_path = Path(__file__).resolve().parent / "resources" / "screen"
    font_path = Path(os.environ["WINDIR"]) / "Fonts" / "malgunbd.ttf"
    return (
        load_image(str(screen_path / "button.png")),
        load_font(str(font_path), _EXIT_FONT_SIZE),
    )


def draw(background_image, button_image, button_font, menu_items):
    background_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    first_button_y = game_config.SCREEN_HEIGHT // 2 + (
        (len(menu_items) - 1) * _BUTTON_VERTICAL_SPACING // 2
    )
    for index, (label, label_width) in enumerate(menu_items):
        button_y = first_button_y - index * _BUTTON_VERTICAL_SPACING
        button_image.draw(
            _BUTTON_CENTER_X,
            button_y,
            _BUTTON_WIDTH,
            _BUTTON_HEIGHT,
        )
        button_font.draw(
            _BUTTON_CENTER_X - label_width // 2,
            button_y,
            label,
            (255, 255, 255),
        )


def draw_exit_button(button_image, button_font):
    button_image.draw(
        _EXIT_BUTTON_CENTER_X,
        _EXIT_BUTTON_CENTER_Y,
        _EXIT_BUTTON_WIDTH,
        _EXIT_BUTTON_HEIGHT,
    )
    button_font.draw(
        _EXIT_BUTTON_CENTER_X - 30,
        _EXIT_BUTTON_CENTER_Y,
        "나가기",
        (255, 255, 255),
    )


def exit_button_clicked(event):
    if event.type != SDL_MOUSEBUTTONDOWN or event.button != SDL_BUTTON_LEFT:
        return False

    mouse_y = game_config.SCREEN_HEIGHT - event.y
    button_left = _EXIT_BUTTON_CENTER_X - _EXIT_BUTTON_WIDTH // 2
    button_right = _EXIT_BUTTON_CENTER_X + _EXIT_BUTTON_WIDTH // 2
    button_bottom = _EXIT_BUTTON_CENTER_Y - _EXIT_BUTTON_HEIGHT // 2
    button_top = _EXIT_BUTTON_CENTER_Y + _EXIT_BUTTON_HEIGHT // 2
    return (
        button_left <= event.x <= button_right
        and button_bottom <= mouse_y <= button_top
    )


def clicked_button_index(event, button_count):
    if event.type != SDL_MOUSEBUTTONDOWN or event.button != SDL_BUTTON_LEFT:
        return None

    mouse_y = game_config.SCREEN_HEIGHT - event.y
    first_button_y = game_config.SCREEN_HEIGHT // 2 + (
        (button_count - 1) * _BUTTON_VERTICAL_SPACING // 2
    )
    button_left = _BUTTON_CENTER_X - _BUTTON_WIDTH // 2
    button_right = _BUTTON_CENTER_X + _BUTTON_WIDTH // 2
    for index in range(button_count):
        button_y = first_button_y - index * _BUTTON_VERTICAL_SPACING
        button_bottom = button_y - _BUTTON_HEIGHT // 2
        button_top = button_y + _BUTTON_HEIGHT // 2
        if (
            button_left <= event.x <= button_right
            and button_bottom <= mouse_y <= button_top
        ):
            return index
    return None
