from pico2d import SDL_QUIT, get_events, load_image

import game_config
import menu_ui


_stage_image = None
_exit_button_image = None
_exit_button_font = None


def init():
    global _stage_image, _exit_button_image, _exit_button_font
    image_path = game_config.RESOURCE_DIR / "stage" / "train_stage.png"
    _stage_image = load_image(str(image_path))
    _exit_button_image, _exit_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _stage_image, _exit_button_image, _exit_button_font
    _stage_image = None
    _exit_button_image = None
    _exit_button_font = None


def handle_events():
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if menu_ui.exit_button_clicked(event):
            return "stage_select"
    return None


def draw():
    if _stage_image is None or _exit_button_image is None or _exit_button_font is None:
        raise RuntimeError("Train stage mode has not been initialized.")
    _stage_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    menu_ui.draw_exit_button(_exit_button_image, _exit_button_font)
