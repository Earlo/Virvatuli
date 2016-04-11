import random

import pygame
from pygame.locals import *

from .Level import stage
from .Entity import charachter
from .Mechanic import grid
from .game_constants import *

from .. import constants
#from ..Engine import events


##example of a really boring game

def startGame( conn ):
    GAME = game()
class game():
    def __init__(self,PROGRAM, save = None):
        self.PROGRAM = PROGRAM

        self.units = []
        self.ammo = []
        self.effects = []

        if save == None:
            self.start_game()

    def game_step(self):
        #last = pygame.time.get_ticks()
        self.AREA.update()
        self.stage.update()
        for e in self.effects:
            e.update()
        for u in self.units:
            u.update()
        for a in self.ammo:
            a.update()

        #t = pygame.time.get_ticks()
        #print( t - last )

    def game_loop(self):
        #last = 0
        while not self.PROGRAM.done:
            self.AREA.update()
            self.stage.update()
            for e in self.effects:
                e.update()
            for u in self.units:
                u.update()
            for a in self.ammo:
                a.update()
            #t = pygame.time.get_ticks()
            #print( t - last )
            #last = t

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

        super().__init__( (0, 0), (constants.GWIDTH, constants.GHEIGTH) )
#        self.rect = self.surf().get_rect()

        self.oldsprite = ""

        self.grid = grid.grid( self.size, 32 )
        self.scroll = +self.h-self.surf().get_height()

    def oldsurf(self):
        return self.GAME.PROGRAM.GHandle["BGR"][self.oldsprite]

    def surf(self):
        return self.GAME.PROGRAM.GHandle["BGR"][self.sprite]

    def update(self):
        t = pygame.time.get_ticks()
        self.timeInterval = t - self.lastUpdated
        self.lastUpdated = t

        scrollAdd = self.GAME.stage.scrollspeed() * self.timeInterval
        if (self.scroll > 0):
            self.oldscroll = self.scroll
            self.scroll = -self.surf().get_height()
            self.oldsprite = self.sprite
            #self.surf = self.nextsurf
        elif not self.oldsprite == "":
            if self.oldscroll > self.surf().get_height():
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
