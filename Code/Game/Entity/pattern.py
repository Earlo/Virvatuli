
import math

import random

import pygame

from .. import vector

from . import effect


#GENERIC
class pattern():
    def __init__(self, owner):
        self.owner = owner
        self.start = pygame.time.get_ticks()
        self.timeInterval = 0
        self.side = 1

    def done(self):
        return self.time() > 2000

    def time(self):
        return pygame.time.get_ticks() - self.start

    def iterate(self, vec):
        #could be rounded?
        #but not sure if it's worth it from the point of performance.

        self.owner.floatpos = ( self.owner.floatpos[0] + vec[0] * self.owner.change,
                                self.owner.floatpos[1] + vec[1] * self.owner.change )
        #print(self.owner.floatpos)
        self.owner.center = self.owner.floatpos


#advance in sine
class movePattern0(pattern):
    def __init__(self, owner):
        super().__init__(owner)
        self.overflow = 360
        self.div = 4

    def iterate(self):
        rad = math.radians( ( self.time() / self.div ) % self.overflow )
        x = self.side*math.cos(math.sin( rad ))
        y = math.sin(math.sin( rad ))
        super().iterate( (x,y) )


#Spiral across the screen
class movePattern1(pattern):
    def __init__(self,owner):
        super().__init__(owner)
        #self.baseX = 0.5
        self.overflow = 360
        self.div = 6
        base = [1, 0 ]

    def iterate(self):

        rad = math.radians( ( self.time() / self.div ) % self.overflow )
        #x = self.side*math.sin( rad ) + 0.5
        x = ( math.cos(rad )/.75 + 0.75) / 2
        y = -math.sin( rad )


        super().iterate( (x,y) )

        #d =  ( ( rad ) ** 2 )
        #x, y = vector.uvturn( rad )

        #self.owner.x += self.side*( 0.5 + x)*self.owner.change
        #self.owner.y += y*self.owner.change

        #if self.current < self.overflow:
        #    self.current += self.increase
        #else:
        #    self.current = 0



# sine down the screen
class movePattern2(pattern):
    def __init__(self, owner):
        super().__init__(owner)
        self.side = 1
        self.overflow = 360
        self.div = 4

    def iterate(self):
        rad = math.radians( ( self.time() / self.div ) % self.overflow )

        #S = math.copysign(1,self.current)
        y = math.cos(math.sin(rad))
        x = self.side*math.sin(math.sin(rad))
        super().iterate( (x,y) )

        #user.shoot or some shit?

        #if math.fabs((self.current)) > self.overflow:
        #    self.round +=1
        #    bullets.blast( self.owner, [0,1], 1 )

        #    self.step = -self.step


#Should do a sweeping motion
class movePattern3(pattern):
    def __init__(self,owner):
        super().__init__(owner)
        self.side = 1

        self.overflow = 36000
        self.div = 0.2

    def iterate(self):
        rad = math.radians( ( self.time() / self.div ) % self.overflow )



        x, y = vector.uvturn(rad)

        #print(x,y)
        #voit myös kommentoida nämä kaksi riviä pois testatessa

        x += self.side*x**3

        super().iterate( (x,y) )






