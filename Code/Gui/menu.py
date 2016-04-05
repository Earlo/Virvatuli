

import pygame

from pygame.locals import *

from .scale import *
RC = RelativeCordinate # a function from scale.py to find relative coordinates inside a surface

from ..constants import *
from ..Engine import events

class widget(object): #Contains all stuff common with all widegests
    def __init__(self):
        self.parent = None

    def adjust_p(self, p_surf, parent = None): #adjust parents
        if not p_surf == None:
            self.parent_surf = p_surf
        if not parent == None:
            self.parent = parent

    def adjust_r(self):
        self.surf = pygame.Surface((RC(self.parent_surf, *self.rsurf)))
        self.rect = self.surf.get_rect()
        self.pos = RC(self.parent_surf, *self.rpos)
        if not self.parent == None:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = [x + y for x, y in zip(self.pos, self.parent.absolute_position())]
        else:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = self.pos

    def absolute_position(self):
        return self.c_rect.topleft

    def relative_position(self):
        return self.pos

    def blit(self, update = True, surf = None, area = None):
        if surf == None:
            surf = self.surf
        if not area == None:
            pos = [x + y for x, y in zip(self.relative_position(), area.topleft)]
        else:
            pos = self.relative_position()

        self.parent_surf.blit(surf, pos, area) #draw self on parent surface

        if update:
            if area == None:
                area = self.rect.copy()
                area.topleft = pos
            else:
                area.move_ip(self.relative_position())
            if self.parent == None: #send event to main screen handle
                events.blit_request(area,self.parent_surf)   #edit later
                #events.blit_request(self.c_rect,self.parent_surf) #for debugging
            else: #send message forward to parent
                self.parent.blit(  area = area )

    def debug(self):
        print ("values for this widget",self,"are:\n",self.pos,"\n",self.rect,"\n",self.c_rect)

class button (widget):    #Menu Button
    def __init__(self, parent_surf, rsurf, rpos, text, func, colour = [200,20,25] ):
        super().__init__()
        self.rsurf = rsurf
        self.rpos = rpos
        self.text = text
        self.adjust(parent_surf)
        self.down = False
        self.func = func
        self.colour = colour
        self.i_colour = self.colour[:]
        self.cb_colour = [colour[0]/2,colour[1]/2,colour[2]/2]
        self.b_colour = [colour[0]/4,colour[1]/4,colour[2]/4]

    def adjust(self, p_surf, parent = None):
        self.adjust_p(p_surf, parent)
        self.adjust_r()

        font_size = int(self.rect.width/len(self.text))+5
        if font_size > self.rect.height:
            font_size = self.rect.height
        self.font = pygame.font.SysFont(FONT, font_size)
        self.label = self.font.render(self.text, 1, (1,1,1))

    def draw(self):
        self.surf.fill(self.i_colour)

        #old
        pygame.draw.rect(self.surf, self.cb_colour ,self.rect.inflate(-2,-2) ,1)
        pygame.draw.rect(self.surf, self.b_colour ,self.rect,1)

        #experimental
        #self.surf.fill(self.d_colour)
        #h = 2
        #w = 2
        #lr = pygame.Rect( (self.rect.topleft), (w, self.rect.height) )
        #tr = pygame.Rect( (self.rect.topleft), (self.rect.width, h) )
        #rr = pygame.Rect( (self.rect.topright), (-(w - 1), self.rect.height ) )
        #br = pygame.Rect( (self.rect.bottomleft), (self.rect.width, -(h - 1)) )

        #pygame.draw.rect(self.surf, self.dd_colour ,rr)
        #pygame.draw.rect(self.surf, self.colour ,lr)
        #pygame.draw.rect(self.surf, self.colour ,tr)
        #pygame.draw.rect(self.surf, self.dd_colour ,br)

        #new
        #pygame.draw.line(self.surf, self.d_colour, self.rect.topleft, self.rect.topright, 3)
        #pygame.draw.line(self.surf, self.d_colour, self.rect.topleft, self.rect.bottomleft, 3)
        #pygame.draw.line(self.surf, self.dd_colour, self.rect.bottomright, self.rect.topright, 3)
        #pygame.draw.line(self.surf, self.dd_colour, self.rect.bottomright, self.rect.bottomleft, 3) #5

        #pygame.draw.rect(self.surf, self.d_colour ,self.rect,3)

        self.surf.blit(self.label, ((self.rect.width/2) - self.label.get_width()/2, (self.rect.height/2) - self.label.get_height()/2))

    def change_colours(self):
        c = self.i_colour[:]
        self.i_colour = self.b_colour[:]
        self.b_colour = c
        self.draw()
        self.blit()

    def pressed(self, PROGRAM, event):
        if self.c_rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONUP:
                #self.debug()
                self.down = True
                self.change_colours()
                events.func_request(self.func[:])

