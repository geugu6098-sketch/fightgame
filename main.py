from pico2d import close_canvas, open_canvas, update_canvas

import opening_mode


def main():
    open_canvas(opening_mode.SCREEN_WIDTH, opening_mode.SCREEN_HEIGHT)
    try:
        opening_mode.init()
        while opening_mode.handle_events():
            opening_mode.draw()
            update_canvas()
    finally:
        opening_mode.finish()
        close_canvas()


if __name__ == "__main__":
    main()