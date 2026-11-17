from pico2d import close_canvas, open_canvas, update_canvas

import game_config
from mode import (
    character_select_mode,
    control_mode,
    game_mode,
    opening_mode,
    option_mode,
    select_mode,
    stage_select_mode,
)


_next_modes = {
    "select": select_mode,
    "game": game_mode,
    "options": option_mode,
    "character_select": character_select_mode,
    "controls": control_mode,
    "stage_select": stage_select_mode,
}


def main():
    open_canvas(game_config.SCREEN_WIDTH, game_config.SCREEN_HEIGHT)
    current_mode = opening_mode
    try:
        current_mode.init()
        while True:
            transition = current_mode.handle_events()
            if transition == "quit":
                break
            if transition in _next_modes:
                current_mode.finish()
                current_mode = _next_modes[transition]
                current_mode.init()
            current_mode.draw()
            update_canvas()
    finally:
        current_mode.finish()
        close_canvas()


if __name__ == "__main__":
    main()