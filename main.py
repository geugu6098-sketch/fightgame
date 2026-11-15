from pico2d import close_canvas, open_canvas, update_canvas

import game_config
import opening_mode
import select_mode


def main():
    open_canvas(game_config.SCREEN_WIDTH, game_config.SCREEN_HEIGHT)
    current_mode = opening_mode
    try:
        current_mode.init()
        while True:
            transition = current_mode.handle_events()
            if transition == "quit":
                break
            if transition == "select":
                current_mode.finish()
                current_mode = select_mode
                current_mode.init()
            current_mode.draw()
            update_canvas()
    finally:
        current_mode.finish()
        close_canvas()


if __name__ == "__main__":
    main()