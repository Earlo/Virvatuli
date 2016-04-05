
import random
import pygame

from ..Entity import enemy
from ..Entity import pattern

#ADD GENERIC
class phase():
    asd = 5
    def __init__(self,GAME):
        self.GAME = GAME
        self.events = []
        self.firstMoment = pygame.time.get_ticks() - self.asd
        self.lastUpdated = self.firstMoment
        self.duration = 1000
    def update(self):
        t = pygame.time.get_ticks()
        self.timeInterval = t - self.lastUpdated
        self.lastUpdated = t
        for e in self.events:
            e[0] += self.timeInterval
            while e[0] >= e[1]:
                e[2]( self.lastUpdated + e[0] )
                e[0] -= e[1]

#Event structure is [ ms since last call, ms between each call, function to be called]
class phase00(phase):
    def __init__(self,GAME):
        super().__init__(GAME)
        self.events = [ [0, self.asd,self.rngSin] ]
    def update(self):
        super().update()
        return False

    def rngSin(self, time):
        #print(time, self.lastUpdated, self.lastUpdated - time)
        #r = 50 + time % 150 * (time % 2 - 1)
        #r = 200
        #pass
        r = random.randint(50,250)
        e = enemy.enemy0(self.GAME, [-128, 100+r], time, pattern.movePattern0)
        self.GAME.units.append(e)

        #self.GAME.units.append( enemy.boss0(self.GAME, [-128, 300], time) )
        #pass
        #r = random.randint(-50,50)
        #e = enemy.enemy0(self.GAME, [250+r,-128], time, pattern.movePattern2)
        #self.GAME.units.append(e)


class phase0(phase):
    def __init__(self,GAME):
        super().__init__(GAME)
        self.step = 0

        #reWrite :D
    def update(self):
        if self.step < 300:
            if self.step%10 == 0:
                e = enemy.enemy0(self.GAME, [-32, self.step ], pattern.movePattern1)
                self.GAME.units.append(e)
        elif self.step > 300 and self.step < 600:
            if self.step%20 == 0:
                e = enemy.enemy0(self.GAME, [-32, 50], pattern.movePattern0)
                self.GAME.units.append(e)
                e = enemy.enemy0(self.GAME, [self.GAME.AREA.rect.w+32, 50], pattern.movePattern0)
                e.pattern.side = -1
                self.GAME.units.append(e)
        if self.step > 550 and self.step < 800:
            if self.step%25 == 0:
                e = enemy.enemy1(self.GAME, [ (random.random()-.5 )* 100 + self.GAME.AREA.rect.w / 2 , -32], pattern.movePattern2)
                if (random.random() > 0.5):
                    e.pattern.side = -1
                self.GAME.units.append(e)
        elif self.step > 1000 and self.step < 1360:
            if self.step%10 == 0:
                e = enemy.enemy0(self.GAME, [-32, 50], pattern.movePattern3)
                self.GAME.units.append(e)
        elif self.step > 1400 and self.step < 1500:
            if self.step%10 == 0:
                e = enemy.enemy0(self.GAME, [self.GAME.AREA.rect.w+32, 50], pattern.movePattern3)
                e.pattern.side = -1
                self.GAME.units.append(e)

        if self.step > 1400 and self.step < 1600:
            if self.step%15 == 0:
                e = enemy.enemy1(self.GAME, [ (random.random()-.5 )* 100 + self.GAME.AREA.rect.w / 2 , -32], pattern.movePattern2)
                if (random.random() > 0.5):
                    e.pattern.side = -1
                self.GAME.units.append(e)
        if self.step > 1550 and self.step < 1800:
            if self.step%10 == 0:
                e = enemy.enemy0(self.GAME, [-32, 50], pattern.movePattern3)
                self.GAME.units.append(e)
                e = enemy.enemy0(self.GAME, [self.GAME.AREA.rect.w+32, 50], pattern.movePattern3)
                e.pattern.side = -1
                self.GAME.units.append(e)
        elif self.step > 2500:
            return True
        self.step += 1
        return False

class phase1():
    def __init__(self,GAME):
        self.GAME = GAME
        self.step = 0

        e = enemy.boss0(self.GAME, [ self.GAME.AREA.rect.w / 2+20 ,-32 ] )

        self.boss = e
        self.START = False
    def start(self):
        self.START = True
        self.GAME.units.append( self.boss )

    def update(self):
        if not self.START:
            self.start()

        #return self.boss.DEAD
class end():
    def __init__(self,GAME):
        self.GAME = GAME
    def update(self):
        return False