class menu_box (widget): #box that contains several other widgets inside itself
    def __init__(self, parent_surf, rsurf, rpos, colour, title = ""):
        super().__init__()

        self.rsurf = rsurf
        self.rpos = rpos

        self.content = []

        self.adjust(parent_surf)

        self.colour = colour
        self.d_colour = [colour[0]/2,colour[1]/2,colour[2]/2]
        self.title = title
        if not title == "":
            self.create_label()

    def adjust(self, p_surf, parent = None):
        self.adjust_p(p_surf, parent)
        self.adjust_r()

        for wid in self.content:
            wid.adjust(self.surf, parent = self)

    def create_label(self):
        self.label = label(self.surf, .05, (0,0),self.title)
        self.add_widgets([self.label])

    def add_widgets(self,con):
        self.content.extend(con)
        for wid in self.content:
            wid.adjust(self.surf, parent = self)
        self.draw()

    def draw(self):
        self.surf.fill(self.colour)
        pygame.draw.rect(self.surf, self.d_colour ,self.rect,1)
        for x in self.content:
            x.draw()
            x.blit(update = False)

    def debug_lines(self):
        w = 3
        for x in range(0,self.surf.get_width(),20):
            p0 = (x, 0)
            p1 = (x, self.surf.get_height())
            r = (x * 100) % 255
            b = (r * 100) % 255
            g = (b * 100) % 255
            c = (r, b, g)
            pygame.draw.line(self.surf, c, p0, p1, w)

        for y in range(0,self.surf.get_height(),20):
            p0 = (0, y)
            p1 = (self.surf.get_width(), y)
            r = (x * 100) % 255
            b = (r * 100) % 255
            g = (b * 100) % 255
            c = (r, b, g)
            pygame.draw.line(self.surf, c, p0, p1, w)

    def pressed(self, PROGRAM, event):
        if self.c_rect.collidepoint(event.pos):
            #if event.type == pygame.MOUSEBUTTONUP:
                #self.debug()
            for x in self.content:
                x.pressed(PROGRAM,event)

