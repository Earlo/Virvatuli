
"""
    def erase(self):#does not work properly (?)
        self.blit(surf = self.GAME.PROGRAM.surf_VOID, area = self.rect)
        area = self.surf().get_rect().copy()
        area.topleft = self.gPos()

    def blit(self, update = True, surf = None, area = None):
        if surf == None:
            surf = self.surf()
        if not area == None:
            pos = [x + y for x, y in zip( self.gPos(), area.topleft)]
        else:
            pos = self.gPos()

        #self.GAME.PROGRAM.surf_GAME.blit(surf, pos, area) #draw self on parent surface
"""
