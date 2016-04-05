
import pygame


from . import unit
from . import player
from ..Mechanic import spells
from ..Mechanic import ritual


#maybe make an additional class above unit?
class charachter(unit.unit):
    sprites = ["energy1",
               "energy2",
               "energy3"]
    def __init__(self, GAME):
        super().__init__(GAME, [280,500], pygame.time.get_ticks())

        #self.tail = [effect.energyTail(self.GAME,self.pos(),[self.sprites[2]]),
        #             effect.energyTail(self.GAME,self.pos(),[self.sprites[2]]),
        #             effect.energyTail(self.GAME,self.pos(),[self.sprites[2]]),
        #             effect.energyTail(self.GAME,self.pos(),[self.sprites[2]]),
        #             effect.energyTail(self.GAME,self.pos(),[self.sprites[1]]),
        #             effect.energyTail(self.GAME,self.pos(),[self.sprites[1]]),
        #             effect.energyTail(self.GAME,self.pos(),[self.sprites[1]]),
        #             effect.energyTail(self.GAME,self.pos(),[self.sprites[1]]) ]
        #self.GAME.effects.extend(self.tail)

        #self.oldpos = collections.deque([self.pos()]*70, 70)
        self.side = "ALLY"
        self.DEAD = False

        self.CIRCLE = ritual.circle()
        self.ACTIVECIRCLE = 0

        self.weapon = blaster( self )
        self.hp = 3

        self.speed = 0.3
        self.hitbox = pygame.Rect(0,0,2,2)

        self.adhockeyrepeat = True
        self.pattern = player.player( self )

        #self.hitbox = pygame.draw.circle(self.surf, (0,200,200), self.rect.center , 2, 0)


    #def update(self):
    #    super().update()

    def hit(self,bullet):
        self.hp -= 1
        bullet.hit()
        if self.hp <= 0:
            self.DEAD = True

    def castaSpell(self):
        if self.ACTIVECIRCLE == 0:
            pass
        elif self.ACTIVECIRCLE == 1:
            spells.spell1(self.GAME)
        elif self.ACTIVECIRCLE == 2:
            spells.spell2(self.GAME)
        elif self.ACTIVECIRCLE == 3:
            spells.spell3(self.GAME)
        elif self.ACTIVECIRCLE == 4:
            spells.spell4(self.GAME)

    def placeBeacon(self):
        self.GAME.effects.append( ritual.beacon( self.GAME, self.center, self.lastUpdated ) )

    def deathConditions(self):
        return self.hp <= 1

    def remove(self):
        print("geimu over")

#Make seperate file
#Make generic
#make time relative

import random

from . import bullets
from .. import vector

class blaster():
    def __init__(self, user):
        self.user = user
        self.type = bullets.blast
        #self.type = bullets.bullet
        self.shots = [ [0, 25, [ [ 0,-1], 0] ],
                       [0, 35, [ vector.uvturn(165)  ] ],
                       [0, 35, [ vector.uvturn(-165) ] ],
                       [0, 50, [ vector.uvturn(175)  ] ],
                       [0, 50, [ vector.uvturn(-175) ] ] ]

        #self.AshotParam = ( self.user, [ 0,-1], 0)
        #self.BshotParam = ( self.user, vector.uvturn(165), 0)
        #self.CshotParam = ( self.user, vector.uvturn(-165), 0)
        #self.DshotParam = ( self.user, vector.uvturn(175), 0)
        #self.EshotParam = ( self.user, vector.uvturn(-175), 0)
        #check all the steps after transisting over to time

    def update(self):

        for s in self.shots:
            s[0] += self.user.timeInterval
            shotcount = s[0] // s[1]
            if shotcount > 0:
                s[0] -= shotcount * s[1]
                for n in range(0, shotcount):
                    self.fire( s[-1], self.user.lastUpdated + s[0] - n*s[1])
                    #s[2]( self.user.lastUpdated + s[0] - n*s[1] )


        #if self.step%5 == 0:
        #    self.fire( self.AshotParam, 0.01 )
        #if self.step%4 == 0:
        #    self.fire( self.BshotParam, 0.05 )
        #    self.fire( self.CshotParam, 0.05 )
        #if self.step%3 == 0:
        #    self.fire( self.DshotParam, 0.1 )
        #    self.fire( self.EshotParam, 0.1 )

    def fire(self, t, time):
        param = t[:]
        #os = [x * spread for x in vector.uvturn( random.randint(0,360) ) ]
        b = self.type( self.user, param[0], time  )
        b.FLAGS["ENEMY"] = False
