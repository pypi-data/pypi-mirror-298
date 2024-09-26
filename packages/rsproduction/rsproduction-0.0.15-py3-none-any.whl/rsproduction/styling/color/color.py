def bgr2rgb(color_bgr):
    return (color_bgr[2], color_bgr[1], color_bgr[0])

def rgb2bgr(color_rgb):
    return (color_rgb[2], color_rgb[1], color_rgb[0])

def as_float(color):
    return color / 255

def as_int(color):
    res = (int(color[0]*255), int(color[1]*255), int(color[2]*255))
    return res

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

LIGHT_GRAY = as_int((0.8, 0.8, 0.8))
DARK_GRAY = as_int((0.4, 0.4, 0.4))
CORNFLOWER_BLUE = as_int((1., 0.6, 0.6))
COLOR = as_int((0.4, 0.4, 0.4))
DARKRED = as_int((0., 0., 0.545))
FOCUSED = CORNFLOWER_BLUE

FOREGROUND = BLACK
FOREGROUND_DISABLED = DARK_GRAY