class scroll_menu_box(widget):
    def __init__(self, p_surf, view_size, rpos, colour, rsurf, title = ""):
        super().__init__()

        self.rsurf = rsurf
        self.rpos = rpos
        self.view_size = view_size

        self.content = []
        self.scroll_bar = None


        self.colour = colour
        self.d_colour = [colour[0]/2,colour[1]/2,colour[2]/2]

        self.adjust(p_surf)

        self.font_size = 18
        self.font = pygame.font.SysFont(FONT, self.font_size)
        self.title = title
        if not title == "":
            self.create_label()
    def adjust(self, p_surf, parent = None):
        self.adjust_p( p_surf, parent)
        self.adjust_r()
        if self.scroll_bar == None:
            max_scroll = self.surf.get_height() - self.viewport.get_height()
            self.scroll_bar = drag_bar(self.viewport, (.05, .1), .02 )
            self.scroll_bar.adjust(self.viewport, parent = self)
        else:
            self.scroll_bar.adjust(self.viewport, parent = self)
        for wid in self.content:
            wid.adjust(self.viewport, parent = self)
            wid.parent_surf = self.surf

    def adjust_r(self):
        self.viewport =  pygame.Surface(( RC( self.parent_surf, *self.view_size ) ))
        self.surf = pygame.Surface(( RC( self.viewport, *self.rsurf ) ))
        self.rect = self.viewport.get_rect()
        self.pos = RC(self.parent_surf, *self.rpos)
        if not self.parent == None:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = [x + y for x, y in zip(self.pos, self.parent.c_rect.topleft)]
        else:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = self.pos

    def scroll(self):
        self.scroll_bar.adjust(self.viewport, self)
        self.viewport.blit(self.surf, ( 0, - self.scroll_bar.OFFSET * (self.surf.get_height() - self.viewport.get_height() ) ) )

        #OS = self.get_offset()
        #return [x + y for x, y in zip(self.pos, OS)]
        #self.pos = [x + y for x, y in zip(RC(self.parent_surf, *self.rpos), OS)]

        self.scroll_bar.draw()
        self.scroll_bar.blit(update = False)

    def absolute_position(self):
        OS = self.get_offset()
        return [x + y for x, y in zip(self.c_rect.topleft, OS)]

    def get_offset(self):
        return [0, int(- self.scroll_bar.OFFSET * (self.surf.get_height() - self.viewport.get_height() )) ]


    def create_label(self):
        self.label = label(self.surf,.05,(0,0),self.title)
        self.add_widgets([self.label])

    def add_widgets(self,con):
        self.content.extend(con)
        for wid in self.content:
            wid.adjust(self.viewport, parent = self)
            wid.parent_surf = self.surf
        self.scroll()

        self.draw()

    def draw(self):
        self.surf.fill(self.colour)
        #self.debug_lines()

        for x in self.content:
            x.draw()
            x.blit(update = False)
        self.scroll_bar.adjust(self.viewport, self)
        self.viewport.blit(self.surf, self.get_offset() )
        self.scroll_bar.draw()
        self.scroll_bar.blit(update = False)
        pygame.draw.rect(self.viewport, self.d_colour ,self.rect,1)

    def debug_lines(self):
        w = 3
        for x in range(0,self.surf.get_width(),39):
            p0 = (x, 0)
            p1 = (x, self.surf.get_height())
            r = (x * 100) % 255
            b = (r * 100) % 255
            g = (b * 100) % 255
            c = (r, b, g)
            pygame.draw.line(self.surf, c, p0, p1, w)

        for y in range(0,self.surf.get_height(),39):
            p0 = (0, y)
            p1 = (self.surf.get_width(), y)
            r = (x * 100) % 255
            b = (r * 100) % 255
            g = (b * 100) % 255
            c = (r, b, g)
            pygame.draw.line(self.surf, c, p0, p1, w)

    def blit(self, update = True, surf = None, area = None):
        if surf == None:
            surf = self.viewport # ?
        if not area == None:
            c_area = area.copy()
            OS = self.get_offset()
            area.move_ip(OS)

            pos = [x + y for x, y in zip(self.relative_position(), area.topleft)]
            p = [x + y for x, y in zip(c_area.topleft, OS)]
            self.viewport.blit(self.surf, p, c_area ) #?
        else:
            pos = self.relative_position()

        self.parent_surf.blit(surf, pos, area) #draw self on parent surface

        if update:
            if area == None:
                area = self.rect.copy()
                area.topleft = pos
            else:
                area.move_ip(self.relative_position())
            if self.parent == None: #send event to main screen handle
                events.blit_request(area,self.parent_surf)   #edit later
                #events.blit_request(self.c_rect,self.parent_surf) #for debugging
            else: #send message forward to parent
                self.parent.blit(  area = area )

    def pressed(self, PROGRAM, event):
        if self.c_rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONUP:
                m_OS = [0, self.scroll_bar.OFFSET * (self.surf.get_height() - self.viewport.get_height() )]
                event.pos =  [x + y for x, y in zip(event.pos, m_OS)]
                for x in self.content:
                    x.pressed(PROGRAM,event)
            else:
                self.scroll_bar.pressed(PROGRAM,event)

