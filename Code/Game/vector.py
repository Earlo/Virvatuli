
import math

def dis(s,e): #distance between start and the end
    vecx = (e[0] - s[0])
    vecy = (e[1] - s[1])
    return (math.sqrt(vecx**2+vecy**2))

def uvector(s,e): #start and end, returns unitvector pointing from start towards end.
    #print (s,e)
    vecx = (e[0] - s[0])
    vecy = (e[1] - s[1])
    length = (math.sqrt(vecx**2+vecy**2))
    if length == 0:
        return [0,0]
    else:
        unitvector = (vecx/length, vecy/length)
        return unitvector


def uvturn(dir): #returns a vector pointing in direction dir (degrees)
    dir = math.radians(dir)
    vec = [math.sin(dir),math.cos(dir)]
    return vec

