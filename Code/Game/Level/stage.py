from . import phase

#ADD GENERIC

class stage():
    def __init__(self,GAME):
        self.GAME = GAME
        self.SCRspeed = 0.2
        self.scrollON = 1
        self.phases = [phase.phase00(self.GAME)]
        #self.phases = [ phase1(self.GAME), end(self.GAME)]
        self.logic()

    def update(self):
        self.logic()

    def scrollspeed(self):
        return self.scrollON * self.SCRspeed
        #return math.sin(self.step/20)**2

    def logic(self):
        if (self.phases[0].update()):
            self.phases.pop(0)
        #pass
        #if len(self.GAME.units) < 6 and self.cooldown < 1:
            #if self.state:
            #    e = enemy.enemy0(self.GAME, patterns.movePattern0 )
            #else:
            #    e = enemy.enemy0(self.GAME, patterns.movePattern1)
            #self.state = not self.stat
            #self.cooldown = 10
            #self.GAME.units.append(e)

class test(stage):
    def __init__(self,GAME):
        super().__init__(GAME)

    def logic(self):
        self.phases[0].update()

class stage0():
    def __init__(self,GAME):
        super().__init__(GAME)
        self.phases = [phase.phase0(self.GAME), phase.phase1(self.GAME), phase.end(self.GAME)]
