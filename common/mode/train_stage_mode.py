from pico2d import (
    SDLK_a,
    SDLK_d,
    SDLK_ESCAPE,
    SDLK_LEFT,
    SDLK_RIGHT,
    SDLK_DOWN,
    SDLK_s,
    SDLK_UP,
    SDLK_w,
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
_superman_crouch_image = None
_superman_jump_image = None
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
_CROUCH_FRAME_X_BOUNDS = (
    (0, 182, 347, 511, 671, 834, 1024),
    (0, 186, 347, 504, 667, 829, 1024),
)
_JUMP_FRAME_X_BOUNDS = (
    (0, 183, 356, 526, 682, 845, 1024),
    (0, 184, 348, 517, 680, 846, 1024),
)
_CROUCH_FRAME_SEQUENCE = (0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11)
# The eighth crouch cell contains part of its neighboring sprite.
_SUPERMAN_START_X = 180
_SUPERMAN_P2_START_X = game_config.SCREEN_WIDTH - _SUPERMAN_START_X
_SUPERMAN_Y = 305
_SUPERMAN_HEIGHT = 400
_SUPERMAN_MOVE_SPEED = 240
_JUMP_LANDING_FRAME_COUNT = 2
_JUMP_FLIGHT_FRAME_COUNT = (
    _FRAME_COLUMNS * _FRAME_ROWS - _JUMP_LANDING_FRAME_COUNT
)
_JUMP_FLIGHT_DURATION = _JUMP_FLIGHT_FRAME_COUNT / _FRAMES_PER_SECOND
_JUMP_DURATION = _FRAME_COLUMNS * _FRAME_ROWS / _FRAMES_PER_SECOND
_JUMP_HEIGHT = 180
_JUMP_INITIAL_VELOCITY = 4 * _JUMP_HEIGHT / _JUMP_FLIGHT_DURATION
_GRAVITY = 8 * _JUMP_HEIGHT / (_JUMP_FLIGHT_DURATION ** 2)
_SUPERMAN_X_MIN = 150
_SUPERMAN_X_MAX = game_config.SCREEN_WIDTH - _SUPERMAN_X_MIN
_HEALTH_BAR_WIDTH = 560
_HEALTH_BAR_HEIGHT = 187
_HEALTH_BAR_Y = 595
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
_player1_jump_started_at = None
_player2_jump_started_at = None
_player1_crouch_started_at = None
_player2_crouch_started_at = None
_last_update_time = 0.0


def init():
    global _stage_image, _superman_idle_image
    global _superman_front_image, _superman_back_image
    global _superman_crouch_image, _superman_jump_image
    global _health_bar_image
    global _name_button_image, _name_button_font
    global _superman_x, _superman_p2_x, _last_update_time
    global _player1_jump_started_at, _player2_jump_started_at
    global _player1_crouch_started_at, _player2_crouch_started_at
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
        _superman_crouch_image = load_image(str(character_dir / "superman_crouch.png"))
        _superman_jump_image = load_image(str(character_dir / "superman_jump.png"))
    else:
        _superman_idle_image = None
        _superman_front_image = None
        _superman_back_image = None
        _superman_crouch_image = None
        _superman_jump_image = None
    _pressed_keys.clear()
    _superman_x = _SUPERMAN_START_X
    _superman_p2_x = _SUPERMAN_P2_START_X
    _player1_jump_started_at = None
    _player2_jump_started_at = None
    _player1_crouch_started_at = None
    _player2_crouch_started_at = None
    _last_update_time = get_time()
    _name_button_image, _name_button_font = menu_ui.load_exit_button_assets()


def finish():
    global _stage_image, _superman_idle_image
    global _superman_front_image, _superman_back_image
    global _superman_crouch_image, _superman_jump_image
    global _health_bar_image
    global _name_button_image, _name_button_font
    _stage_image = None
    _superman_idle_image = None
    _superman_front_image = None
    _superman_back_image = None
    _superman_crouch_image = None
    _superman_jump_image = None
    _health_bar_image = None
    _name_button_image = None
    _name_button_font = None
    _pressed_keys.clear()


def handle_events():
    global _superman_x, _superman_p2_x, _last_update_time
    global _player1_jump_started_at, _player2_jump_started_at
    global _player1_crouch_started_at, _player2_crouch_started_at
    for event in get_events():
        if event.type == SDL_QUIT:
            return "quit"
        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            return "stage_select"

        if event.type == SDL_KEYDOWN and event.key in (
            SDLK_a,
            SDLK_d,
            SDLK_s,
            SDLK_w,
            SDLK_LEFT,
            SDLK_RIGHT,
            SDLK_DOWN,
            SDLK_UP,
        ):
            is_new_press = event.key not in _pressed_keys
            _pressed_keys.add(event.key)
            if is_new_press:
                key_time = get_time()
                if event.key == SDLK_s:
                    _player1_crouch_started_at = key_time
                elif event.key == SDLK_DOWN:
                    _player2_crouch_started_at = key_time
                elif event.key == SDLK_w and game_state.player1_character == "superman":
                    if (
                        _player1_jump_started_at is None
                        or key_time - _player1_jump_started_at >= _JUMP_DURATION
                    ):
                        _player1_jump_started_at = key_time
                elif event.key == SDLK_UP and game_state.player2_character == "superman":
                    if (
                        _player2_jump_started_at is None
                        or key_time - _player2_jump_started_at >= _JUMP_DURATION
                    ):
                        _player2_jump_started_at = key_time
        elif event.type == SDL_KEYUP and event.key in (
            SDLK_a,
            SDLK_d,
            SDLK_s,
            SDLK_w,
            SDLK_LEFT,
            SDLK_RIGHT,
            SDLK_DOWN,
            SDLK_UP,
        ):
            _pressed_keys.discard(event.key)
            if event.key == SDLK_s:
                _player1_crouch_started_at = None
            elif event.key == SDLK_DOWN:
                _player2_crouch_started_at = None

    current_time = get_time()
    elapsed_time = max(0.0, current_time - _last_update_time)
    _last_update_time = current_time
    player1_jumping = _is_jump_active(_player1_jump_started_at, current_time)
    player1_direction = int(SDLK_d in _pressed_keys) - int(
        SDLK_a in _pressed_keys
    )
    if (
        game_state.player1_character == "superman"
        and not player1_jumping
        and player1_direction
    ):
        _superman_x += player1_direction * _SUPERMAN_MOVE_SPEED * elapsed_time
        _superman_x = max(
            _SUPERMAN_X_MIN,
            min(_superman_x, _SUPERMAN_X_MAX),
        )
    player2_direction = int(SDLK_RIGHT in _pressed_keys) - int(
        SDLK_LEFT in _pressed_keys
    )
    player2_jumping = _is_jump_active(_player2_jump_started_at, current_time)
    if (
        game_state.player2_character == "superman"
        and not player2_jumping
        and player2_direction
    ):
        _superman_p2_x += (
            player2_direction * _SUPERMAN_MOVE_SPEED * elapsed_time
        )
        _superman_p2_x = max(
            _SUPERMAN_X_MIN,
            min(_superman_p2_x, _SUPERMAN_X_MAX),
        )
    return None


def _is_jump_active(started_at, current_time):
    return (
        started_at is not None
        and 0 <= current_time - started_at < _JUMP_DURATION
    )


def _animation_frame(
    started_at,
    current_time,
    hold_last_frame=False,
    frame_sequence=None,
):
    frame_count = (
        len(frame_sequence)
        if frame_sequence is not None
        else _FRAME_COLUMNS * _FRAME_ROWS
    )
    frame = int(max(0.0, current_time - started_at) * _FRAMES_PER_SECOND)
    if hold_last_frame:
        frame = min(frame, frame_count - 1)
    else:
        frame %= frame_count
    if frame_sequence is not None:
        return frame_sequence[frame]
    return frame


def _jump_animation_frame(started_at, current_time):
    elapsed_time = max(0.0, current_time - started_at)
    if elapsed_time < _JUMP_FLIGHT_DURATION:
        return min(
            int(elapsed_time * _FRAMES_PER_SECOND),
            _JUMP_FLIGHT_FRAME_COUNT - 1,
        )
    landing_frame = _JUMP_FLIGHT_FRAME_COUNT + int(
        (elapsed_time - _JUMP_FLIGHT_DURATION) * _FRAMES_PER_SECOND
    )
    return min(
        landing_frame,
        _FRAME_COLUMNS * _FRAME_ROWS - 1,
    )


def _jump_offset(started_at, current_time):
    if started_at is None:
        return 0.0
    elapsed_time = min(
        _JUMP_FLIGHT_DURATION,
        max(0.0, current_time - started_at),
    )
    return max(
        0.0,
        _JUMP_INITIAL_VELOCITY * elapsed_time
        - 0.5 * _GRAVITY * elapsed_time ** 2,
    )


def _draw_sprite_frame(
    image,
    frame_bounds,
    center_x,
    flip_horizontal=False,
    frame_index=None,
    center_y=_SUPERMAN_Y,
):
    if frame_index is None:
        frame_index = int(get_time() * _FRAMES_PER_SECOND) % (
            _FRAME_COLUMNS * _FRAME_ROWS
        )
    column = frame_index % _FRAME_COLUMNS
    row = frame_index // _FRAME_COLUMNS
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
            center_y,
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
            center_y,
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
        current_time = get_time()
        center_y = _SUPERMAN_Y + _jump_offset(
            _player1_jump_started_at, current_time
        )
        if _is_jump_active(_player1_jump_started_at, current_time):
            sprite, frame_bounds = _superman_jump_image, _JUMP_FRAME_X_BOUNDS
            frame_index = _jump_animation_frame(
                _player1_jump_started_at, current_time
            )
        elif SDLK_s in _pressed_keys:
            sprite, frame_bounds = (
                _superman_crouch_image,
                _CROUCH_FRAME_X_BOUNDS,
            )
            frame_index = _animation_frame(
                _player1_crouch_started_at,
                current_time,
                hold_last_frame=True,
                frame_sequence=_CROUCH_FRAME_SEQUENCE,
            )
        elif SDLK_d in _pressed_keys and SDLK_a not in _pressed_keys:
            sprite, frame_bounds = _superman_front_image, _FRONT_FRAME_X_BOUNDS
            frame_index = None
        elif SDLK_a in _pressed_keys and SDLK_d not in _pressed_keys:
            sprite, frame_bounds = _superman_back_image, _BACK_FRAME_X_BOUNDS
            frame_index = None
        else:
            sprite, frame_bounds = _superman_idle_image, _IDLE_FRAME_X_BOUNDS
            frame_index = None
        _draw_sprite_frame(
            sprite,
            frame_bounds,
            int(_superman_x),
            frame_index=frame_index,
            center_y=center_y,
        )
    if game_state.player2_character == "superman":
        current_time = get_time()
        center_y = _SUPERMAN_Y + _jump_offset(
            _player2_jump_started_at, current_time
        )
        if _is_jump_active(_player2_jump_started_at, current_time):
            sprite, frame_bounds = _superman_jump_image, _JUMP_FRAME_X_BOUNDS
            frame_index = _jump_animation_frame(
                _player2_jump_started_at, current_time
            )
        elif SDLK_DOWN in _pressed_keys:
            sprite, frame_bounds = (
                _superman_crouch_image,
                _CROUCH_FRAME_X_BOUNDS,
            )
            frame_index = _animation_frame(
                _player2_crouch_started_at,
                current_time,
                hold_last_frame=True,
                frame_sequence=_CROUCH_FRAME_SEQUENCE,
            )
        elif SDLK_LEFT in _pressed_keys and SDLK_RIGHT not in _pressed_keys:
            sprite, frame_bounds = _superman_front_image, _FRONT_FRAME_X_BOUNDS
            frame_index = None
        elif SDLK_RIGHT in _pressed_keys and SDLK_LEFT not in _pressed_keys:
            sprite, frame_bounds = _superman_back_image, _BACK_FRAME_X_BOUNDS
            frame_index = None
        else:
            sprite, frame_bounds = _superman_idle_image, _IDLE_FRAME_X_BOUNDS
            frame_index = None
        _draw_sprite_frame(
            sprite,
            frame_bounds,
            int(_superman_p2_x),
            True,
            frame_index,
            center_y,
        )
    _draw_health_bars()
