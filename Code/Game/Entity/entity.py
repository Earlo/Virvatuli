import pygame

placeholder = "frog"

# make into subclass of pygame.sprite?
#class entity():
class IDhandle():
    count = 0
    #def __init__(self):
    #    pass
    def getID(self):
        self.count += 1
        return (self.count)

IDHANDLE = IDhandle()

class entity( pygame.Rect ):
    def __init__(self, GAME, pos, time ):

        #super().__init__( (0,0), (0,0) )

        #print("created entity ",self, " at ", pygame.time.get_ticks())
        self.GAME = GAME
        self.frame = 0
        self.isInside = False

        self.ID = IDHANDLE.getID()

        self.firstMoment = time
        self.lastUpdated = self.firstMoment
        self.timeInterval = 0

        #if self.sprites == None:
        #    self.sprite = placeholder
        #    self.sprites = [placeholder]
        #else:
        #self.sprite = self.sprites[0]

        self.changeSprite( 0 )

        super().__init__( pos, self.surf().get_size() )

        self.center = pos
        self.floatpos = pos

        self.speed = 0
        self.change = self.speed * self.timeInterval

    def __eq__(self, other):
        return other != None and self.ID == other.ID

    def changeSprite(self, i):
        self.sprite = self.sprites[i]
        self.CURRENTSURFACE = self.GAME.GHandle[self.imagetype][ self.sprite ]

    def surf(self):
        return self.CURRENTSURFACE

    def drawableRect(self):
        return self.GAME.AREA.clip( self )

    def getAge(self):
        return pygame.time.get_ticks() - self.firstMoment

    def update(self):
        t = pygame.time.get_ticks()
        self.timeInterval = t - self.lastUpdated
        self.change = self.speed * self.timeInterval
        self.lastUpdated = t

