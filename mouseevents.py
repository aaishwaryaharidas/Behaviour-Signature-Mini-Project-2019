from pynput.mouse import Listener
import logging

logging.basicConfig(filename="mouse_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')


def on_move(x, y):
    # print("Mouse moved to ({0}, {1})".format(x, y))
    logging.info("Move ({0}, {1})".format(x, y))


def on_click(x, y, button, pressed):
    if pressed:logging.info('Click ({0}, {1}) {2} {3}'.format(x, y, button,pressed))
        # print('Mouse click ({0}, {1}) {2}'.format(x, y, button))



def on_scroll(x, y, dx, dy):
    # print('Mouse scrolled at ({0}, {1})({2}, {3})'.format(x, y, dx, dy))
    logging.info('Scroll ({0}, {1})({2}, {3})'.format(x, y, dx, dy))


with Listener(on_move=on_move, on_click=on_click, on_scroll=on_scroll) as listener:
    listener.join()
