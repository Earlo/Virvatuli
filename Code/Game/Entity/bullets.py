
from . import unit
from . import effect


from . import pattern
class goStraight(pattern.pattern):
    def __init__(self, owner, vec):
        super().__init__( owner )
        self.vec = vec

    def iterate( self ):
        super().iterate( self.vec )

#Generic
class bullet(unit.unit):
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time)
        #self.FLAGS.append("HARMFUL")
        self.damage = 1

    def update(self):
        super().update()
        self.collision()


    def deathevent(self):
        if self.FLAGS["DEAD"]:
            self.user.GAME.effects.append( effect.blasthit( self.GAME, self.center, self.lastUpdated ))

    def remove(self):
        self.deathevent()
        self.GAME.ammo.remove(self)
        self.resetTiles()

    def deathConditions(self):
        #print(self.drawableRect())
        return len(self.tiles) == 0 or self.FLAGS["DEAD"]

    def hit(self, other):
        other.hit( self )
        self.FLAGS["DEAD"] = True
        #bullet.hit()

class blast(bullet):
    sprites = ["player_shot1",
                "enemy_shot1"]
    def __init__(self, user, vec, time):
        #super().__init__(user.GAME, (user.x,user.y), sprite = self.sprites[s])
        super().__init__(user.GAME, user.center, time)
        self.hasHit = False
        self.user = user
        user.GAME.ammo.append(self)
        self.speed = 0.5
        self.pattern = goStraight( self, vec )

    #def hit(self):
    #    self.hasHit = True

class blade(bullet):
    sprites = ["churiken_1",
               "churiken_2",
               "churiken_3",
               "churiken_4",
               "churiken_5"]
    def __init__(self, user, vec, pos, time):
        super().__init__(user.GAME, pos, time)
        self.damage = 10
        self.hasHit = False
        self.user = user
        user.GAME.ammo.append(self)
        self.speed = 0.5
        self.pattern = goStraight( self, vec )

        self.animationSpeed = 25
        self.animationlen = len(self.sprites) * self.animationSpeed
        self.frame = 0
    def update(self):
        ##don't be a fucking idiot
        f = (self.lastUpdated % self.animationlen) // self.animationSpeed
        if self.frame != f:
            self.frame = f
            self.sprite = self.sprites[ self.frame ]
        super().update()

    def deathConditions(self):
        #print(self.drawableRect())
        return self.drawableRect().size == (0,0)
        #return self.GAME.AREA.isOut(self,0,0)

