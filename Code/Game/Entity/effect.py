
from . import entity

class effect(entity.entity):
    imagetype = "SPRITE"
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time)
        self.frame = self.timeleft // self.timePerFrame
        self.done = False


    def update(self):
        super().update()
        self.timeleft -= self.timeInterval
        f = self.timeleft // self.timePerFrame
        if not f == self.frame:
            if (f > 0 ):
                self.frame = f
                self.sprite = self.sprites[self.frame]
            else:
                self.done = True
        if (self.done):
            self.GAME.effects.remove(self)

class explosion(effect):
    sprites = ["explosion4",
             "explosion3",
             "explosion2",
             "explosion1"]
    timePerFrame = 30
    timeleft = timePerFrame * len(sprites)
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time)

    def update(self):
        super().update()

class blasthit(effect):
    sprites = ["player_shot2",
            "player_shot3"]
    timePerFrame = 30
    timeleft = timePerFrame * len(sprites)
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time)

    def update(self):
        super().update()



class energyTail(effect):
    def __init__(self, GAME, pos, sprite):
        self.sprites = sprite
        super().__init__(GAME, 2, pos)
        #self.surf.set_alpha(160)

    def update(self):
        super().update()
        #self.x = x
        #self.y = y

class portrait(entity.entity):
    imagetype = "PORTRAIT"
    def __init__(self, GAME, time, pos):
        super().__init__(GAME, pos)
        self.time = time
        self.timer = 0

    def update(self):
        self.timer += 1
        f = self.timer // self.time
        if not f == self.frame:
            if (f < len(self.sprites) ):
                self.frame = f
                self.sprite = self.sprites[self.frame]
            else:
                self.dead = True


class enemy1_portrait(portrait):
    sprites = ["enemy1_portrait0"]
    def __init__(self, GAME, pos):
        super().__init__(GAME, 100, pos)

    def update(self):
        super().update()
        self.surf().set_alpha(200-self.timer*2)
        dx = self.vec[0] * self.speed
        dy = self.vec[1] * self.speed
        self.x += 1
        self.y += 1
        if (self.dead):
            self.GAME.effects.remove(self)
