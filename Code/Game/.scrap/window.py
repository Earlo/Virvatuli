
import pygame

from . import graphicalAssetHandler
from ..constants import *


class window_handler():
    def __init__(self):
        self.w = SWIDTH
        self.h = SHEIGTH
        self.create_surfaces()
        self.gamepos = (10,10)

        self.GHandle = graphicalAssetHandler.graphicalAssetHandler()
        self.needs_resize = False
        self.last_resie_request = 0

        self.updates = {}

        self.GUI = []

        from ..Gui import screens
        self.load_GUI( screens.SMainMenu )

    def create_surfaces(self): #TODO reconsider this

        #self.MainWindow = pygame.display.set_mode((self.w, self.h), pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE|pygame.FULLSCREEN)
        self.MainWindow = pygame.display.set_mode((self.w, self.h), pygame.HWSURFACE | pygame.DOUBLEBUF )
        #self.MainWindow = pygame.display.set_mode((self.w, self.h))
        #self.MainWindow = pygame.display.set_mode((self.w, self.h), pygame.DOUBLEBUF)

        #self.surf_BGR = pygame.Surface((self.w, self.h), pygame.HWSURFACE) #background surface
        #self.surf_GUI = pygame.Surface((self.w, self.h), pygame.HWSURFACE | pygame.DOUBLEBUF) #.convert() #GUI surface
        #self.surf_GAME = pygame.Surface((self.w, self.h), pygame.HWSURFACE | pygame.DOUBLEBUF) #.convert() #GAME surface
        #self.surf_EFFECT = pygame.Surface((self.w, self.h), pygame.HWSURFACE | pygame.DOUBLEBUF) #s.convert() #GAME surface
        #self.surf_VOID = pygame.Surface((self.w, self.h), pygame.HWSURFACE) #VOID surfaces

        self.surf_GUI = pygame.Surface((self.w, self.h), pygame.HWSURFACE ) #GUI surface
        self.surf_GAME = pygame.Surface((self.w, self.h), pygame.HWSURFACE ) #GAME surface
        self.surf_EFFECT = pygame.Surface((self.w, self.h), pygame.HWSURFACE ) #GAME surface


        #self.MainWindow.blit(self.surf_GUI,(0,0))
        #self.surf_BGR.fill((20,20,200))

        #self.surf_VOID.fill((255,255,255))
        #self.surf_VOID.set_alpha(0)

        #self.surf_GUI.set_colorkey((255,255,255))
        #self.surf_GAME.set_colorkey((255,255,255))
        self.surf_EFFECT.set_colorkey((0,0,0))
        self.surf_GUI.set_colorkey((0,0,0))
        #self.surf_BGR.set_colorkey((255,255,255))

        #self.surfaces = {}
        #self.surfaces[self.surf_GUI] = 4 #surface is a key for it's draw depht
        #self.surfaces[self.surf_GAME] = 2
        #self.surfaces[self.surf_BGR] = 9001

        #self.surfaces["GUI"] = [self.surf_GUI, 0] #surface is a key for it's draw depht

    def refresh_GUI(self):
        for wid in self.GUI:
            wid.draw()
            wid.blit()

    def reset_GUI(self):
        #self.surf_GUI.set_colorkey(None)

        #self.surf_GUI.fill((0,0,0))
        #self.MainWindow.blit(self.surf_GUI,(0,0))
        #self.surf_GUI.set_colorkey((0,0,0))

        self.surf_GUI = pygame.Surface((self.w, self.h) ) #reset gui
        self.surf_GUI.set_colorkey((0,0,0))

        self.GUI = []
        self.active_text_field = None
        #pygame.display.flip()

    def load_GUI(self,GUI):
        self.reset_GUI()

        GUI(self)
        self.GUI_template = GUI

        self.refresh_GUI()
        self.MainWindow.blit(self.surf_GUI, self.gamepos )
        pygame.display.flip()

    def adjust_GUI(self):

        for wid in self.GUI:
            wid.adjust(self.surf_GUI)
        self.refresh_GUI()

    def update_resolution(self):


        self.create_surfaces()
        self.adjust_GUI()
        #pygame.display.flip()

    def rezise_request(self, event):
        self.needs_resize = True
        self.last_resie_request = pygame.time.get_ticks()

        self.w = event.w
        self.h = event.h

    #def add_update(self, event):
    #    s = event.surf
    #    r = event.rect
    #    try:
    #        index = self.surfaces[s]
    #        try:
    #            self.updates[index].append( [s,r] )
    #        except KeyError:
    #            self.updates[index] = [ [s,r] ]
    #    except KeyError:
    #        pass #TODO make up something smart here later, OK?


    def update_display(self):
        """flip = False
        if self.needs_resize:
            if pygame.time.get_ticks() - self.last_resie_request > 50:
                self.update_resolution()
                self.needs_resize = False
                flip = True
        sorted(self.updates)
        upd = []
        for depth in self.updates:
            for change in self.updates[depth]:
                s,r = change
                self.MainWindow.blit( s,r,r)
                #self.MainWindow.blit(s,r)
                upd.append(r)
            self.updates[depth] = []
        if not upd == [] and not flip:
            pygame.display.update(upd)
        elif flip:
            pygame.display.flip()"""
        #self.MainWindow.blit(self.surf_GUI, self.gamepos )

        pygame.display.flip()


    def drawloop(self):
        while( not self.done ):
            self.drawGame()

            #self.clock.tick(self.FPS)
            #self.clock.tick( )
            #try:
            #    pygame.display.set_caption("FPS: %i" % self.clock.get_fps())
            #except OverflowError:
            #    pygame.display.set_caption("FPS: Quite a lot")

    def drawGame(self):

        self.surf_GAME.blit( self.GAME.AREA.surf(), (0, self.GAME.AREA.scroll) )
        if (not self.GAME.AREA.oldsprite == ""):
            self.surf_GAME.blit( self.GAME.AREA.oldsurf(), (0, self.GAME.AREA.oldscroll) )


        """
        for line in self.GAME.AREA.grid:
            for tile in line:
                #ents = set()
                #for e in tile:
                    #ents.add(e)
                #self.surf_EFFECT.blit( e.surf(), e.upleftPos(), e.rect )

                if (len(tile) > 0):
                    import math
                    a = 255/math.sqrt(len(tile))
                    c = ( a,a,len(tile)*10 )
                else:
                    c = (1,0,0)
                try:
                    pygame.draw.rect(self.surf_EFFECT, c, tile.rect, 1)
                except TypeError:
                #    print( len(tile), tile.pos )
                #    print( tile )
                    pygame.draw.rect(self.surf_EFFECT, (0,255,255), tile.rect, 1)
                    self.surf_GAME.blit( e.surf(), e.upleftPos(), e.rect)
        #"""

        #works
        for e in self.GAME.effects:
            #print( e.CURRENTSURFACE._pixels_address )
            #self.surf_GAME.blit( e.surf(), e )
            self.surf_GAME.blit( e.CURRENTSURFACE, e )
        for u in self.GAME.units:
            self.surf_GAME.blit( u.CURRENTSURFACE, u )
            #self.surf_GAME.blit( u.surf(), u )
            #pygame.draw.rect(self.surf_GAME, (255,125,125), u.hitbox, 1)

        for a in self.GAME.ammo:
            self.surf_GAME.blit( a.CURRENTSURFACE, a )
            #pygame.draw.rect(self.surf_GAME, (255,125,125), a.hitbox, 1)


        #pygame.draw.circle( self.surf_EFFECT, (0,255,0), [int(i) for i in self.GAME.char.upleftPos()] , 3 )
        #pygame.draw.circle( self.surf_EFFECT, (0,255,0), [int(i) for i in self.GAME.char.botrightPos()] , 3 )

        #pygame.draw.rect( self.MainWindow, (0,255,0), self.GAME.AREA.rect, 1 )
        #pygame.display.update(upd)

        self.MainWindow.blit(self.surf_GAME, self.gamepos, self.GAME.AREA )
        self.MainWindow.blit(self.surf_EFFECT, self.gamepos, self.GAME.AREA )
