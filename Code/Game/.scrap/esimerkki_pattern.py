
#matikkafunktioita
import math 


#esimerkki
class movePattern1():
    def __init__(self,owner):

        self.owner = owner #olento joka seuraa ohjelmaa # voit kommentoida pois testatessa

        #voit keksiä minkä tahansa nimisiä muuttujia tässä joita voit hyödyntää algorytmissäsi
        self.suunnat = [[2,0],[0,1],[-1,0],[0,-1]]
        self.current = 0
        self.counter = 0
        self.overflow = 30

        #tässä funktiossa lasket seuraavan askeleen siirron
    def iterate(self):
        S = math.copysign(1,self.current)
        

        x, y = self.suunnat[ self.current ]     

        #print(x,y)
        #voit myös kommentoida nämä kaksi riviä pois testatessa   
        self.owner.x += x*self.owner.speed
        self.owner.y += y*self.owner.speed

        self.counter +=1
        if (self.counter % self.overflow == 0): #jos counterin jakojäännös overflowsta on 0
            self.counter = 0
            self.current += 1
            if (self.current % len(self.suunnat) == 0):
                self.current = 0

