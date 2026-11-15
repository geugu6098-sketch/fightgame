import os
from pathlib import Path

from pico2d import (
    SDL_KEYDOWN,
    SDL_QUIT,
    SDLK_ESCAPE,
    SDLK_SPACE,
    get_events,
    load_font,
    load_image,
)

import game_config


_opening_image = None
_prompt_font = None


def init():
    global _opening_image, _prompt_font
    image_path = Path(__file__).resolve().parent / "resources" / "screen" / "opening.png"
    _opening_image = load_image(str(image_path))
    font_path = Path(os.environ["WINDIR"]) / "Fonts" / "arial.ttf"
    _prompt_font = load_font(str(font_path), 28)


def finish():
    global _opening_image, _prompt_font
    _opening_image = None
    _prompt_font = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return "quit"
        if event.type == SDL_KEYDOWN and event.key == SDLK_SPACE:
            return "select"
    return None


def draw():
    if _opening_image is None or _prompt_font is None:
        raise RuntimeError("Opening mode has not been initialized.")
    _opening_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    _prompt_font.draw(511, 342, "Press the Space bar", (255, 255, 255))
