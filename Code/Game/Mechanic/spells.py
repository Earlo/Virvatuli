
import random
from ..Entity import bullets
from ..Entity import enemy

def spell1(GAME):#down
    pass

def spell2(GAME):#up
    u = GAME.char
    r = GAME.AREA.grid.res
    p = GAME.AREA.grid.centerpiece.center
    bullets.blade(u,[0,-1], p, u.lastUpdated)
    for point in GAME.char.CIRCLE.upt:
        np = [p[0] + point[0]*r ,p[1] + point[1]*r ]
#        def __init__(self, user, vec, s = 0, pos = None):
        bullets.blade(u,[ random.random() / 5,-1],  np, u.lastUpdated)
    GAME.char.CIRCLE.reset()

def spell3(GAME):#Rect
    pass

def spell4(GAME):#hex
    frogs = []
    enemies = []
    for u in GAME.units:
        if u.side == "ENEMY":
            enemies.append(u)
            frogs.append( enemy.frog(GAME, u.center, u.lastUpdated) )
    for e in enemies:
        e.remove()
    #for f in frogs:
    GAME.units.extend(frogs)
    GAME.char.CIRCLE.reset()
