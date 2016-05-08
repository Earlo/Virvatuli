import os
import sys
#import __main__

import pygame
#BASEPATH = os.path.dirname(os.path.realpath(__main__.__file__))
BASEPATH = os.path.dirname(os.path.realpath(sys.argv[0]) )

fpath = os.path.join(BASEPATH,"Assets")

class graphicalAssetHandler(dict):
    def __init__(self):
        super().__init__()

        self["SPRITE"] = dict()
        self["PORTRAIT"] = dict()
        self["BGR"] = dict()

        for root, dirs, files in os.walk( os.path.join( fpath,"sprites") ):
            for file in files:
                if file.endswith(".png"):
                    name = file.split(os.path.sep)[-1].split(".")[0]
                    i = pygame.image.load( os.path.join( fpath,"sprites", file) ).convert()

                    i.set_colorkey(i.get_at((0, 0)), pygame.RLEACCEL)
                    #i = i.subsurface( i.get_bounding_rect() ).convert()
                    #i.set_colorkey( )

                    self["SPRITE"][name] = i

        for root, dirs, files in os.walk( os.path.join( fpath,"portraits") ):
            for file in files:
                if file.endswith(".png"):
                    path = os.path.join( fpath,"portraits", file)
                    name = file.split(os.path.sep)[-1].split(".")[0]
                    i = pygame.image.load( path ).convert()

                    #get the smallest image that has all the significatn pixels
                    i.set_colorkey(i.get_at((0, 0)))
                    #i = i.subsurface( i.get_bounding_rect() ).convert()

                    self["PORTRAIT"][name] = i

        for root, dirs, files in os.walk( os.path.join( fpath,"bgr") ):
            for file in files:
                if file.endswith(".png"):
                    path = os.path.join( fpath,"bgr", file)
                    name = file.split(os.path.sep)[-1].split(".")[0]
                    i = pygame.image.load( path ).convert()
                    #i.set_colorkey(i.get_at((0, 0)))
                    self["BGR"][name] = i


                    
class graphicalDict(dict):
    def __init__(self):
        super().__init__()

        self["SPRITE"] = dict()
        self["PORTRAIT"] = dict()
        self["BGR"] = dict()

        for root, dirs, files in os.walk( os.path.join( fpath,"sprites") ):
            for file in files:
                if file.endswith(".png"):
                    name = file.split(os.path.sep)[-1].split(".")[0]
                    i = pygame.image.load( os.path.join( fpath,"sprites", file) )

                    i.set_colorkey(i.get_at((0, 0)))
                    #i = i.subsurface( i.get_bounding_rect() ).convert()
                    #i.set_colorkey( )

                    self["SPRITE"][name] = i

        for root, dirs, files in os.walk( os.path.join( fpath,"portraits") ):
            for file in files:
                if file.endswith(".png"):
                    path = os.path.join( fpath,"portraits", file)
                    name = file.split(os.path.sep)[-1].split(".")[0]
                    i = pygame.image.load( path )

                    #get the smallest image that has all the significatn pixels
                    i.set_colorkey(i.get_at((0, 0)))
                    #i = i.subsurface( i.get_bounding_rect() ).convert()

                    self["PORTRAIT"][name] = i

        for root, dirs, files in os.walk( os.path.join( fpath,"bgr") ):
            for file in files:
                if file.endswith(".png"):
                    path = os.path.join( fpath,"bgr", file)
                    name = file.split(os.path.sep)[-1].split(".")[0]
                    i = pygame.image.load( path )
                    self["BGR"][name] = i
                    