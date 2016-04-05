import pygame

from ..constants import *

#TODO fix
def blit_request(rect, p_surf):
    signal = pygame.event.Event(update_screen_event, {"rect":rect,"surf":p_surf})
    pygame.event.post(signal)


def func_request(func):
    stype = func.pop(0)
    f = func.pop(0)
    if stype == ONETIME:
        signal = pygame.event.Event(function_call_event, {"func":f,"param":func})
    elif stype == MAINCHA:
        pass
    pygame.event.post(signal)