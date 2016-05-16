import random

import pygame
#from pygame.locals import *

import json

from .Level import stage
from .Entity import charachter
from .Mechanic import grid
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
            self.t = [0,0,0,0]
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
            drawres = dict()
            self.AREA.update()
            self.stage.update()
            drawres["BGR"] = dict()
            drawres["SPRITE"] = dict()
            drawres["PORTRAIT"] = dict()

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

            #print ( "sim ", pygame.time.get_ticks() - s)

            ret["GFX"] = drawres
            #print(ret)

            #self.clock.tick(100)       
            print(self.t)
            #self.ToEngine.put( ret )
            
            self.EC.send( ret )
            
            #t = pygame.time.get_ticks()
            #print( t - last )
            #last = t
        self.EC.join()

        print("LoopdDOne")
    def start_game(self):
        self.AREA = gameArea( self )

        self.char = charachter.charachter(self)
        self.units.append(self.char)

        self.stage = stage.test(self)
        #self.stage = stage.stage0(self)
    def end_game(self):
        print("end")
        pass

#class gameArea():
class gameArea( pygame.Rect ):
    sprites = [ "BGR_1",
                "DEBUG",
                "BGR_4"]
    def __init__(self, GAME):
        self.GAME = GAME
        self.content = []

        self.lastUpdated = pygame.time.get_ticks()
        self.timeInterval = 0

        self.sprite = self.sprites[1]

        #not sure if needed as a rect. investigate TODO
        super().__init__( (0, 0), (constants.GWIDTH, constants.GHEIGTH) )
#        self.rect = self.surf().get_rect()

        self.oldsprite = ""

        self.grid = grid.grid( self.size, 32 )

        #self.scroll = 0
        self.scroll = +self.h-self.gData()["rect"][1]

    #def oldsurf(self):
    #    return self.GAME.GHandle["BGR"][self.oldsprite]

    def gData(self):
       return self.GAME.GHandle["BGR"][self.sprite]

    def update(self):
        t = pygame.time.get_ticks()
        self.timeInterval = t - self.lastUpdated
        self.lastUpdated = t
        scrollAdd = self.GAME.stage.scrollspeed() * self.timeInterval
        if (self.scroll > 0):
            self.oldscroll = self.scroll
            self.scroll = -self.gData()["rect"][1]
            self.oldsprite = self.sprite
            #self.surf = self.nextsurf
        elif not self.oldsprite == "":
            if self.oldscroll > self.gData()["rect"][1]:
                self.oldsprite = ""
            else:
                pos = [0, self.scroll]
                pos[1] += self.oldscroll
            self.oldscroll += scrollAdd
        self.scroll += scrollAdd

    #def checkBorders(self,unit,dx,dy):
    #    if self.checkX( unit, dx):
    #        dx = 0
    #    if self.checkY( unit, dy):
    #        dy = 0
    #    return dx, dy

    #def checkX(self, unit, dx):
    #    return ( (unit.x - unit.rect.w/2 + dx < 0) or (unit.x + unit.rect.w/2 + dx > self.rect.w) )

    #def checkY(self, unit, dy):
    #    return ( (unit.y - unit.rect.h/2 + dy < 0) or (unit.y + unit.rect.h/2 + dy > self.rect.h) )

    #def isOut(self, unit, dy, dx):
    #    return self.checkX(unit, dx) or self.checkY(unit, dy)



#def XtoYinZ(x,y,z,step):
#    return(x + y - (step - z) )
