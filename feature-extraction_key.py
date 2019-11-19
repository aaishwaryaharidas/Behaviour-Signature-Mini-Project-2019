import sys
from collections import defaultdict
from time import time
import pygame
from pygame.key import name as keyname
from pygame.locals import *
import logging

logging.basicConfig(filename="keyfeature_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Mapping of a key to a list of holdtimes (from which you can average, etc)
holdtimes = defaultdict(list)

# Mapping of a key pair to a list of digraph times
digraphs = defaultdict(list)

# Keys which have been pressed down, but not up yet.
pending = {}

# Last key to be de-pressed, corresponding time.
last_key = None

# Text that the user has typed so far (one sublist for every Enter pressed)
typed_text = [[]]

#Log hold time and flight time
def show_times():
    all_text = [k for line in typed_text for k in line]

    #Monographs-Hold times
    for key in all_text:
        #print ("%s: %.5f" % (key, holdtimes[key].pop(0)))
        logging.info("Key:{0}, Holdtime: {1}".format(key, holdtimes[key].pop(0)))

    #Digraphs-Flightimes
    for key1, key2 in zip(all_text, all_text[1:]):
        #print ("(%s, %s): %.5f" % (key1, key2,digraphs[(key1, key2)].pop(0)))
        logging.info("Keys:({0},{1}), Flighttime: {2}".format(key1,key2, digraphs[(key1,key2)].pop(0)))

def time_keypresses(events):
    global last_key

    for event in events:

        if event.type == KEYDOWN:

            # ESC exits the program
            if event.key == K_ESCAPE:
                show_times()
                sys.exit(0)

            t = pending[event.key] = time()
            if last_key is not None:
                if event.key != K_RETURN:
                    digraphs[(last_key[0], keyname(event.key))].append(t - last_key[1])
                last_key = None
        elif event.type == KEYUP:
            if event.key == K_RETURN:
                update_screen()
                typed_text.append([])
                pending.pop(event.key)
                last_key = None
            else:
                t = time()
                holdtimes[keyname(event.key)].append(t - pending.pop(event.key))
                last_key = [keyname(event.key), t]
                typed_text[-1].append(keyname(event.key))


def update_screen():
    global screen
    screen.fill((255, 255, 255))
    header_font = pygame.font.Font(None, 42)
    header = header_font.render("Type away! Press 'Enter' to show.", True, (0, 0, 0))
    header_rect = header.get_rect()
    header_rect.centerx = screen.get_rect().centerx
    header_rect.centery = screen.get_rect().centery - 100

    text_font = pygame.font.Font(None, 32)
    user_text = text_font.render("".join(typed_text[-1]) if typed_text[-1] else "...",
                                 True, (0, 0, 255))
    text_rect = user_text.get_rect()
    text_rect.centerx = screen.get_rect().centerx
    text_rect.centery = screen.get_rect().centery

    screen.blit(header, header_rect)
    screen.blit(user_text, text_rect)

    pygame.display.update()


if __name__ == '__main__':
    pygame.init()
    window = pygame.display.set_mode((800, 600))
    screen = pygame.display.get_surface()
    update_screen()
    show_times()
    while True:
        time_keypresses(pygame.event.get())
