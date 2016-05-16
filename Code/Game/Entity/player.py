
#import pygame
from pygame.locals import *

from . import pattern


class player(pattern.pattern):
    def __init__(self, owner):
        super().__init__(owner)

    def iterate(self):
        keys = self.owner.GAME.keys
        dx,dy = 0,0
        self.owner.change = self.owner.speed * self.owner.timeInterval

        if keys[K_UP]: dy-= self.owner.change
        if keys[K_DOWN]: dy+= self.owner.change
        if keys[K_LEFT]: dx-= self.owner.change
        if keys[K_RIGHT]: dx+= self.owner.change
        #print(self.owner.y)
        #self.owner.oldpos.append(self.owner.pos())
        #dx,dy = self.owner.GAME.AREA.checkBorders(self.owner,dx,dy)

        self.owner.floatpos = self.fixFloatpos( self.owner.floatpos[0] + dx, self.owner.floatpos[1] + dy )


        self.owner.center = self.owner.floatpos
        #super().iterate( (0,0) )

        #print(self.floatpos, self.owner.center)

        if (not self.owner.DEAD):
            if keys[K_z]:self.owner.weapon.update()

            if keys[K_c] and self.owner.adhockeyrepeat:
               self.owner.adhockeyrepeat = False
               self.owner.placeBeacon()

            if keys[K_SPACE]:self.owner.castaSpell()

            if keys[K_q] and self.owner.adhockeyrepeat:
                self.owner.adhockeyrepeat = False
                #print(self.owner, self.owner )
                print( len( self.owner.GAME.units ), len( self.owner.GAME.ammo ), len( self.owner.GAME.effects ) )
                print( self.owner.GAME.clock.get_fps() ) 
                #print( len( self.owner.GAME.ammo ) )

            if not keys[K_c] and not keys[K_q]:
                self.owner.adhockeyrepeat = True

    def fixFloatpos(self, f0, f1):

        minw = self.owner.w / 2
        minh = self.owner.h / 2

        ux = f0 - minw
        uy = f1 - minh
        dx = f0 + minw
        dy = f1 + minh

        fx = f0
        fy = f1

        if ux < 0:
            fx = minw
        elif dx > self.owner.GAME.AREA.w:
            fx = self.owner.GAME.AREA.w - minw

        if uy < 0:
            fy = minh
        elif dy > self.owner.GAME.AREA.h:
            fy = self.owner.GAME.AREA.h - minh

        return (fx,fy)


