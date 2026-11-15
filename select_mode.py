from pathlib import Path

from pico2d import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, get_events, load_image

import game_config


_select_image = None


def init():
    global _select_image
    image_path = Path(__file__).resolve().parent / "resources" / "screen" / "mod_select.png"
    _select_image = load_image(str(image_path))


def finish():
    global _select_image
    _select_image = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return "quit"
    return None


def draw():
    if _select_image is None:
        raise RuntimeError("Select mode has not been initialized.")
    _select_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )