from pico2d import (
    SDL_BUTTON_LEFT,
    SDL_MOUSEBUTTONDOWN,
    SDL_MOUSEMOTION,
    SDL_QUIT,
    get_events,
    load_image,
)

import game_config
import menu_ui


_stage_select_image = None
_stage_button_image = None
_exit_button_image = None
_exit_button_font = None
_first_stage_button_hovered = False

_stage_button_positions = (
    (230, 470),
    (640, 470),
    (1050, 470),
    (230, 250),
    (640, 250),
    (1050, 250),
)
_stage_button_width = 300
_stage_button_height = 169


def init():
    global _stage_select_image, _stage_button_image
    global _exit_button_image, _exit_button_font
    global _first_stage_button_hovered
    _first_stage_button_hovered = False
    image_path = game_config.RESOURCE_DIR / "screen" / "main_select.png"
    _stage_select_image = load_image(str(image_path))
    button_path = game_config.RESOURCE_DIR / "screen" / "stage_select_button.png"
    _stage_button_image = load_image(str(button_path))
    _exit_button_image, _exit_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _stage_select_image, _stage_button_image
    global _exit_button_image, _exit_button_font
    global _first_stage_button_hovered
    _stage_select_image = None
    _stage_button_image = None
    _exit_button_image = None
    _exit_button_font = None
    _first_stage_button_hovered = False


def _is_first_stage_button_clicked(event):
    if event.type != SDL_MOUSEBUTTONDOWN or event.button != SDL_BUTTON_LEFT:
        return False

    x, y = _stage_button_positions[0]
    mouse_y = game_config.SCREEN_HEIGHT - event.y
    half_width = _stage_button_width // 2
    half_height = _stage_button_height // 2
    return (
        x - half_width <= event.x <= x + half_width
        and y - half_height <= mouse_y <= y + half_height
    )


def handle_events():
    global _first_stage_button_hovered
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_MOUSEMOTION:
            x, y = _stage_button_positions[0]
            _first_stage_button_hovered = menu_ui.point_over_button(
                event,
                x,
                y,
                _stage_button_width,
                _stage_button_height,
            )
        if menu_ui.exit_button_clicked(event):
            return "character_select"
        if _is_first_stage_button_clicked(event):
            return "train_stage"
    return None


def draw():
    if (
        _stage_select_image is None
        or _stage_button_image is None
        or _exit_button_image is None
        or _exit_button_font is None
    ):
        raise RuntimeError("Stage select mode has not been initialized.")
    _stage_select_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    for x, y in _stage_button_positions:
        _stage_button_image.draw(
            x,
            y,
            _stage_button_width,
            _stage_button_height,
        )
    if _first_stage_button_hovered:
        menu_ui.draw_hover_button(
            _exit_button_image,
            _exit_button_font,
            "트레이닝 룸",
            112,
        )
    menu_ui.draw_exit_button(_exit_button_image, _exit_button_font)
