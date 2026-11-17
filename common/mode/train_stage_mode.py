from pico2d import (
    SDLK_a,
    SDLK_d,
    SDLK_ESCAPE,
    SDLK_LEFT,
    SDLK_RIGHT,
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
_health_bar_image = None
_name_button_image = None
_name_button_font = None

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
_SUPERMAN_P2_START_X = game_config.SCREEN_WIDTH - _SUPERMAN_START_X
_SUPERMAN_Y = 305
_SUPERMAN_HEIGHT = 400
_SUPERMAN_MOVE_SPEED = 240
_SUPERMAN_X_MIN = 150
_SUPERMAN_X_MAX = game_config.SCREEN_WIDTH - _SUPERMAN_X_MIN
_HEALTH_BAR_WIDTH = 560
_HEALTH_BAR_HEIGHT = 187
_HEALTH_BAR_Y = 580
_HEALTH_BAR_PLAYERS = (
    (350, 1, False),
    (930, 2, True),
)
_NAME_BUTTON_WIDTH = 160
_NAME_BUTTON_HEIGHT = 48
_NAME_BUTTON_Y = 687
_CHARACTER_LABELS = {"superman": ("슈퍼맨", 60)}
_DEFAULT_CHARACTER_LABEL = ("상대", 40)
_pressed_keys = set()
_superman_x = _SUPERMAN_START_X
_superman_p2_x = _SUPERMAN_P2_START_X
_last_update_time = 0.0


def init():
    global _stage_image, _superman_idle_image
    global _superman_front_image, _superman_back_image
    global _health_bar_image
    global _name_button_image, _name_button_font
    global _superman_x, _superman_p2_x, _last_update_time
    image_path = game_config.RESOURCE_DIR / "stage" / "train_stage.png"
    _stage_image = load_image(str(image_path))
    health_bar_path = game_config.RESOURCE_DIR / "screen" / "health_bar.png"
    _health_bar_image = load_image(str(health_bar_path))
    selected_characters = (
        game_state.player1_character,
        game_state.player2_character,
    )
    if "superman" in selected_characters:
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
    _superman_p2_x = _SUPERMAN_P2_START_X
    _last_update_time = get_time()
    _name_button_image, _name_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _stage_image, _superman_idle_image
    global _superman_front_image, _superman_back_image
    global _health_bar_image
    global _name_button_image, _name_button_font
    _stage_image = None
    _superman_idle_image = None
    _superman_front_image = None
    _superman_back_image = None
    _health_bar_image = None
    _name_button_image = None
    _name_button_font = None
    _pressed_keys.clear()


def handle_events():
    global _superman_x, _superman_p2_x, _last_update_time
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return "stage_select"

        if event.type == SDL_KEYDOWN and event.key in (
            SDLK_a,
            SDLK_d,
            SDLK_LEFT,
            SDLK_RIGHT,
        ):
            _pressed_keys.add(event.key)
        elif event.type == SDL_KEYUP and event.key in (
            SDLK_a,
            SDLK_d,
            SDLK_LEFT,
            SDLK_RIGHT,
        ):
            _pressed_keys.discard(event.key)

    current_time = get_time()
    elapsed_time = max(0.0, current_time - _last_update_time)
    _last_update_time = current_time
    player1_direction = int(SDLK_d in _pressed_keys) - int(
        SDLK_a in _pressed_keys
    )
    if game_state.player1_character == "superman" and player1_direction:
        _superman_x += player1_direction * _SUPERMAN_MOVE_SPEED * elapsed_time
        _superman_x = max(
            _SUPERMAN_X_MIN,
            min(_superman_x, _SUPERMAN_X_MAX),
        )
    player2_direction = int(SDLK_RIGHT in _pressed_keys) - int(
        SDLK_LEFT in _pressed_keys
    )
    if game_state.player2_character == "superman" and player2_direction:
        _superman_p2_x += (
            player2_direction * _SUPERMAN_MOVE_SPEED * elapsed_time
        )
        _superman_p2_x = max(
            _SUPERMAN_X_MIN,
            min(_superman_p2_x, _SUPERMAN_X_MAX),
        )
    return None


def _draw_sprite_frame(image, frame_bounds, center_x, flip_horizontal=False):
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
    if flip_horizontal:
        image.clip_composite_draw(
            frame_left,
            frame_bottom,
            frame_width,
            frame_height,
            0,
            "h",
            center_x,
            _SUPERMAN_Y,
            draw_width,
            _SUPERMAN_HEIGHT,
        )
    else:
        image.clip_draw(
            frame_left,
            frame_bottom,
            frame_width,
            frame_height,
            center_x,
            _SUPERMAN_Y,
            draw_width,
            _SUPERMAN_HEIGHT,
        )


def _draw_health_bars():
    players = (
        game_state.player1_character,
        game_state.player2_character,
    )
    for center_x, player_number, mirrored in _HEALTH_BAR_PLAYERS:
        if mirrored:
            _health_bar_image.composite_draw(
                0,
                "h",
                center_x,
                _HEALTH_BAR_Y,
                _HEALTH_BAR_WIDTH,
                _HEALTH_BAR_HEIGHT,
            )
        else:
            _health_bar_image.draw(
                center_x,
                _HEALTH_BAR_Y,
                _HEALTH_BAR_WIDTH,
                _HEALTH_BAR_HEIGHT,
            )
        character_name, label_width = _CHARACTER_LABELS.get(
            players[player_number - 1],
            _DEFAULT_CHARACTER_LABEL,
        )
        _name_button_image.draw(
            center_x,
            _NAME_BUTTON_Y,
            _NAME_BUTTON_WIDTH,
            _NAME_BUTTON_HEIGHT,
        )
        _name_button_font.draw(
            center_x - label_width // 2,
            _NAME_BUTTON_Y,
            character_name,
            (255, 255, 255),
        )


def draw():
    if (
        _stage_image is None
        or _health_bar_image is None
        or _name_button_image is None
        or _name_button_font is None
    ):
        raise RuntimeError("Train stage mode has not been initialized.")
    _stage_image.draw(
        game_config.SCREEN_WIDTH // 2,
        game_config.SCREEN_HEIGHT // 2,
        game_config.SCREEN_WIDTH,
        game_config.SCREEN_HEIGHT,
    )
    if game_state.player1_character == "superman":
        if SDLK_d in _pressed_keys and SDLK_a not in _pressed_keys:
            sprite, frame_bounds = _superman_front_image, _FRONT_FRAME_X_BOUNDS
        elif SDLK_a in _pressed_keys and SDLK_d not in _pressed_keys:
            sprite, frame_bounds = _superman_back_image, _BACK_FRAME_X_BOUNDS
        else:
            sprite, frame_bounds = _superman_idle_image, _IDLE_FRAME_X_BOUNDS
        _draw_sprite_frame(sprite, frame_bounds, int(_superman_x))
    if game_state.player2_character == "superman":
        if SDLK_LEFT in _pressed_keys and SDLK_RIGHT not in _pressed_keys:
            sprite, frame_bounds = _superman_front_image, _FRONT_FRAME_X_BOUNDS
        elif SDLK_RIGHT in _pressed_keys and SDLK_LEFT not in _pressed_keys:
            sprite, frame_bounds = _superman_back_image, _BACK_FRAME_X_BOUNDS
        else:
            sprite, frame_bounds = _superman_idle_image, _IDLE_FRAME_X_BOUNDS
        _draw_sprite_frame(sprite, frame_bounds, int(_superman_p2_x), True)
    _draw_health_bars()
