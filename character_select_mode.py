from pathlib import Path

from pico2d import SDL_QUIT, get_events, load_image

import game_config
import menu_ui


_character_select_image = None
_exit_button_image = None
_exit_button_font = None


def init():
    global _character_select_image, _exit_button_image, _exit_button_font
    image_path = (
        Path(__file__).resolve().parent
        / "resources"
        / "screen"
        / "main_select.png"
    )
    _character_select_image = load_image(str(image_path))
    _exit_button_image, _exit_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _character_select_image, _exit_button_image, _exit_button_font
    _character_select_image = None
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
    menu_ui.draw_exit_button(_exit_button_image, _exit_button_font)
