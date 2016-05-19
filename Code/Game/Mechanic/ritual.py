import pygame


from .. import vector
from ..Entity import unit
from ..Entity import effect


from ..Entity import pattern
class beaconMove(pattern.pattern):
    def __init__(self, owner):
        super().__init__( owner )

    def iterate( self ):
        #redo

        if (not self.owner.onSpot):

            p = self.owner.tile.rect.center

            if (vector.dis(self.owner.center, p) < self.owner.change):
                #print( p, self.owner.topleft )
                self.owner.center = p
                self.owner.onSpot = True
                self.owner.tile.occupied = True
                if (self.owner.tile.grid.centerpiece == None):
                    self.owner.GAME.char.CIRCLE.start( self.owner, self.owner.tile.grid )
                    #self.tile.grid.set_cp(self)
                elif( not (self.owner.tile.pos in self.owner.GAME.char.CIRCLE.ctiles.values() )):
                    self.owner.GAME.char.CIRCLE.reset()
                    #had to do this due to loop structure in unit.update
                    self.owner.used = True
                    #self.owner.remove()
                else:
                    self.owner.GAME.char.CIRCLE.place(self.owner)
            else:
                if not self.owner.tile.occupied:
                    m = 1
                else:
                    m = -1
                vec = vector.uvector(self.owner.center, p)
                super().iterate( (vec[0]*m,vec[1]*m) )
                self.owner.addToGrid()
        #else:
        #    super().iterate( (0,0) )


class beacon(unit.unit):
    sprites = ["energy3"]
    def __init__(self, GAME, pos, time):
        super().__init__(GAME, pos, time)
        self.onSpot = False
        self.side = "ALLY"
        self.used = False
        self.pattern = beaconMove(self)
        self.speed = 0.1

    def move(self):
        pass

    def hit(self,bullet):
        pass

    def addToGrid(self):
        super().addToGrid()
        #do something here to give player the advantage on border cases
        self.tile = self.tiles[0]
        #print(self.tile.rect, len(self.tiles))

    def update(self):
        #print(self)
        super().update()

    def remove(self):
        self.GAME.effects.remove(self)
        if self.onSpot:
            self.tile.occupied = False
        self.resetTiles()

    def deathConditions(self):
        return (self.drawableRect().size == (0,0)) or self.used

class circle():
    hexr =  [(-2,-1) , (-2,1) , (0,2) , (0,-2) , (2,1) , (2,-1)]
    crect =  [(-2,-1) , (-2,1) , (2,1) , (2,-1)]
    upt = [(-2,1) , (0,-2) , (2,1)]
    downt =  [(-2,-1) , (0,2) , (2,-1)]

    combos = [[-2,-1], [-2,1], [0,2],[0,0],[0,-2], [2,1], [2,-1] ]

    def __init__(self):
        self.ctiles = {}
        self.beacons =  []
        self.filled = []
        self.tileEffects = []
        self.drawPoints = []

    def start(self,cp,grid):
        x0,y0 = cp.tile.pos
        self.GAME = cp.GAME
        self.grid = grid
        grid.centerpiece = cp
        for x,y in self.combos:
            if ( (x0+x < 0) or (y0+y < 0) or (x0+x >= len(grid)) or (y0+y >= len(grid[0])) ):
                self.reset()
                return False
            else:
                t = grid[x0 + x][y0 + y]
                self.ctiles[ (x,y) ] = t.pos
                #self.ctiles.append( t.pos )
                #t.draw(cp.GAME.AREA.effectSurf, c = (255,255,100))
        self.drawTiles()
        return True


    def place(self, b):
        for key,t in self.ctiles.items():
            if t == b.tile.pos:
                self.filled.append(key)
                self.beacons.append(b)
        self.testConnections()


    def testConnections(self):
        self.removeEffect()
        self.drawTiles()
        if  all( point in self.filled for point in self.hexr):
            #self.drawTiles()
            self.drawCIRCLE(self.upt)
            self.drawCIRCLE(self.downt)
            self.GAME.char.ACTIVECIRCLE =  4
        elif  all( point in self.filled for point in self.crect): #rect
            #self.drawTiles()
            self.drawCIRCLE(self.crect)
            self.GAME.char.ACTIVECIRCLE =  3
        elif  all( point in self.filled for point in self.upt): #triup
            #self.drawTiles()
            self.drawCIRCLE(self.upt)
            self.GAME.char.ACTIVECIRCLE =  2
        elif  all( point in self.filled for point in self.downt): #tridown
            #self.drawTiles()
            self.drawCIRCLE(self.downt)
            self.GAME.char.ACTIVECIRCLE =  1

    #def effect(self):

    #   print("something happened")


    def reset(self):

        self.removeEffect()
        self.ctiles = {}
        
        self.removeEffect()
        
        self.filled = []
        for b in self.beacons:
            b.remove()
        self.beacons =[]
        self.grid.centerpiece.remove()
        
        self.grid.centerpiece = None
        self.GAME.char.ACTIVECIRCLE = 0

    def removeEffect(self):
        #pass
        for e in self.tileEffects:
            self.GAME.effects.remove(e)
        self.tileEffects = []
        self.drawPoints = []
        #self.GAME.PROGRAM.surf_EFFECT.set_colorkey()
        #self.GAME.PROGRAM.surf_EFFECT.fill((0,0,0,0))
        #self.GAME.PROGRAM.surf_EFFECT.set_colorkey((0,0,0,0))

    def drawTiles(self):
        x0,y0 = self.grid.centerpiece.tile.pos
        for x,y in self.combos:
                t = self.grid[x0 + x ][y0 + y ]
                e = effect.MagicTile( self.GAME, t.rect.center)
                self.tileEffects.append( e )
                self.GAME.effects.append( e )
                #pygame.draw.rect(self.GAME.PROGRAM.surf_EFFECT, (0,255,255), t.rect, 1)

    def drawCIRCLE(self, ctype):
        r = self.grid.res
        points = []
        for k in ctype:
            p = self.ctiles[k]
            points.append( (p[0]*r + r/2, p[1]*r + r/2) )
        self.drawPoints.append( points )
        #pygame.draw.polygon(self.GAME.PROGRAM.surf_EFFECT, (20,20,200), points, 5)
        #pygame.draw.polygon(self.GAME.PROGRAM.surf_EFFECT, (100,100,255), points, 3)
        #pygame.draw.polygon(self.GAME.PROGRAM.surf_EFFECT, (200,200,255), points, 1)




