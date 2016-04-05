
import math
import itertools

import pygame


class grid(list):
    def __init__(self, size, res):
        super().__init__()
        self.size = size
        self.res = res

        self.x_range = (size[0] // res)
        self.y_range = (size[1] // res)

        self.centerpiece = None

        for a in range( self.x_range ):
            self.append([])
            for b in range( self.y_range ):
                self[a].append( tile (self, [a, b] ) )
                # self.tiles[-1].draw(self.surf)

    def add(self, unit):
        #pretty byt slow

        #ul = unit.topleft
        #br = unit.bottomright
        #minx = max( min( ul[0] // self.res, self.x_range ), 0)
        #miny = max( min( ul[1] // self.res, self.y_range ), 0)
        #maxx = max( min( math.ceil(br[0] / self.res), self.x_range ), 0)
        #maxy = max( min( math.ceil(br[1] / self.res), self.y_range ), 0)

        #ugly but faster

        minx,maxx,miny,maxy = self.getTiles( unit.hitbox.topleft, unit.hitbox.bottomright)

        #minx = unit.topleft[0] // self.res
        #miny = unit.topleft[1] // self.res
        #maxx = math.ceil( unit.bottomright[0] / self.res)
        #maxy = math.ceil( unit.bottomright[1] / self.res)

        for a in range(minx,maxx):
            for b in range(miny,maxy):
                #t = self[a][b]
                #unit.tiles.append( t )
                #t.append(unit)
                unit.tiles.append( self[a][b] )
                self[a][b].append( unit )

    def getTiles(self, ul, br):
        minx = ul[0] // self.res
        miny = ul[1] // self.res
        maxx = math.ceil( br[0] / self.res)
        maxy = math.ceil( br[1] / self.res)

        if minx < 0:
            minx = 0
        elif minx > self.x_range:
            minx = self.x_range

        if miny < 0:
            miny = 0
        elif miny > self.y_range:
            miny = self.y_range

        if maxx < 0:
            maxx = 0
        elif maxx > self.x_range:
            maxx = self.x_range

        if maxy < 0:
            maxy = 0
        elif maxy > self.y_range :
            maxy = self.y_range

        return minx,maxx,miny,maxy

class tile(list):
    def __init__(self, grid, pos):
        #debuig
        self.colour = [50,50,50]
        self.occupied = False
        self.grid = grid
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0] * self.grid.res, self.pos[1] * self.grid.res, self.grid.res, self.grid.res)

    def draw(self, surf, c=[100, 100, 100]):
        pygame.draw.rect(surf, c, self.rect, 1)
