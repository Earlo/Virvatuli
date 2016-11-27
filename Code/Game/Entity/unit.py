
from . import effect
from . import entity
#clamp = lambda n, minn, maxn: max(min(maxn, n), minn)

class unit(entity.entity):
    imagetype = "SPRITE"
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time)
        self.FLAGS = {"DEAD":False,
                      "ENEMY":True,
                      "TANGIBLE":False}
        self.tiles = []

        self.hitbox = self.copy()

        self.addToGrid()

    def update(self):
        super().update()
        
        self.pattern.iterate()

        self.hitbox.center = self.center

        self.addToGrid()
        
        if (self.deathConditions()):
            self.remove()

    def resetTiles(self):
        for t in self.tiles:
            t.remove(self)
        self.tiles = []

    def addToGrid(self):
        self.resetTiles( )
        self.GAME.AREA.grid.add(self)

    def collision(self): #really shit code, but will do
        #pass
        #print("ASDS")
        for t in self.tiles:
            for i in t:
                if i.FLAGS["TANGIBLE"]:
                    if not (i.FLAGS["ENEMY"] == self.FLAGS["ENEMY"]):
                        if self.hitbox.colliderect(i.hitbox):
                            self.hit(i)

    def hit(self,bullet):
        self.hp -= bullet.damage
        if self.hp < 1:
            self.FLAGS["DEAD"] = True
        #bullet.hit()

    def deathevent(self):
        if self.hp < 1:
            self.GAME.effects.append( effect.explosion( self.GAME, self.center, self.lastUpdated ))

    def remove(self):
        self.deathevent()
        self.GAME.units.remove(self)
        self.resetTiles( )
        #game ares is flipped every time
        #if update:
        #    if area == None:
        #        area = self.drawableRect()
        #    else:
        #        area.move_ip((self.x,self.y)) #fix
        #    events.blit_request( area , self.surf)   #edit later
