import __main__

import os

import pygame


#BASEPATH = os.path.dirname(os.path.realpath(__main__.__file__))


LANGUAGE = "english"

#SWIDTH =  800
#SHEIGTH = 600

#640*896 ?
GWIDTH = 640
GHEIGTH = 896
SWIDTH =  GWIDTH + 20
SHEIGTH = GHEIGTH + 20

FONT = "Calibri" #I know. Will change later

#millisecnds
LETTER_INPUT_HELD_DOWN_DELAY    = 100
LETTER_INPUT_HELD_DOWN_INTERWAL = 20
INPUT_BOX_ACTIVITY_INDICATOR = "|"

update_screen_event = pygame.USEREVENT + 1
function_call_event = pygame.USEREVENT + 2
MAINCHA = 0
ONETIME = 1

def nothing():
    #print ("nothing") #:D
    pass


