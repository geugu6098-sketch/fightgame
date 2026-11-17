from pico2d import (
    SDLK_a,
    SDLK_d,
    SDL_KEYDOWN,
    SDL_KEYUP,
    SDL_QUIT,
    get_events,
    get_time,
    load_image,
)

import game_config
import game_state
import menu_ui


_stage_image = None
_superman_idle_image = None
_superman_front_image = None
_superman_back_image = None
_exit_button_image = None
_exit_button_font = None

_FRAME_COLUMNS = 6
_FRAME_ROWS = 2
_FRAMES_PER_SECOND = 8
_IDLE_FRAME_X_BOUNDS = (
    (0, 182, 347, 510, 680, 831, 1024),
    (0, 184, 360, 516, 678, 846, 1024),
)
_FRONT_FRAME_X_BOUNDS = (
    (0, 174, 342, 508, 676, 835, 1024),
    (0, 178, 339, 506, 668, 828, 1024),
)
_BACK_FRAME_X_BOUNDS = (
    (0, 252, 475, 698, 916, 1129, 1376),
    (0, 243, 464, 682, 919, 1125, 1376),
)
_SUPERMAN_START_X = 180
_SUPERMAN_Y = 305
_SUPERMAN_HEIGHT = 400
_SUPERMAN_MOVE_SPEED = 240
_SUPERMAN_X_MIN = 150
_SUPERMAN_X_MAX = game_config.SCREEN_WIDTH - _SUPERMAN_X_MIN
_pressed_keys = set()
_superman_x = _SUPERMAN_START_X
_last_update_time = 0.0


def init():
    global _stage_image, _superman_idle_image
    global _superman_front_image, _superman_back_image
    global _exit_button_image, _exit_button_font
    global _superman_x, _last_update_time
    image_path = game_config.RESOURCE_DIR / "stage" / "train_stage.png"
    _stage_image = load_image(str(image_path))
    if game_state.selected_character == "superman":
        character_dir = game_config.RESOURCE_DIR / "character" / "superman"
        _superman_idle_image = load_image(str(character_dir / "superman_idle.png"))
        _superman_front_image = load_image(str(character_dir / "superman_front.png"))
        _superman_back_image = load_image(str(character_dir / "superman_back.png"))
    else:
        _superman_idle_image = None
        _superman_front_image = None
        _superman_back_image = None
    _pressed_keys.clear()
    _superman_x = _SUPERMAN_START_X
    _last_update_time = get_time()
    _exit_button_image, _exit_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _stage_image, _superman_idle_image
    global _superman_front_image, _superman_back_image
    global _exit_button_image, _exit_button_font
    _stage_image = None
    _superman_idle_image = None
    _superman_front_image = None
    _superman_back_image = None
    _exit_button_image = None
    _exit_button_font = None
    _pressed_keys.clear()


def handle_events():
    global _superman_x, _last_update_time
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if menu_ui.exit_button_clicked(event):
            return "stage_select"

        if event.type == SDL_KEYDOWN and event.key in (SDLK_a, SDLK_d):
            _pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP and event.key in (SDLK_a, SDLK_d):
            _pressed_keys.discard(event.key)

    current_time = get_time()
    elapsed_time = max(0.0, current_time - _last_update_time)
    _last_update_time = current_time
    movement_direction = int(SDLK_d in _pressed_keys) - int(
        SDLK_a in _pressed_keys
    )
    if _superman_idle_image is not None and movement_direction:
        _superman_x += movement_direction * _SUPERMAN_MOVE_SPEED * elapsed_time
        _superman_x = max(
            _SUPERMAN_X_MIN,
            min(_superman_x, _SUPERMAN_X_MAX),
        )
    return None


def _draw_sprite_frame(image, frame_bounds):
    frame = int(get_time() * _FRAMES_PER_SECOND) % (
        _FRAME_COLUMNS * _FRAME_ROWS
    )
    column = frame % _FRAME_COLUMNS
    row = frame // _FRAME_COLUMNS
    frame_left, frame_right = frame_bounds[row][column : column + 2]
    frame_width = frame_right - frame_left
    frame_height = image.h // _FRAME_ROWS
    frame_bottom = image.h - (row + 1) * frame_height
    draw_width = frame_width * _SUPERMAN_HEIGHT // frame_height
    image.clip_draw(
        frame_left,
        frame_bottom,
        frame_width,
        frame_height,
        int(_superman_x),
        _SUPERMAN_Y,
        draw_width,
        _SUPERMAN_HEIGHT,
    )


def draw():
    if _stage_image is None or _exit_button_image is None or _exit_button_font is None:
        raise RuntimeError("Train stage mode has not been initialized.")
    _stage_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    if _superman_idle_image is not None:
        if SDLK_d in _pressed_keys and SDLK_a not in _pressed_keys:
            sprite, frame_bounds = _superman_front_image, _FRONT_FRAME_X_BOUNDS
        elif SDLK_a in _pressed_keys and SDLK_d not in _pressed_keys:
            sprite, frame_bounds = _superman_back_image, _BACK_FRAME_X_BOUNDS
        else:
            sprite, frame_bounds = _superman_idle_image, _IDLE_FRAME_X_BOUNDS
        _draw_sprite_frame(sprite, frame_bounds)
    menu_ui.draw_exit_button(_exit_button_image, _exit_button_font)
