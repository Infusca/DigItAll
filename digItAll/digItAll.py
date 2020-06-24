# dig it all. version 2.0

# ************************************ TO DO **********************************************
# 1) enemy and player collision - add noise and inability to detect
# 2) weight limit: need to empty junk, trash icon
# 3) pouch: see all finds and info blurb about them by clicking on each
# 4) 2-3 other beep signals depending on what is found

import random
import time
import math
import winsound
import pygame
from pygame import mixer
import time
# from threading import Timer
# import multitimer
pygame.init()
pygame.mixer.init()

player_beep = mixer.Sound('C:/Users/nahol/Dropbox/Code/beep.wav')
# high_tone = mixer.Sound('C:/Users/nahol/Dropbox/Code/high_tone_beep.wav')
# low_tone = mixer.Sound ('C:/Users/nahol/Dropbox/Code/low_tone_beep.wav')

WIDTH = 900
HEIGHT = 800

# set frame
frame = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Dig It All!')
clock = pygame.time.Clock()

# register shapes
background_image = pygame.image.load('grass-bg.gif')
green = (0,255,0)
white = (255,255,255)
enemy_down = pygame.image.load('enemy_down.gif')

# define game functions

def draw(x,y):
    frame.blit(background_image, (WIDTH/2,HEIGHT/2))
    frame.blit(enemy_down, (x,y))


quitGame = False

while not quitGame:

    # quits and closes game when user hits window X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    frame.fill(white)
    draw(0,0)




pygame.quit()
quit()
