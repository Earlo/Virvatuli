
import sys
import os
import time

import threading

#!TEST
#from multiprocessing import Process
from multiprocessing import Process, Pipe

import pygame
from pygame.locals import *

from . import window
from . import localization

from ..Game.game import game

from ..constants import *

class engine(window.window_handler):
    def __init__(self):
        super().__init__() #initialize window handler

        self.FPS = 100 #silky smooth 100 frames per second

        self.mouse = [pygame.mouse.get_pos() , False ,  [0,0] , None ]
        self.clock = pygame.time.Clock()
        self.additional_tasks = []
        self.function = nothing
        self.done = False
        self.active_text_field = None
        self.active_drag_obj = None

        self.GAME = None

        self.language = getattr(localization, LANGUAGE)()

    def m_loop(self):
        while not self.done:
            self.mouse[0] = pygame.mouse.get_pos()
            self.mouse[1] = False
            #pygame.event.pump()#
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # Closed from X
                    self.done = True # Stop the Loop
                elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                    #print (event.pos)
                    if event.button == 1: #TODO make mousehandler later, seriosly
                        self.mouse[1] = True
                        for obj in self.GUI:#check if any in game buttons are pressed
                            obj.pressed(self,event) #self.mouse[0]
                    if event.type == pygame.MOUSEBUTTONUP:
                        self.active_drag_obj = None
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if not self.active_text_field == None:
                            self.active_text_field.inactivate()
                            self.active_text_field = None
                elif event.type == pygame.MOUSEMOTION:
                    if not self.active_drag_obj == None:
                        self.active_drag_obj.dragged(event)
                elif event.type == pygame.KEYDOWN:
                    if not self.active_text_field == None:
                        self.active_text_field.update(event)
                elif event.type == pygame.VIDEORESIZE: #or event.type == pygame.FULLSCREEN:
                   self.rezise_request(event)
                #elif event.type == update_screen_event:
                #    self.add_update(event)
                elif event.type == function_call_event:
                    self.OTfunction_wrapper(event)

            #self.update_display()

            self.function()

            self.clock.tick(self.FPS)
            #self.clock.tick( )
            #try:
            pygame.display.set_caption("FPS: %i" % self.clock.get_fps())
            #except OverflowError:
            #    pygame.display.set_caption("FPS: Quite a lot")



    def STARTGAME(self):
        #self.GAME = game(self)
        #self.GUI = []
        #self.GUI = self.GAME.game_gui()

        pattern_conn, child_conn = Pipe()
        p = Process(target=self.GAME.game_loop, args =(child_conn,) )
        #p.start()
        #p.join()
        #self.function = self.drawGame
        #threading.Thread(target=self.GAME.game_loop).start()
        #threading.Thread(target=self.drawloop).start()

        #self.function = self.geamloap

    def geamloap(self):
        self.GAME.game_step()
        self.drawGame()

    def OTfunction_wrapper(self,e):
        e.func( *e.param )


def start():
    pygame.init()
    pygame.display.init()
    pygame.font.init()

    global PROGRAM
    PROGRAM = engine()
    PROGRAM.m_loop()
    pygame.quit()
