from pico2d import SDL_QUIT, get_events

import menu_ui


_menu_items = (
    ("혼자 하기", 122),
    ("같이 하기", 122),
    ("연습", 56),
)
_background_image = None
_button_image = None
_button_font = None


def init():
    global _background_image, _button_image, _button_font
    _background_image, _button_image, _button_font = menu_ui.load_assets()


def finish():
    global _background_image, _button_image, _button_font
    _background_image = None
    _button_image = None
    _button_font = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
    return None


def draw():
    if _background_image is None or _button_image is None or _button_font is None:
        raise RuntimeError("Game mode has not been initialized.")
    menu_ui.draw(
        _background_image,
        _button_image,
        _button_font,
        _menu_items,
    )
