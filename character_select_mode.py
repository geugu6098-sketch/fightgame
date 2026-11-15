from pathlib import Path

from pico2d import SDL_QUIT, get_events, load_image

import game_config
import menu_ui


_character_select_image = None
_character_button_image = None
_exit_button_image = None
_exit_button_font = None

_character_button_positions = (
    (380, 460),
    (640, 460),
    (900, 460),
    (380, 245),
    (640, 245),
    (900, 245),
)
_character_button_size = 200


def init():
    global _character_select_image, _character_button_image
    global _exit_button_image, _exit_button_font
    image_path = (
        Path(__file__).resolve().parent
        / "resources"
        / "screen"
        / "main_select.png"
    )
    _character_select_image = load_image(str(image_path))
    button_path = (
        Path(__file__).resolve().parent
        / "resources"
        / "screen"
        / "character_select_button.png"
    )
    _character_button_image = load_image(str(button_path))
    _exit_button_image, _exit_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _character_select_image, _character_button_image
    global _exit_button_image, _exit_button_font
    _character_select_image = None
    _character_button_image = None
    _exit_button_image = None
    _exit_button_font = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if menu_ui.exit_button_clicked(event):
            return "select"
    return None


def draw():
    if (
        _character_select_image is None
        or _character_button_image is None
        or _exit_button_image is None
        or _exit_button_font is None
    ):
        raise RuntimeError("Character select mode has not been initialized.")
    _character_select_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    for x, y in _character_button_positions:
        _character_button_image.draw(
            x,
            y,
            _character_button_size,
            _character_button_size,
        )
    menu_ui.draw_exit_button(_exit_button_image, _exit_button_font)
