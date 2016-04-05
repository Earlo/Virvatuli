
from . import unit
from . import danmaku
from . import effect
from . import pattern

class enemy(unit.unit):
    def __init__(self, GAME, pos, time, pat):
        super().__init__(GAME, pos, time)
        self.pattern = pat(self)
        self.FLAGS["TANGIBLE"] = True

    def deathConditions(self):
        #print( self.isInside)
        return (self.FLAGS["DEAD"]) or ( len(self.tiles) == 0 and self.pattern.done() )


class enemy0(enemy):
    sprites = ["enemy_1_smaller"]
    def __init__(self, GAME, pos, time, pat):
        super().__init__(GAME, pos, time, pat)
        self.hp = 4
        self.speed = .25



#Update rest of the enemies /_}
class enemy1(unit.unit):
    sprites = ["eye1",
            "eye2",
            "eye_close1",
            "eye_close2"]
    def __init__(self, GAME, pos, pat):
        super().__init__(GAME, pos)

        self.side = "ENEMY"

        self.hp = 12
        self.step = 0

        self.pattern = pat(self)

        self.speed = 0.22

    def update(self):
        super().update()

        if self.step >= 150 and  self.step < 160:
            self.sprite = self.sprites[3]
        elif self.step >= 140 and self.step < 150 or self.step >= 160 and  self.step < 170:
            self.sprite = self.sprites[2]
        elif self.step % 20 == 10:
            self.sprite = self.sprites[0]
        elif self.step % 20 == 0:
            self.sprite = self.sprites[1]

        if self.step == 170:
            self.step = 0
        else:
            self.step += 1

        self.pattern.iterate()
        self.addToGrid()
        if not self.isInside:
            self.isInside = not self.GAME.AREA.isOut(self,0,0)

        self.collision()
        if (self.deathConditions()):
            self.kill()

    def deathConditions(self):
        #print(self.drawableRect())
        return (self.hp < 1) or (self.drawableRect().size == (0,0) and self.isInside)




class boss0(enemy):
    sprites = ["enemy_1_smaller",
            "enemy_1_super2",
            "enemy_1_super3",
            "enemy_1_super4",
            "enemy_1_super1"]
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time, pattern.boss0)
        self.hp = 100
        self.speed = 0.5
        self.DEAD = False

        self.danmaku = [ danmaku.roundblast ]

    def deathConditions(self):
        #print(self.drawableRect())
        return self.DEAD


class frog(enemy):
    sprites = ["frog2"]
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time, pattern.frog)

        self.side = "ALLY"


        self.isInside = True
        self.hp = 1
        self.speed = 0.25

    def deathConditions(self):
        #print(self.drawableRect())
        return self.hp < 1 or self.drawableRect().size == (0,0)

