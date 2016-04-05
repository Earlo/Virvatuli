from .. import vector

from . import bullets

def roundblast(user,os,f = 30):
    for  a in range(0,360,f):
        vec = vector.uvturn(a+os)
        bullets.blast( user, vec, user.lastUpdated )
