import math
import pygame
from win10toast import ToastNotifier


toaster = ToastNotifier()
def show_notification(title,content):
    toaster.show_toast(title, content, threaded = True,
                   icon_path = None)

def draw_transparent_square(win,size,alpha_level,color,pos):
    s = pygame.Surface(size)  # square size
    s.set_alpha(alpha_level)  # alpha level/ visibility( ראיה) 300 is max
    s.fill(color)  # color
    win.blit(s, pos)  # position
def draw_transparent_circle(win,x,y,radius,color,alpha_level):
    pygame.gfxdraw.filled_circle(win,x,y,radius,(color[0],color[1],color[2],alpha_level))

def draw_transparent_image(window,x,y,image,alpha_level):
    img = image.copy()
    img.set_alpha(alpha_level)
    window.blit(img,(x,y))

def check_point_in_circle(circle_x,circle_y,circle_radius,soldier_x,soldier_y):
        """same function as check in but returns the opposite"""
        sqx = (soldier_x - circle_x) ** 2
        sqy = (soldier_y - circle_y) ** 2
        if math.sqrt(sqx + sqy) < circle_radius:
            return True
        else:
            return False

def blit_fade_text(window,text,font,alpha_level,pos,color):
    text = font.render(text, True, color)
    surf = pygame.Surface(text.get_size()).convert_alpha()
    surf.fill((color[0],color[1],color[2], alpha_level))
    text.blit(surf, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
    window.blit(text, pos)

def move_buildings_handler(buildings,x_change,y_change): 
    # sometimes there is a bug(not in code) that happen and that the buildings is not in a possible pos
    # the bug:
    # that the buildings positions last 2 numbers are (10,30,50,70,90)(מספר עשרות אי זוגית)
    for building_id in buildings:
        build = buildings[building_id]
        x,y = build["pos"]
        x += x_change
        y += y_change
        build["pos"] = (x,y)
        buildings[building_id] = build
    return buildings