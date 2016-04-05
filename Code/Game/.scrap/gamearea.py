    def blit(self, update = True, surf = None, area = None):
        if surf == None:
            surf = self.surf
        if not area == None:
            pos = [x + y for x, y in zip(self.relative_position(), area.topleft)]
        else:
            pos = self.relative_position()[:]
        pos[1] += self.scroll
        self.parent_surf.blit(surf, pos, area) #draw self on parent surface

        if update:
            if area == None:
                area = self.rect.copy()
                #area.topleft = pos
                area.topleft = self.relative_position()[:]
            else:
                area.move_ip(self.relative_position())
            #events.blit_request(area,self.parent_surf)   #edit later
            self.parent_surf.blit(self.effectSurf, area.topleft )
            #events.blit_request(area,self.parent_surf)   #edit later
