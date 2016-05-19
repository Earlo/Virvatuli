import random

import pygame
#from pygame.locals import *

import json

from .Level import stage
from .Entity import charachter
#from .Mechanic import grid
from . import gameArea
from .game_constants import *

from .. import constants
#from ..Engine import events

#not sure if so good solution, but, makes thing much simpler.
from ..Engine import graphicalAssetHandler

#from multiprocessing import Queue
#import Queue

# example of a really boring game

#def startGame( FromEngine,ToEngine ):
#    GAME = game( FromEngine, ToEngine )
#    GAME.game_loop()

def startGame( conn ):
    #pygame.init()
    GAME = game( conn )
    GAME.game_loop()

class game():
    #def __init__(self, FromEngine,ToEngine,save = None):
    def __init__(self, ENGINECONNECTION,save = None):
        #self.PROGRAM = PROGRAM
        self.EC = ENGINECONNECTION
        
        self.clock = pygame.time.Clock()


        #self.FromEngine = FromEngine
        #self.ToEngine = ToEngine

        self.done = False
        self.units = []
        self.ammo = []
        self.effects = []

        self.keys = []

        #self.GHandle = graphicalAssetHandler.graphicalDict()

        with open('result.json') as data_file:    
            self.GHandle = json.load(data_file)
        print( self.GHandle)
        #if save == None:
        self.start_game()

    def game_loop(self):
        print("STARTING GAMELAOE")
        #last = 0
        #while not self.PROGRAM.done:
        while not self.done:
            ret = dict()
            #self.t = [0,0,0,0]
            #s = pygame.time.get_ticks()
            while (self.EC.poll() ):
                self.message = self.EC.recv()
                #print(self.EC.poll())
                #print( self.message["T"] - pygame.time.get_ticks(),pygame.time.get_ticks() )
                try:
                    self.keys = self.message["KEY"]
                except KeyError:
                    pass
                try:
                    if (self.message['END']):
                        print( "THEGAME,",self.message["END"] )
                        self.done = True
                        ret["END"] = True
                        break
                except KeyError:
                    pass
            #print ( "poll ", pygame.time.get_ticks() - s)
            
            #s = pygame.time.get_ticks()
            
            #TODO better solution for giving the things to draw
            drawres = dict()
            self.AREA.update()
            self.stage.update()
            drawres["BGR"] = dict()
            drawres["SPRITE"] = dict()
            drawres["PORTRAIT"] = dict()
            drawres["POLY"] = []

            drawres["BGR"][self.AREA.sprite] =  [(0, self.AREA.scroll)]
            if (not self.AREA.oldsprite == ""):
                try:
                    drawres["BGR"][self.AREA.oldsprite].append( (0, self.AREA.oldscroll) )
                except KeyError:
                    drawres["BGR"][self.AREA.oldsprite] =  [(0, self.AREA.oldscroll)]
            for e in self.effects:
                e.update()
                try:
                    drawres[e.imagetype][e.sprite].append( e.topleft )
                except KeyError:
                    drawres[e.imagetype][e.sprite] = [ e.topleft ]
            for u in self.units:
                u.update()
                try:
                    drawres[u.imagetype][u.sprite].append( u.topleft )
                except KeyError:
                    drawres[u.imagetype][u.sprite] = [ u.topleft ]
            for a in self.ammo:
                a.update()
                try:
                    drawres[a.imagetype][a.sprite].append( a.topleft )
                except KeyError:
                    drawres[a.imagetype][a.sprite] = [ a.topleft ]
            
            #TODO FIX THIS ASDASDASDAS so ugly
            #print
            if (len(self.char.CIRCLE.drawPoints) > 0):
                for points in  self.char.CIRCLE.drawPoints:
                    #pygame.draw.polygon(self.GAME.PROGRAM.surf_EFFECT, (20,20,200), points, 5)
                    drawres["POLY"].append( ( (20  ,20  ,200), points, 5 ) )
                    drawres["POLY"].append( ( (100,100,255), points, 3 ) )
                    drawres["POLY"].append( ( (200,200,255), points, 1 ) )

            #print ( "sim ", pygame.time.get_ticks() - s)

            ret["GFX"] = drawres
            #print(ret)

            #self.clock.tick(100)       
            #print(self.t)
            #self.ToEngine.put( ret )
            
            self.EC.send( ret )
            
            #t = pygame.time.get_ticks()
            #print( t - last )
            #last = t
        self.EC.join()

        print("LoopdDOne")
    def start_game(self):
        self.AREA = gameArea.gameArea( self )

        self.char = charachter.charachter(self)
        self.units.append(self.char)

        self.stage = stage.test(self)
        #self.stage = stage.stage0(self)
    def end_game(self):
        print("end")
        pass

