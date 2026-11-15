from pico2d import SDL_QUIT, get_events

import menu_ui


_menu_items = (
    ("게임하기", 112),
    ("옵션", 56),
    ("조작키 확인", 150),
    ("나가기", 84),
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
        clicked_index = menu_ui.clicked_button_index(event, len(_menu_items))
        if clicked_index == 0:
            return "game"
        if clicked_index == len(_menu_items) - 1:
            return "quit"
    return None


def draw():
    if _background_image is None or _button_image is None or _button_font is None:
        raise RuntimeError("Select mode has not been initialized.")
    menu_ui.draw(
        _background_image,
        _button_image,
        _button_font,
        _menu_items,
    )