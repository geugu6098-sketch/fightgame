from pathlib import Path

from pico2d import SDL_KEYDOWN, SDL_QUIT, SDLK_ESCAPE, get_events, load_image


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

_opening_image = None


def init():
    global _opening_image
    image_path = Path(__file__).resolve().parent / "resources" / "screen" / "opening.png"
    _opening_image = load_image(str(image_path))


def finish():
    global _opening_image
    _opening_image = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return False
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return False
    return True


def draw():
    if _opening_image is None:
        raise RuntimeError("Opening mode has not been initialized.")
    _opening_image.draw(
        SCREEN_WIDTH // 2,
        SCREEN_HEIGHT // 2,
        SCREEN_WIDTH,
        SCREEN_HEIGHT,
    )