#Oh boy :,D
class boss0(pattern):
    def __init__(self, owner):
        super().__init__(owner)
        self.phases = [ self.sp0, self.p0, self.stransform, self.transform, self.sp1, self.p1, self.sp0, self.p0,
                        self.sp2, self.p2]
        self.div = 10
        #debug
        #self.phases = [self.sp0, self.p0]
        #self.degree = 0
        #self.side = 1
        #self.fire = 0
        #self.baseY = 200
        #self.cooldown = 20
        #self.step = 0
        #self.owner.hp = 100

    def iterate(self):
        if (self.phases[0]()):
            self.phases.pop(0)
            if len(self.phases) == 0:
                self.owner.DEAD = False

    def sp0(self):
        self.goal = (self.owner.GAME.AREA.centerx,
                self.owner.GAME.AREA.centery - 100)
        return True

    def p0(self): #move in
        l = vector.dis(self.owner.center, self.goal)
        v = vector.uvector(self.owner.center, self.goal)
        if l > 100:
            x = v[0] * 110/100
            y = v[1] * 110/100

        elif l>1:
            x = v[0] * (l+10)/100
            y = v[1] * (l+10)/100
        else:
            return True
        super().iterate( (x,y) )
        return False

    def stransform(self):
        self.phasestartime = self.time()
        self.limit = 50
        self.count = 0
        self.aends = [300,600,900,1800,2500]
        def atime(self):
            return self.time() - self.phasestartime
        def wait(self):
            return atime(self) > self.aends[0]
        def wake(self):
            #print(atime(self))
            self.owner.sprite = self.owner.sprites[1]
            return atime(self) > self.aends[1]
        def awake(self):
            self.owner.sprite = self.owner.sprites[2]
            return atime(self) > self.aends[2]

        self.frequency = 300
        def flick(self):
            t = (atime(self) - self.aends[2]) % self.frequency - self.frequency/2
            if t < 0:
                self.owner.sprite = self.owner.sprites[2]
            elif t > 0:
                self.owner.sprite = self.owner.sprites[3]

            if (self.frequency > 5):
                    self.frequency -= 2

            return atime(self) > self.aends[3]

        def flickbode(self):
            d = atime(self) - self.aends[3]
            t = (atime(self) - self.aends[2]) % self.frequency - self.frequency/2
            if t < 0:
                self.owner.sprite = self.owner.sprites[2]
            elif t > 0:
                self.owner.sprite = self.owner.sprites[3]
            if (self.frequency > 5):
                    self.frequency -= 2

            v = vector.uvturn(random.random()*360)
            pos = list( map(sum, zip( self.owner.center, [v[0]*(d//25)**2,v[1]*(d//25)**2])))
            self.owner.GAME.effects.append( effect.explosion( self.owner.GAME, pos, pygame.time.get_ticks() ))
            return atime(self) > self.aends[4]
        self.cphases = [wait, wake, awake, flick, flickbode]
        return True
    def transform(self):

        if ( self.cphases[0](self) ):
            self.cphases.pop(0)

        return (len(self.cphases) == 0)


    def sp1(self):
        self.owner.sprite = self.owner.sprites[4]
        self.point = [[100,185],[290,100],[480,185]]
        self.cooldown = 25
        self.lastblast = 0
        self.blastcount = 0
        return True

    def p1(self):

        l = vector.dis(self.owner.center, self.point[0])
        v = vector.uvector(self.owner.center, self.point[0])

        if l > 100:
            x = v[0] * 110/100
            y = v[1] * 110/100
            super().iterate( (x,y) )

        elif l>1:
            x = v[0] * (l+10)/100
            y = v[1] * (l+10)/100
            super().iterate( (x,y) )

        else:
            if (self.time() - self.cooldown) > self.lastblast:
                self.owner.danmaku[0](self.owner, self.blastcount*10)
                self.lastblast = self.time()
                self.blastcount += 1
            if self.blastcount == 4:
                self.blastcount = 0
                self.point.append( self.point.pop(0) )

        if self.owner.hp <= 0:
            print ("!!!")
            self.degree = 0
            self.side = 1
            self.cooldown = 20
            self.fire = 0
            self.step = 0
            self.owner.hp = 100
            self.baseY = 200
            return True


    def sp2(self):
        return True

    def p2(self):
        v = vector.uvturn( self.side * self.degree)
        self.owner.x += v[0]*self.owner.change*1.5
        self.owner.y += v[1]*self.owner.change

        if self.degree >= 360:
            self.owner.y = self.baseY
            self.side = -self.side
            self.degree = 0
        else:
            self.degree += 4

        if self.cooldown <= 0:
            self.fire = 5
            self.cooldown = 40
        else:
            self.cooldown -= 1

        if self.fire > 0:
            if self.step%3 == 0:
                if (random.random() < 0.8):
                    self.fire -= 1
                    target = self.owner.GAME.char.pos()
                    vec = vector.uvector(self.owner.pos(), target)
                    bullets.blast( self.owner, vec, 1 )
                else:
                    self.owner.danmaku(0)

        self.step += 1
        if self.owner.hp <= 0:
            print ("!!!")
            self.owner.hp = 100
            return True




class frog(pattern):
    def __init__(self, owner):
        super().__init__(owner)
        self.side = math.copysign(1, random.random() - 0.5)
        self.baseY = owner.y

        self.overflow = 360
        self.div = 4


    def iterate(self):
        rad = math.radians(  (self.time()/self.div)%self.overflow )
        y = math.cos(math.sin( rad ))**2*32
        x = self.side*math.fabs(math.sin(math.sin( rad )))

        self.owner.floatpos = ( self.owner.floatpos[0] + x*self.owner.change,
                                self.baseY + y  )

        self.owner.center = self.owner.floatpos

