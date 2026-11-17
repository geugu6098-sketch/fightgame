from pico2d import (
    SDL_BUTTON_LEFT,
    SDL_MOUSEBUTTONDOWN,
    SDL_MOUSEMOTION,
    SDL_QUIT,
    get_events,
    load_image,
)

import game_config
import game_state
import menu_ui


_character_select_image = None
_character_button_image = None
_superman_logo = None
_exit_button_image = None
_exit_button_font = None
_first_character_button_hovered = False

_character_button_positions = (
    (380, 460),
    (640, 460),
    (900, 460),
    (380, 245),
    (640, 245),
    (900, 245),
)
_character_button_size = 200
_superman_logo_size = 150


def init():
    global _character_select_image, _character_button_image, _superman_logo
    global _exit_button_image, _exit_button_font
    global _first_character_button_hovered
    _first_character_button_hovered = False
    image_path = game_config.RESOURCE_DIR / "screen" / "main_select.png"
    _character_select_image = load_image(str(image_path))
    button_path = game_config.RESOURCE_DIR / "screen" / "character_select_button.png"
    _character_button_image = load_image(str(button_path))
    logo_path = (
        game_config.RESOURCE_DIR
        / "character"
        / "superman"
        / "superman_logo.png"
    )
    _superman_logo = load_image(str(logo_path))
    _exit_button_image, _exit_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _character_select_image, _character_button_image, _superman_logo
    global _exit_button_image, _exit_button_font
    global _first_character_button_hovered
    _character_select_image = None
    _character_button_image = None
    _superman_logo = None
    _exit_button_image = None
    _exit_button_font = None
    _first_character_button_hovered = False


def _is_first_character_button_clicked(event):
    if event.type != SDL_MOUSEBUTTONDOWN or event.button != SDL_BUTTON_LEFT:
        return False

    x, y = _character_button_positions[0]
    mouse_y = game_config.SCREEN_HEIGHT - event.y
    half_size = _character_button_size // 2
    return (
        x - half_size <= event.x <= x + half_size
        and y - half_size <= mouse_y <= y + half_size
    )


def handle_events():
    global _first_character_button_hovered
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_MOUSEMOTION:
            x, y = _character_button_positions[0]
            _first_character_button_hovered = menu_ui.point_over_button(
                event,
                x,
                y,
                _character_button_size,
                _character_button_size,
            )
        if menu_ui.exit_button_clicked(event):
            return "select"
        if _is_first_character_button_clicked(event):
            game_state.selected_character = "superman"
            return "stage_select"
    return None


def draw():
    if (
        _character_select_image is None
        or _character_button_image is None
        or _superman_logo is None
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
    x, y = _character_button_positions[0]
    _superman_logo.draw(x, y, _superman_logo_size, _superman_logo_size)
    if _first_character_button_hovered:
        menu_ui.draw_hover_button(
            _exit_button_image,
            _exit_button_font,
            "슈퍼맨",
            60,
        )
    menu_ui.draw_exit_button(_exit_button_image, _exit_button_font)
