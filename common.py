import struct

def pack(fmt, *args):
    return struct.pack('<' + fmt, *args)

def unpack(fmt, *args):
    try:
        return struct.unpack('<' + fmt, *args)
    except:
        return
def text(scr, font, txt, pos, clr=(255,255,255)):
    scr.blit(font.render(txt, True, clr), pos)