class drag_bar(widget):
    def __init__(self, parent_surf, rrect, rh, colour = [20,20,20] ):
        super().__init__()

        self.rrect = rrect
        self.rsurf = [self.rrect[0], SCROLLBAR_RANGE]
        self.rpos = [SCROLLBAR_OFFSET[0], rh ]
        self.OFFSET = 0
        self.G_OFFSET = 0

        #self.scroll_ratio = scroll_ratio

        self.adjust(parent_surf)
        self.colour = colour

    def adjust(self, p_surf, parent = None):
        self.adjust_p(p_surf, parent)
        self.adjust_r()

        self.bar = pygame.Surface(RC(self.parent_surf, *self.rrect))
        self.bar_rect = self.bar.get_rect()
        self.bar_rect.topleft = [0,self.G_OFFSET]
        self.c_bar_rect = self.bar_rect.copy()
        self.c_bar_rect.topleft = [self.c_rect.topleft[0],self.c_rect.topleft[1] + self.G_OFFSET]

        self.MAX_G_OFFSET = self.parent_surf.get_height() * (SCROLLBAR_RANGE - self.rrect[1])
        self.G_OFFSET = self.MAX_G_OFFSET * self.OFFSET

    def adjust_r(self):
        self.surf = pygame.Surface((RC(self.parent_surf, *self.rsurf)))
        self.rect = self.surf.get_rect()
        self.pos = RC(self.parent_surf, *self.rpos)
        if not self.parent == None:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = [x + y for x, y in zip(self.pos, self.parent.c_rect.topleft)]
        else:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = self.pos

    def draw(self):
        self.surf.fill(self.parent.colour)
        pygame.draw.line(self.surf, self.colour, self.rect.midtop, self.rect.midbottom, 3)
        pygame.draw.rect(self.surf, self.colour ,self.bar_rect, 0)

    def pressed(self, PROGRAM, event):
        if self.c_rect.collidepoint(event.pos):
            if self.c_bar_rect.collidepoint(event.pos):
                PROGRAM.active_drag_obj = self

    def dragged(self,event):
        c = event.rel[1]
        self.G_OFFSET += c
        if self.G_OFFSET < 0:
            self.G_OFFSET = 0
            c = 0
        elif self.G_OFFSET > self.MAX_G_OFFSET:
            self.G_OFFSET = self.MAX_G_OFFSET
            c = 0

        self.c_rect.topleft = self.pos
        self.OFFSET = self.G_OFFSET / self.MAX_G_OFFSET

        self.parent.scroll()
        self.parent.blit()

class label(widget):
    def __init__(self, p_surf, rheight, rpos, text):
        super().__init__()
        self.rpos = rpos
        self.rheight = rheight
        if not type(text) == list:
            text = [str(text)]
        self.text = text
        self.adjust(p_surf)

    def adjust(self, p_surf, parent = None):
        self.adjust_p(p_surf, parent)
        self.adjust_r()

    def adjust_r(self):
        h = RelativeHeight(self.parent_surf, self.rheight)
        self.font_size = int( h / len( self.text ) )
        self.font = pygame.font.SysFont(FONT, self.font_size)

        self.create_lines()

        w = max( map ( lambda line: line.get_width(), self.lines))
        w = w * 1.05
        self.surf = pygame.Surface((w,h))
        self.rect = self.surf.get_rect()
        self.pos = RC(self.parent_surf, *self.rpos)
        if not self.parent == None:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = [x + y for x, y in zip(self.pos, self.parent.absolute_position())]
        else:
            self.c_rect = self.rect.copy()
            self.c_rect.topleft = self.pos

    def change_text(self, new_text):
        if not type(new_text) == list:
            new_text = [str(new_text)]
        old_text = self.text
        self.text = new_text
        self.create_lines()
        w = max( map ( lambda line: line.get_width(), self.lines)) *1.05
        wold = self.surf.get_width()
        if not len(self.text) == len(old_text) or (abs(wold - w) > 0.02*wold ) :
            self.adjust_r()

    def create_lines(self):
        self.lines = []
        for t in self.text:
            line = self.font.render(t, 1, (250,250,250))
            self.lines.append( line )

    def draw(self):
        self.surf.fill((30,30,30))
        x = 0
        for line in self.lines:
            self.surf.blit( line, (0, self.font_size * x ) )
            x += 1

    def pressed(self, PROGRAM, event):
        return False

