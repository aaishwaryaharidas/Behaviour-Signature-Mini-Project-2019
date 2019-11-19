import sys
import time
import pygame
import os
import logging

logging.basicConfig(filename="keystroke_log.txt", level=logging.DEBUG, format='%(asctime)s: %(message)s')
os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Time")
clock = pygame.time.Clock()

pygame.init()

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit(0)
            t = time.time()
        if event.type == pygame.KEYUP:
            t = time.time() - t
            t = str(t)
            t = t[:5]
            #print("You pressed key",event.key," for",t,'seconds')
            logging.info("key {0} holdtime {1} seconds'".format(chr(event.key), t))
