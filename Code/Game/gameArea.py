import pygame


from .Mechanic import grid
from .. import constants

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