class input_box(widget):
    def __init__(self, p_surf, rsurf, rpos, explanation, string):
        super().__init__()

        self.rpos = rpos
        self.rsurf = rsurf

        self.string = str(string)
        self.context = str(explanation)
        self.suffix = ""
        self.active = False
        self.adjust(p_surf)

    def adjust(self, p_surf, parent = None):
        self.adjust_p(p_surf, parent)
        self.adjust_r()

        self.font_size = int(self.rect.height/2)
        self.font = pygame.font.SysFont(FONT, self.font_size)

    def update(self,event):
        key = event.key
        if key == K_BACKSPACE:
            self.string = self.string[0:-1]
        else:
            try:
                self.string += str(event.unicode)
            except KeyError:
                pass
        self.draw()
        self.blit()
        #self.blit(area = self.rect)

    def draw(self):
        string = self.string + self.suffix
        self.label = self.font.render(string, 1, (250,250,250))
        self.explanation = self.font.render(self.context, 1, (200,200,200))

        self.surf.fill((30,30,30))
        self.surf.blit(self.explanation,(0,0))
        self.surf.blit(self.label,(0,self.font_size))
        #self.surf.blit(self.label,(0, 0))

    def activate(self):
        pygame.key.set_repeat(LETTER_INPUT_HELD_DOWN_DELAY,
                      LETTER_INPUT_HELD_DOWN_INTERWAL)
        self.suffix = INPUT_BOX_ACTIVITY_INDICATOR
        self.draw()
        self.blit()

    def inactivate(self):
        pygame.key.set_repeat()
        self.suffix = ""
        self.draw()
        self.blit()

    def pressed(self, PROGRAM, event):
        if self.c_rect.collidepoint(event.pos):
            if event.type == pygame.MOUSEBUTTONUP:
                PROGRAM.active_text_field = self
                self.activate()

class bar(widget): #TODO update
    def __init__(self, p_surf, rsurf, rpos, explanation, range , c0 = (1,1,1), c1 = (255,0,0) ):
        super().__init__()

        self.rpos = rpos
        self.rsurf = rsurf

        self.context = str(explanation)
        ##self.suffix = ""

        self.value_min = range[0]
        self.value_max = range[1]
        self.value = range[0]

        self.adjust(p_surf)

    def adjust(self, p_surf, parent = None):
        self.adjust_p(p_surf, parent)
        self.adjust_r()

        self.font_size = int(self.rect.height/2)
        self.font = pygame.font.SysFont(FONT, self.font_size)
        #end


        self.s_rect = self.rect.inflate(2,2) #surrounding rect

        #self.c0 = (1,1,1)
        #self.c1 = (255,0,0)

        self.c0 = c0
        self.c1 = c1
        self.ct = (self.c1[0]/2,self.c1[1]/2,self.c1[2]/2)
        #self.s_rect = self.rect.inflate(2,2) #surrounding rect

        #self.keys = keys

        self.font_size = self.rect.height
        #self.font_size = 12
        self.font = pygame.font.SysFont(FONT, self.font_size)

    def pressed(self, PROGRAM, event):
        return False
    #    return self.rect.collidepoint(mouse)

    def act(self):
        pass

    def update(self):
        if self.value < self.value_min:
            self.value = self.value_min
        if self.value > self.value_max:
            self.value = self.value_max
        self.draw()
        return self.value

    def draw(self, update = True):
        self.explanation = self.font.render(self.context+": "+ str(self.value), 1, self.ct)
        from ..Engine.engine import PROGRAM
        #border
        pygame.draw.rect(PROGRAM.surf_GUI, (100,100,100),self.s_rect, 1)

        w = self.rect.width
        wp = w * (self.value - self.value_min) / (self.value_max - self.value_min)
        pygame.draw.rect(PROGRAM.surf_GUI, self.c0 ,self.rect, 0) #base colour
        if not wp == 0:
            nrect = pygame.Rect(self.rect.topleft,(wp,self.rect.height))
            pygame.draw.rect(PROGRAM.surf_GUI, self.c1 ,nrect, 0) #fill colour

        #e_pos = [x + y for x, y in zip(self.rect.midtop, (-self.explanation.get_width()/2,-4-self.font_size))]
        e_pos = [x + y for x, y in zip(self.rect.midtop, (-self.explanation.get_width()/2, 2 ))]

        ex_rect = PROGRAM.surf_GUI.blit(self.explanation,e_pos)


        PROGRAM.MainWindow.blit(PROGRAM.surf_GUI, self.s_rect, self.s_rect)
        PROGRAM.MainWindow.blit(PROGRAM.surf_GUI, ex_rect, ex_rect)
        PROGRAM.updates.append(self.s_rect)



