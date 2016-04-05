

SCROLLBAR_OFFSET = [.94, .06]
SCROLLBAR_RANGE = .94

def RelativeCordinate(parent, w, h): #returs point relative to scree size
    pw, ph = parent.get_size()

    return[ int(w * pw), int(h * ph) ]

def RelativeHeight(parent, h): 
    ph = parent.get_height()
    return int(h * ph)

def RelativeWidth(parent, w, h):
    pw = parent.get_width()

    return int(w * pw)


