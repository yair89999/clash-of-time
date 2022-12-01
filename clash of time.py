import pygame
import pygame.gfxdraw
from win32api import GetSystemMetrics
import os,time,random,math,webbrowser


if os.getcwd().split("\\")[-1] != "clash of time": # os.getcwd() gets the folder the file runs on
    try:
        os.chdir("clash of time") # change the diractory it works on to discord bot(now it start it from the "games and projects" directory)
    except: # can cause a error if it starts it from the folder
        pass

# doing the imports that using things in the folder "/clash of time"
from module import *

pygame.mixer.pre_init(44100, 16, 2, 4096) # improves the sound
pygame.init()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,+30) # place the window in the screen

screen_x,screen_y = GetSystemMetrics(0),GetSystemMetrics(1) - 70 # fullscreen
screen_rect = pygame.Rect(0,0,screen_x,screen_y)
window = pygame.display.set_mode((screen_x,screen_y))
pygame.display.set_caption("clash of time")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP]) # pygame.event.get() will only check for the events in the []

folder = "images" # when changing it change in the getBuildingsNames file too
very_small_font = pygame.font.SysFont("", 20)
small_font = pygame.font.SysFont("", 25)
font = pygame.font.SysFont("", 30)
font_shadow = pygame.font.SysFont("", 35) # for the font in the line above
medium_font = pygame.font.SysFont("",35)
bigger_font = pygame.font.SysFont("", 40)
huge_font = pygame.font.SysFont("", 50)

game_icon = pygame.transform.smoothscale(pygame.image.load(folder+"/game icon.png"), (int(screen_x//3),int(screen_x//3*0.5625))) # 1920x1080  1:0.5625
game_icon.set_alpha(200)

class create_base_bg():
    def __init__(self):
        self.width,self.height = 1000,1000
        self.tiles = [] # [tile,tile...] [(x,y,color(rgb)),(x,y,color(rgb))...] 10,000 tiles
        self.centered_tile = None # for other classes use
        self.centered_tile_index = None
        self.tile_size = 20 # 20px = width,height
        self.tile = {1:pygame.transform.scale(pygame.image.load(folder+"/grass/type1.png").convert_alpha(),(self.tile_size,self.tile_size)),
         2:pygame.transform.scale(pygame.image.load(folder+"/grass/type2.png").convert_alpha(),(self.tile_size,self.tile_size))}
        self.draw_sea = True
        self.sea = pygame.transform.smoothscale(pygame.image.load(folder + "/sea animation around tiles.png").convert_alpha(),(int(self.tile_size*2*1.6),self.tile_size*2)) # 500x300 1.6:1
        self.sea_animation_time = time.time()+1 # every sec the sea will move
        self.sea_animation_start_y = 0
        self.sea_animation_pixels_per_time = 10
    def set(self): # set the tiles of the board(get positions)
        center_tile = None
        center_tile_index = None
        color_a = (0,235,0)
        color_b = (0,200,0)
        num_of_tiles = 100
        
        tiles_pos = open("user data/tiles start pos.txt","r").read()
        if tiles_pos == "":
            start_x =  (screen_x//2) - (num_of_tiles*self.tile_size  //2)
            start_y =  (screen_y//2) - (num_of_tiles*self.tile_size  //2)
        else:
            start_x,start_y = (int(tiles_pos.split(",")[0]),int(tiles_pos.split(",")[1]))

        self.start_pos = (start_x,start_y)
        color = 1 # 1/0
        center = (start_x + num_of_tiles*self.tile_size//2,start_y + num_of_tiles*self.tile_size//2)
        self.tiles.append(
                    (center[0],center[1], (255,0,0),1)
                ) # marks the center of the base
        for n in range(1,num_of_tiles+1):
            for n2 in range(1,num_of_tiles+1):
                if n == num_of_tiles//2 and n2 == num_of_tiles//2:
                    center_tile = (start_x + self.tile_size *n,start_y + self.tile_size*n2, color_a,1)
                    center_tile_index = n
                if color == 1:
                    self.tiles.append(
                        (start_x + self.tile_size *n,start_y + self.tile_size*n2, color_a,1)
                        )
                    color = 0
                else:
                    self.tiles.append(
                        (start_x + self.tile_size *n,start_y + self.tile_size*n2, color_b,2)
                        )
                    color = 1
            if color == 1: color = 0
            else: color = 1
        self.centered_tile = center_tile
        self.centered_tile_index = center_tile_index
    def draw_tiles(self):
        if self.draw_sea == True:
            #window.fill((0,160,222)) # clean blue as sea
            for x in range(0,screen_x,self.sea.get_width()):
                for y in range(self.sea_animation_start_y-self.sea.get_height(),screen_y,self.sea.get_height()):
                    window.blit(self.sea,(x,y))
            if self.sea_animation_time <= time.time():
                self.sea_animation_start_y += self.sea_animation_pixels_per_time
                self.sea_animation_pixels_per_time *= -1
                self.sea_animation_time = time.time()+1
        for tile in self.tiles[1:]:
            if screen_rect.colliderect(pygame.Rect(tile[0],tile[1],self.tile_size,self.tile_size)):
                window.blit(self.tile[tile[3]],(tile[0],tile[1]))
                #pygame.draw.rect(window, tile[2], [tile[0],tile[1],self.tile_size,self.tile_size])
        pygame.draw.rect(window, self.tiles[0][2], [self.tiles[0][0]+2,self.tiles[0][1]+2,self.tile_size-4,self.tile_size-4]) # red
        pygame.draw.rect(window, (255,255,0), [self.tiles[0][0]+self.tile_size//2//2,self.tiles[0][1]+self.tile_size//2//2 # yellow
            ,self.tile_size//2,self.tile_size//2])
base_bg = create_base_bg()
base_bg.set()

# place the function here because need the grass image
def loading_screen(phase):
    # background
    grass1 = base_bg.tile[1]
    grass2 = base_bg.tile[2]
    num = 1
    start_at = 1
    for x in range(0,screen_x,base_bg.tile_size):
        for y in range(0,screen_y,base_bg.tile_size):
            if num%2 == 0:
                window.blit(grass1, (x,y))
            else:
                window.blit(grass2, (x,y))
            num += 1
            
        if start_at == 1:
            num = 1
            start_at = 2
        else:
            num = 2
            start_at = 1
    # logo image
    window.blit(game_icon,(screen_x//2-game_icon.get_width()//2, screen_y//2-game_icon.get_height()//2))

    # loading screen text (the num of dots by the phase (phase per dot, phase=1 1 dot, phase=2 2 dots))
    if phase == 1:
        window.blit(bigger_font.render("Loading"+phase*".",True,(0,0,0)),(screen_x//2-bigger_font.size("Loading"+phase*".")[0]//2,screen_y//2-bigger_font.size("Loading"+phase*".")[1]//2))
    elif phase == 2:
        window.blit(bigger_font.render("Loading"+phase*".",True,(0,0,0)),(screen_x//2-bigger_font.size("Loading"+phase*".")[0]//2,screen_y//2-bigger_font.size("Loading"+phase*".")[1]//2))
    elif phase == 3:
        window.blit(bigger_font.render("Loading"+phase*".",True,(0,0,0)),(screen_x//2-bigger_font.size("Loading"+phase*".")[0]//2,screen_y//2-bigger_font.size("Loading"+phase*".")[1]//2))
    
    pygame.display.update()

loading_screen(phase=1)

class create_buildings():
    def __init__(self):
        self.center_tile = base_bg.centered_tile
        tile_size = base_bg.tile_size
        self.buildings_sizes = {
            "townhall":(tile_size*7,tile_size*7),
            "gold mine": (tile_size*5,int(tile_size*5*1.2)),
            "gold storage":(tile_size*6,tile_size*6),
            "iron mine":(tile_size*5,tile_size*5),
            "iron storage":(tile_size*6,tile_size*6),

            "army camp":(tile_size*6,tile_size*6),
            "barracks":(tile_size*5,tile_size*5),
            "the lab":(tile_size*5,int(tile_size*5)), # 576x568  1:0.986

            "lazer tower":(tile_size*5,tile_size*5)
        }

        self.upgrade_btn_size = (int(60*0.6*2),int(60*0.60)) # 666x330 1:0.49 2.018
        self.upgrade_btn = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/upgrade building button.png"),self.upgrade_btn_size)
        self.upgrade_btn_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/upgrade building button mouse on.png"),self.upgrade_btn_size)
        
        self.barracks_train_btn_size = (int(60*0.6*2.13),int(60*0.60)) # 600x281 1:0.46  2.13:1
        self.barracks_train_btn = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/train soldiers button.png"),self.barracks_train_btn_size)
        self.barracks_train_btn_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/train soldiers button mouse on.png"),self.barracks_train_btn_size)
        
        self.info_btn_size = (40,40)
        self.info_btn = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/building info button.png"),self.info_btn_size)
        self.info_btn_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/building info button mouse on.png"),self.info_btn_size)

        self.the_lab_upgrade_soldier_btn_size = (int(40*1.6),40) # 600x360 1:0.6 1.6:1
        self.the_lab_upgrade_soldier_btn = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/upgrade soldiers button.png"),self.the_lab_upgrade_soldier_btn_size)
        self.the_lab_upgrade_soldier_btn_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/upgrade soldiers button mouse on.png"),self.the_lab_upgrade_soldier_btn_size)


        self.buildings_names = return_buildings_names()
        self.buildings_levels = return_buildings_levels()
        
        self.buildings_guns_names = return_buildings_guns_names()
        self.buildings_guns_levels = return_buildings_guns_levels()

        self.buildings_images = {}
        self.buildings_guns_images = {}

        self.collectors_to_take_images = {
            "gold mine": pygame.transform.smoothscale(pygame.image.load(folder + "/gold coin to take money.png"), (tile_size*2, int(tile_size*2*1.5))), # 500x750   1:1.5
            "iron mine":pygame.transform.smoothscale(pygame.image.load(folder + "/iron to take money.png"), (tile_size*2, int(tile_size*2*1.5))), # 500x700 1:1.5
        } # the collectors images of what will be above them to take what they produce
        # in army camp, army camp full sign
        self.full_sign_size = (int(tile_size*2*0.9),tile_size*2)
        self.full_sign = pygame.transform.smoothscale(pygame.image.load(folder+"\\full sign.png"), self.full_sign_size) # 500x530   0.9:1
        self.in_upgrade_cover = {}

        # buildings_costs_data is a variable that is used to store all of the buildings info(cost,cash type...)
        buildings_costs_data = reload_buildings_costs()
        self.building_cost = buildings_costs_data["buildings cost"]
        self.building_cost_cash_type = buildings_costs_data["buildings cash type"]
        self.upgrade_cost = buildings_costs_data["upgrade cost"] # {building name:{level:cost_for_next_level,level:cost_for_next_level...}}
        
        self.max_of_each_building_by_townhall = {
            "1":{
                "gold mine":2,
                "gold storage":1,
                "iron mine":2,
                "iron storage":1,
                "army camp":1,
                "barracks":1,
                "the lab":0,
                "lazer tower":1
            },
            "2":{
                "gold mine":3,
                "gold storage":1,
                "iron mine":3,
                "iron storage":1,
                "army camp":1,
                "barracks":1,
                "the lab":0,
                "lazer tower":2
            },
            "3":{
                "gold mine":4,
                "gold storage":2,
                "iron mine":4,
                "iron storage":2,
                "army camp":2,
                "barracks":2,
                "the lab":1,
                "lazer tower":2
            }
        }

        self.max_upgrade_of_each_building_by_townhall = {} # {building_name:{townhall_level:max_level, "1":"1","2":3}}
        self.upgrade_time = { # in seconds
            'townhall': {
                "1":600, # 10min
                "2":1200, # 20min
                "3":2400, # 40min
                },
            'gold mine': {
                "1":120, # 2min
                "2":300, #5min
                "3": 600, #10min
                },
            "iron mine":{
                "1":120, # 2min
                "2":300, #5min
                "3":600, # 10min
            },
            # storages will be double then the mines(until __ level)
            "gold storage":{
                "1":300, # 5min
                "2":600, # 10min
                "3":900, # 15min
            },
            "iron storage":{
                "1":300, # 5min
                "2":600, # 10min
                "3":900
            },
            "army camp":{
                "1":300, # 5min
                "2":720, # 12 min
            },
            "barracks":{
                "1":300,  # 5min
                "2":900,  # 15 min
                "3":1800, # 30min
            },
            "the lab":{
                "1": 1200, # 20min
            },
            "lazer tower":{

            }
        }
        self.max_buildings_levels = {} # {building_name:level}
        self.max_production = { # max of what it can save without the user taking it
            "gold mine": {
                "1":500,
                "2":700,
                "3":1000,
            },
            "iron mine": {
                "1":500,
                "2":700,
                "3":1000,
            }
        }
        self.produce_per_sec = { # how much of what it produces it gives per sec
            "gold mine": {
                "1":1,
                "2":2,
                "3":4,
            },
            "iron mine": {
                "1":1,
                "2":2,
                "3":4,
            }
        }
        self.max_cash_in_storage_by_storage_level = {
            "gold storage":{
                "1":1000,
                "2":2000,
                "3":3000
            },
            "iron storage":{
                "1":1000,
                "2":2000,
                "3":3000
            }
        }
        self.buildings_info = get_buildings_info()
        self.army_camp_capacity_change_by = 50 # when buying an army camp
        self.army_camp_capacity_add_by_level = {
            # how much capacity is being add to the max army capacity per level
            # for example from level 1-2 20 add
            "1":20, # add in level 1-2
            "2":30, # add in level 2-3
            "3":40, # add in level 3-4
        }
        self.army_camp_capacity_by_level = {
            "1":50,
            "2":70,
            "3":100,
        }
        
        self.buildings_health = {
            "townhall":{
                "1":1000,
                "2":2000,
                "3":4000,
            },
            "gold mine": {
                "1":400,
                "2":800,
                "3":1000,
            },
            "gold storage":{
                "1":500,
                "2":1000,
                "3":1500
            },
            "iron mine":{
                "1":400,
                "2":800,
                "3":1000,
            },
            "iron storage":{
                "1":500,
                "2":1000,
                "3":1500
            },

            "army camp":{
                "1":300,
                "2":500,
                "3":1000,
            },
            "barracks":{
                "1":350,
                "2":600,
                "3":1200,
                "4":2000,
            },
            "the lab":{
                "1":500,
                "2":1200
            },
            "lazer tower":{
                "1":400
            }
        }
        self.attacking_buildings_guns_by_building_name = {
            "lazer tower":"lazer gun"
        }
        self.guns_sizes = {
            "lazer gun":(int(tile_size*1.5),int(tile_size*1.5*3.2))
        }
        self.attacking_buildings_guns_by_gun_name = {}
        for build_name in self.attacking_buildings_guns_by_building_name:
            gun_name = self.attacking_buildings_guns_by_building_name[build_name]
            self.attacking_buildings_guns_by_gun_name[gun_name] = build_name

        self.attacking_buildings_guns = {} # like the buildings dict: {gun name:{level:image...}}

        # buildings_images
        # max_buildings_levels
        # in_upgrade_cover
        index = 0
        for name in self.buildings_names:
            self.buildings_images[name] = {}
            self.max_buildings_levels[name] = self.buildings_levels[index]
            for level in range(1,self.buildings_levels[index]+1):
                self.buildings_images[name][str(level)] = pygame.transform.smoothscale(pygame.image.load(folder + f"/buildings/{name}/{str(level)}.png").convert_alpha(), self.buildings_sizes[name])
                self.in_upgrade_cover[name] = pygame.transform.smoothscale(pygame.image.load(folder + f"/in upgrade cover.png").convert_alpha(), self.buildings_sizes[name])
            index += 1
        
        # buildings guns
        index = 0
        for building_gun_name in self.buildings_guns_names:
            self.buildings_guns_images[building_gun_name] = {}
            for level in range(self.buildings_guns_levels[index]):
                level += 1
                path = folder + f"/buildings guns/{building_gun_name}/{str(level)}.png"
                self.buildings_guns_images[building_gun_name][str(level)] = pygame.transform.smoothscale(pygame.image.load(path).convert_alpha(),self.guns_sizes[building_gun_name])

            index += 1

        # max upgrade by townhall
        index = 0
        max_townhall_level = self.buildings_levels[self.buildings_names.index("townhall")]
        for name in self.buildings_names:
            self.max_upgrade_of_each_building_by_townhall[name] = {} # {townhall_level:level}
            max_upgrade = self.buildings_levels[index]
            for level in range(1,max_upgrade+1):
                if max_townhall_level >= level:
                    self.max_upgrade_of_each_building_by_townhall[name][str(level)] = str(level)
                elif max_townhall_level < level:
                    # if the building upgrade is above the townhall upgrade then the max upgrade of this building will be in the max level of the townhall
                    self.max_upgrade_of_each_building_by_townhall[name][str(max_townhall_level)] = str(level)
            index += 1

        # set the special building levels by townhall
        self.max_upgrade_of_each_building_by_townhall["the lab"] = {
            "1":0,
            "2":0,
            "3":1,
            "4":2,
        }
        
        self.buildings = reload_buildings()# [building,building] => [id:{building name:name, pos:(x,y), level:level}](id because there will be a few of the same type)

        self.on_building = None # the current building the user is pressing on
        self.moving_buildings = {} # can only be 1 in at per time(built like the self.buildings values)(built like this in case i want to do a few in a time)
        self.building_start_moving_pos = {} # the position when pressed to move the building # can only be 1 in at per time(built like the self.buildings values)(built like this in case i want to do a few in a time)
        self.upgrade_building = reload_in_upgrade_buildings() # {"id":id, "finish time": time.time() object}
        self.in_building_info_screen = False
        self.in_building_info_screen_building = None # the id of this building

        self.army_camp_for_soldiers_info = [] # stores all of the army camps info(the building info)
        self.army_camp_moving_soldiers = [] # [soldier dict,soldier dict] => {'name': 'rock machine', 'level': 1, 'capacity': 7, 'angle': 30, 'pos': (361.1672955930054, 471.5), 'in camp': '12'}

    def draw_buildings(self,draw_moving_building = True, back_tile_color = "g", check_mouse_press = False): # draw ALL of the buildings(any type)
        """back_tile_color is a parameter for the green/red tiles behind the building
        red-can't place (r-red)
        green-can place (g-green)"""
        
        in_upgrade_times_text_to_show = [] # [time,sec/min/hour,(x,y)]
        for building in self.buildings:
            id = building
            if id not in self.moving_buildings:
                building = self.buildings[id]
                name = building["building name"]
                pos = building["pos"]
                level = building["level"]
                image2 = self.buildings_images[name][level]
                window.blit(
                    image2, pos
                )
                # collector
                if name in self.collectors_to_take_images:
                    show_cash_above_img = False
                    if building["time to produce"] <= time.time():
                        if building["money produced"] < self.max_production[name][level]:
                            building["money produced"] += self.produce_per_sec[name][level]
                        building["time to produce"] = time.time() + 1
                    if building["money produced"] > 100: # show the collector get sign above the building
                        image = self.collectors_to_take_images[name]
                        window.blit(image, (pos[0]+image2.get_width()//2-image.get_width()//2,pos[1]+image2.get_height()//2-image.get_height()))
                        show_cash_above_img = True
                        
                    if show_cash_above_img == True:
                        if "gold" in name and user.gold == user.max_gold \
                            or "iron" in name and user.iron == user.max_iron \
                            or "diamonds" in name and user.diamonds == user.max_diamonds:
                            draw_transparent_square(window,(image.get_width(),40),100,(150,0,0),(pos[0]+image2.get_width()//2-image.get_width()//2,pos[1]+image2.get_height()//2-image.get_height()))
                # attack building
                if name in self.attacking_buildings_guns_by_building_name:
                    gun_name = self.attacking_buildings_guns_by_building_name[name]
                    angle = building["gun angle"]
                    gun_image = pygame.transform.rotate(self.buildings_guns_images[gun_name][level],angle)
                    gun_pos = (pos[0] + image2.get_width()//2-gun_image.get_width()//2,pos[1] + image2.get_height()//2-gun_image.get_height()//2)
                    window.blit(gun_image,gun_pos)
                # army camp
                # barracks
                if army.capacity == army.max_capacity:
                    if name == "army camp" or name == "barracks":
                        width = self.buildings_sizes[name][0]
                        sign_height = self.full_sign_size[1]
                        x,y = pos[0]+width//2-self.full_sign_size[0]//2,pos[1]-sign_height//2
                        window.blit(self.full_sign, (x,y))
                if name == "army camp":
                    self.store_army_camp_info(building,id)
                if name == "the lab":
                    if the_lab_screen.soldiers == {}:
                        the_lab_screen.set_soldiers_dict()
                    for soldier_name in the_lab_screen.soldiers:
                        soldier = the_lab_screen.soldiers[soldier_name]
                        if army.soldier_in_upgrade != None and soldier["name"] == army.soldier_in_upgrade["name"]:
                            finish_time = army.soldier_in_upgrade["finish time"]
                            time_left = finish_time - time.time()
                            time_text = ""
                            hours = int(time_left//60//60)
                            minutes = int(time_left//60 % 60)
                            seconds = int(time_left % 60)
                            
                            if hours != 0:
                                time_text = str(hours)+":"+str(minutes)+":"+str(seconds)
                            else:
                                if minutes < 10:
                                    minutes = "0"+str(minutes)
                                if seconds < 10:
                                    seconds = "0"+str(seconds)
                                if minutes != 0 and minutes != "00":
                                    time_text = str(minutes)+":"+str(seconds)
                                else:
                                    time_text = str(seconds)+"sec"
                            text_pos = (pos[0] + self.buildings_sizes[name][0]//2 - medium_font.size(time_text)[0]//2,pos[1] - medium_font.size("S")[1]*1.1)
                            window.blit(medium_font.render(time_text,True,(0,0,0)),text_pos)
                            break
                # in upgrade building
                if self.upgrade_building != None and id == self.upgrade_building["id"]:
                    window.blit(self.in_upgrade_cover[name], pos) # draw the cover
                    # draw the time above the building
                    now = time.time()
                    time_left = int(self.upgrade_building["finish time"] - now)
                    time_left2 = None
                    time_type = "" # sec
                    if time_left > 60: # sec => min
                        time_left = time_left // 60
                        time_type = "min"
                    if time_left > 60: # min => hour
                        time_left2 = time_left%60# minutes
                        time_left = time_left // 60
                        time_type = "h"
                    if time_left2 == None:
                        to_append = [str(time_left),time_type,(pos[0]+self.buildings_sizes[name][0]//2-font.size("time: "+str(time_left))[0]//2,pos[1]-font.size("t")[1]*1.5)]
                        in_upgrade_times_text_to_show.append(to_append)
                        #window.blit(font.render("time: "+str(time_left) + time_type,True,(0,0,0)),(pos[0]+self.buildings_sizes[name][0]//2-font.size("time: "+str(time_left))[0]//2,pos[1]-font.size("t")[1]*1.5))
                    else:
                        to_append = [str(time_left) + time_type+" "+str(time_left2)+"min","",(pos[0]+self.buildings_sizes[name][0]//2-font.size("time: "+str(time_left))[0]//2,pos[1]-font.size("t")[1]*1.5)]
                        in_upgrade_times_text_to_show.append(to_append)
                        #window.blit(font.render("time: "+str(time_left) + time_type+" "+str(time_left2)+"min",True,(0,0,0)),(pos[0]+self.buildings_sizes[name][0]//2-font.size("time: "+str(time_left))[0]//2,pos[1]-font.size("t")[1]*1.5))
        # draw the times above all of the buildings(in case the user puts a building on the position that the time left text is on)
        for time_list in in_upgrade_times_text_to_show:
            time_left,time_type,pos = time_list
            window.blit(font.render("time: "+time_left+time_type,True,(0,0,0)),pos)

        if draw_moving_building == True:
            for building in self.moving_buildings:
                id = building
                building = self.buildings[id]
                name = building["building name"]
                pos = building["pos"]
                level = building["level"]
                size = self.buildings_sizes[name]
                color1 = (118,238,0) # not the border
                color2 = (0,255,0) # the border
                if back_tile_color == "r":
                    color1 = (200,0,0)
                    color2 = (255,0,0)
                for square in range(size[0]//base_bg.tile_size):
                    for square2 in range(size[1]//base_bg.tile_size):
                        pygame.draw.rect(window, color1, [pos[0]+square*base_bg.tile_size,   pos[1]+square2*base_bg.tile_size,base_bg.tile_size-1,base_bg.tile_size-1]) # back square
                        pygame.draw.rect(window, color2, [pos[0]+square*base_bg.tile_size,   pos[1]+square2*base_bg.tile_size,base_bg.tile_size-1,base_bg.tile_size-1],1) # border square
                window.blit(
                    self.buildings_images[name][level], pos
                )
                if name in self.attacking_buildings_guns_by_building_name:
                    gun_name = self.attacking_buildings_guns_by_building_name[name]
                    angle = building["gun angle"]
                    gun_image = pygame.transform.rotate(self.buildings_guns_images[gun_name][level],angle)
                    angle_change_pos_needed = building["angle change pos needed"]
                    gun_pos = (pos[0] - angle_change_pos_needed ,pos[1] - angle_change_pos_needed)
                    window.blit(gun_image,gun_pos)
        
        # handles the soldiers on the army camp
        self.draw_move_soldiers_on_army_camp()
        self.army_camp_for_soldiers_info = []

        # draw it here for it to be above the townhall
        if self.on_building != None:
            self.draw_on_building(check_mouse_press)
        
        draw_moving_building = True
        back_tile_color = "g" # return the parameter to its basic form
        check_mouse_press = False
    def store_army_camp_info(self,building,id): # used in the function draw_buildings
        self.army_camp_for_soldiers_info.append([building,id])

    def move_soldiers_by_angle(self,old_xy,speed,angle):
        angle = math.radians(angle)
        new_x = old_xy[0] + (speed*math.cos(angle))
        new_y = old_xy[1] + (speed*math.sin(angle))
        return new_x, new_y
    def draw_move_soldiers_on_army_camp(self): # called in self.draw_buildings()
        if army.soldiers_in_camp != {}:
            num_of_army_camps = len(self.army_camp_for_soldiers_info)
            soldiers_to_show = [] # gets the info of the soldiers in one line
            for i in army.soldiers_in_camp:
                soldiers_to_show.append(army.soldiers_in_camp[i])
            if num_of_army_camps == 0:
                num_of_army_camps = 1
            break_after_n_soldiers = len(soldiers_to_show)//num_of_army_camps
            if self.army_camp_moving_soldiers == []:
                for num in range(num_of_army_camps):
                    for soldier in soldiers_to_show:
                        # "removes" the first one
                        # cant do .remove() because every soldier dict from the same type looks the same (every soldier type looks the same)
                        if soldier["name"] != "bomb" and soldier["name"] != "missile":
                            self.army_camp_moving_soldiers.append(soldier)
                            soldier["angle"] = random.randint(0,360)
                            army_camp_pos = self.army_camp_for_soldiers_info[num][0]["pos"]
                            name = soldier["name"]
                            soldier["pos"] = (random.randint(army_camp_pos[0],army_camp_pos[0]+buildings.buildings_sizes["army camp"][0]-army.army_images_sizes[name][0]),   random.randint(army_camp_pos[1],army_camp_pos[1]+buildings.buildings_sizes["army camp"][1]-army.army_images_sizes[name][1]) )
                            soldier["in camp"] = self.army_camp_for_soldiers_info[num][1] # stores the id
                            soldiers_to_show = soldiers_to_show[1:]
                            if len(soldiers_to_show) == 0 or len(soldiers_to_show) % break_after_n_soldiers == 0: # if removed the num of soldiers it needed to
                                # moves to the next iteration of the range() loop
                                break
            else:
                index = 0
                for soldier in self.army_camp_moving_soldiers: # soldier => (thats one option) {'name': 'killer drone', 'level': 1, 'capacity': 5, 'angle': 343, 'pos': (381, 366)}
                    name = soldier["name"]
                    level = soldier["level"]
                    pos = soldier["pos"]
                    angle = soldier["angle"]

                    in_army_camp = soldier["in camp"]
                    army_camp_pos = self.buildings[in_army_camp]["pos"]

                    image = pygame.transform.rotate(army.army_images[name][str(level)],angle)
                    window.blit(image, pos)

                    new_pos = attack.move_by_angle_and_speed(pos,1,angle)
                    self.army_camp_moving_soldiers[index]["pos"] = new_pos
                    if new_pos[0] < army_camp_pos[0] or new_pos[0] + army.army_images_sizes[name][0] > army_camp_pos[0] + buildings.buildings_sizes["army camp"][0] or \
                        new_pos[1] < army_camp_pos[1] or new_pos[1] + army.army_images_sizes[name][1] > army_camp_pos[1] + buildings.buildings_sizes["army camp"][1]:
                        angle += 180
                    
                    self.army_camp_moving_soldiers[index]["angle"] = angle
                    index += 1


    def handle_mouse(self): # check if pressed on a building(happen when pressing left mouse btn)
        mouse = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)
        updated = False
        for building in self.buildings:
            id = building
            building = self.buildings[id]
            name = building["building name"]
            x,y = building["pos"]
            level = building["level"]
            size = self.buildings_sizes[name]
            building_rect = pygame.Rect(x,y,size[0],size[1])
            if building_rect.colliderect(mouse_rect) and self.moving_buildings == {}:
                # append the type of money to the variable in the user class
                collected_cash = False
                money_at_start = {"gold":user.gold,"iron":user.iron,"diamonds":user.diamonds}
                if name == "gold mine":
                    if user.gold != user.max_gold and name in self.collectors_to_take_images and building["money produced"] > 100:
                        self.collect_all_gold() # calls a function that takes all of the gold
                        collected_cash = True
                    else:
                        self.on_building = id
                        updated = True
                elif name == "iron mine":
                    if user.iron != user.max_iron and name in self.collectors_to_take_images and building["money produced"] > 100:
                        self.collect_all_iron() # calls a function that takes all of the iron
                        collected_cash = True
                    else:
                        self.on_building = id
                        updated = True
                elif name == "diamonds mine":
                    if user.diamonds != user.max_diamonds and name in self.collectors_to_take_images and building["money produced"] > 100:
                        self.collect_all_diamonds() # calls a function that takes all of the diamonds
                        collected_cash = True
                    else:
                        self.on_building = id
                        updated = True
                else:
                    self.on_building = id
                    updated = True

                if collected_cash == True:
                    money_now = {"gold":user.gold,"iron":user.iron,"diamonds":user.diamonds}
                    money_type = name.split(" ")[0]
                    money_earned = money_now[money_type] - money_at_start[money_type]
                    collect_money_effect.append(money_type,money_earned)
                break
        if updated == False:
            self.on_building = None
    
    def collect_all_gold(self):
        for building in self.buildings:
            id = building
            building = self.buildings[id]
            name = building["building name"]
            # append the type of money to the variable in the user class
            if name == "gold mine":
                if user.gold != user.max_gold and name in self.collectors_to_take_images and building["money produced"] > 100:
                    user.gold += building["money produced"]
                    building["money produced"] = 0
                    if user.gold > user.max_gold:
                        building["money produced"] = user.gold - user.max_gold
                        user.gold = user.max_gold
    def collect_all_iron(self):
        for building in self.buildings:
            id = building
            building = self.buildings[id]
            name = building["building name"]
            # append the type of money to the variable in the user class
            if name == "iron mine":
                if user.iron != user.max_iron and name in self.collectors_to_take_images and building["money produced"] > 100:
                    user.iron += building["money produced"]
                    building["money produced"] = 0
                    if user.iron > user.max_iron:
                        building["money produced"] = user.iron - user.max_iron
                        user.iron = user.max_iron
    def collect_all_diamonds(self):
        for building in self.buildings:
            id = building
            building = self.buildings[id]
            name = building["building name"]
            # append the type of money to the variable in the user class
            if name == "diamonds mine":
                if user.diamonds != user.max_diamonds and name in self.collectors_to_take_images and building["money produced"] > 100:
                    user.diamonds += building["money produced"]
                    building["money produced"] = 0
                    if user.diamonds > user.max_diamonds:
                        building["money produced"] = user.diamonds - user.max_diamonds
                        user.diamonds = user.max_diamonds
    
    def draw_on_building(self,with_press_check = False): # in draw_buildings() func ,draw the building the user is on right now and check if pressed to move its position
        # in draw_buildings function
        id = self.on_building
        building = self.buildings[id]
        name = building["building name"]
        level = building["level"]
        x,y = building["pos"]
        width,height = self.buildings_sizes[name]
        window.blit(font.render(name+" "+str(level),True, (0,255,0)),(x+width//2-font.size(name+" "+str(level))[0]//2 ,y-font.size(name+" "+str(level))[1]))
        window.blit(font.render("press r to move",True, (0,0,0)),(x+width//2-font.size("press r to move")[0]//2,y+height))

        # ALL OF THE BUTTONS HAVE THE SAME y so instead of doing the full code of this just do the_lab_button_pos[1]

        the_lab_button_pos = (x+width//2-self.the_lab_upgrade_soldier_btn_size[0]//2,y+height+font.size("p")[1])
        the_lab_button_size = (very_small_font.size("Upgrade")[0]*1.1,40)
        
        train_soldiers_button_pos = (x+width//2-self.barracks_train_btn_size[0]//2,the_lab_button_pos[1])
        

        # info btn (!)(blitting the button after the big if)
        info_btn_pos = (x,the_lab_button_pos[1])
        
        mouse = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()
        # only if the user is not upgrading this building he can make changes
        if self.upgrade_building == None or self.upgrade_building != None and self.upgrade_building["id"] != id: # if there is no building that is in upgrade
            # if can upgrade
            if int(self.buildings[id]["level"]) < self.max_buildings_levels[name]: # if can upgrade
                upgrade_btn_pos = info_btn_pos[0]+self.info_btn_size[0]+5,info_btn_pos[1]

                # upgrade button of the barracks
                if name == "barracks":
                    # upgrade btn
                    upgrade_btn_pos = (
                        x+width//2-self.barracks_train_btn_size[0]//2 + self.barracks_train_btn_size[0]+5
                        ,info_btn_pos[1]
                    )
                    window.blit(self.upgrade_btn, upgrade_btn_pos)
                    train_soldiers_button_pos = (x+width//2-self.barracks_train_btn_size[0]//2,info_btn_pos[1])
                elif name == "the lab":
                    # upgrade btn
                    upgrade_btn_pos = (
                        the_lab_button_pos[0] + the_lab_button_size[0]+10 ,
                        the_lab_button_pos[1]
                    )
                    window.blit(self.upgrade_btn, upgrade_btn_pos)
                else:
                    window.blit(self.upgrade_btn, upgrade_btn_pos)

                # the hover effect of the upgrade button
                button_rect = pygame.Rect(upgrade_btn_pos[0],upgrade_btn_pos[1],self.upgrade_btn_size[0],self.upgrade_btn_size[1])
                if button_rect.collidepoint(mouse):
                    window.blit(self.upgrade_btn_mouse_on,upgrade_btn_pos)

                if mouse_buttons[0] == True: # left button
                    upgrade_btn_rect = pygame.Rect(upgrade_btn_pos[0],upgrade_btn_pos[1],self.upgrade_btn_size[0],self.upgrade_btn_size[1])
                    if name != "barracks":
                        # upgrade btn
                        if upgrade_btn_rect.collidepoint(mouse):
                            upgrade_building_screen.on_building = self.on_building
                            upgrade_building_screen.in_building_upgrade_screen = True
                            # the upgrade itself checks are in upgrade_building_screen class
                    elif name == "barracks":
                        # doing in try:except in case it wont be in the name == barracks if statement and the pos variable wont define
                        try:
                            if upgrade_btn_rect.collidepoint(mouse):
                                upgrade_building_screen.on_building = self.on_building
                                upgrade_building_screen.in_building_upgrade_screen = True
                                # the upgrade itself checks are in upgrade_building_screen class
                        except:pass

            # if its barracks/the lab it will draw the train btn
            # also fixing the info button pos by the name of the building
            if name == "barracks":
                window.blit(self.barracks_train_btn, train_soldiers_button_pos)
                info_btn_pos = (train_soldiers_button_pos[0]-self.info_btn_size[0]-5,the_lab_button_pos[1])
            elif name == "the lab":
                window.blit(self.the_lab_upgrade_soldier_btn,the_lab_button_pos)
                info_btn_pos = (the_lab_button_pos[0]-self.info_btn_size[0]-5,the_lab_button_pos[1])
            
            if with_press_check == True:
                if name == "barracks" or name == "the lab":
                    if mouse_buttons[0] == True: # left btn
                        the_lab_button_rect = pygame.Rect(the_lab_button_pos[0],the_lab_button_pos[1],the_lab_button_size[0],the_lab_button_size[1])
                        train_button_rect = pygame.Rect(train_soldiers_button_pos[0],train_soldiers_button_pos[1],self.barracks_train_btn_size[0],self.barracks_train_btn_size[1])
                        if name == "barracks" and train_button_rect.collidepoint(mouse):
                            if barracks_screen.in_barracks_screen == False:
                                barracks_screen.in_barracks_screen = True
                        elif name == "the lab" and the_lab_button_rect.collidepoint(mouse):
                            the_lab_screen.in_the_lab_screen = True

        # info btn blitting
        if info_btn_pos[0] != None:
            window.blit(self.info_btn,info_btn_pos)

        # keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            self.moving_buildings = {self.on_building:self.buildings[self.on_building]}
            self.building_start_moving_pos = {self.on_building:self.buildings[self.on_building]["pos"]}
            self.on_building = None
        if keys[pygame.K_ESCAPE] or keys[pygame.K_RETURN]:
            self.on_building = None
        
        # the hover effect of the info,train soldiers,upgrade soldiers buttons
        info_btn_rect = pygame.Rect(info_btn_pos[0],info_btn_pos[1], self.info_btn_size[0],self.info_btn_size[1])
        if info_btn_rect.collidepoint(mouse):
            window.blit(self.info_btn_mouse_on,info_btn_pos)
        if name == "barracks":
            train_button_rect = pygame.Rect(train_soldiers_button_pos[0],train_soldiers_button_pos[1],self.barracks_train_btn_size[0],self.barracks_train_btn_size[1])
            if train_button_rect.collidepoint(mouse):
                window.blit(self.barracks_train_btn_mouse_on,train_soldiers_button_pos)
        if name == "the lab":
            upgrade_soldiers_btn_rect = pygame.Rect(the_lab_button_pos[0],the_lab_button_pos[1],self.the_lab_upgrade_soldier_btn_size[0],self.the_lab_upgrade_soldier_btn_size[1])
            if upgrade_soldiers_btn_rect.collidepoint(mouse):
                window.blit(self.the_lab_upgrade_soldier_btn_mouse_on,the_lab_button_pos)

        # does that if the user is pressing on anywhere that is not on the current building the on_building variable will turn to None and the user wont be on any building
        # info btn, out of building check
        pressed_mouse = pygame.mouse.get_pressed()
        if pressed_mouse[0] == True:
            building_rect = pygame.Rect(x,y,width,height)
            if not building_rect.collidepoint(mouse):
                self.on_building = None
            if info_btn_rect.collidepoint(mouse):
                self.in_building_info_screen = True
                self.in_building_info_screen_building = id
        with_press_check = False
    def draw_building_info_screen(self):
        width,height = upgrade_building_screen.min_window_size
        x,y = upgrade_building_screen.min_win_x,upgrade_building_screen.min_win_y
        window.blit(upgrade_building_screen.min_window_image,(x,y))

        esc_button_size = (bigger_font.size("X")[1]+2,bigger_font.size("X")[1]+2)
        esc_button_pos = (x+width-esc_button_size[0]-5,y+5)
        pygame.draw.rect(window, (200,0,0),[esc_button_pos[0],esc_button_pos[1],esc_button_size[0],esc_button_size[1]])
        pygame.draw.rect(window, (255,64,64),[esc_button_pos[0]-2,esc_button_pos[1]-2,esc_button_size[0]+3,esc_button_size[1]+3],2)
        window.blit(bigger_font.render("X",True,(255,255,255)), (esc_button_pos[0]+esc_button_size[0]//2-bigger_font.size("X")[0]//2,esc_button_pos[1]+esc_button_size[1]//2-bigger_font.size("X")[1]//2))

        start_x,start_y = x + bigger_font.size("p")[0],y + bigger_font.size("p")[1]

        # the info the user sees
        building = self.buildings[self.in_building_info_screen_building]
        name = building["building name"]
        level = building["level"]
        window.blit(bigger_font.render(name+" "+level,True,(0,0,0)),(start_x+width//2-bigger_font.size(name+" "+level)[0]//2,start_y+5))
        description = self.buildings_info[name]["description"]
        building_info = description.split("\n")
        # changing the start x,y because of the image border
        x1 = start_x+bigger_font.size("p")[0] # x of the text(not changing)
        y1 = start_y+bigger_font.size("p")[1]*3 # y on the text(changing in the loop)
        for info in building_info:
            window.blit(font.render(info,True,(0,0,0)),(x1,y1))
            y1 += font.size("p")[1]*1.5
    def handle_mouse_in_building_info_screen(self):
        pressed_mouse = pygame.mouse.get_pressed()
        if pressed_mouse[0] == True:
            mouse = pygame.mouse.get_pos()
            width,height = upgrade_building_screen.min_window_size
            x,y = upgrade_building_screen.min_win_x,upgrade_building_screen.min_win_y
            esc_button_size = (bigger_font.size("X")[1]+2,bigger_font.size("X")[1]+2)
            esc_button_pos = (x+width-esc_button_size[0]-5,y+5)
            esc_button_rect = pygame.Rect(esc_button_pos[0],esc_button_pos[1],esc_button_size[0],esc_button_size[1])
            mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)
            if esc_button_rect.colliderect(mouse_rect):
                self.in_building_info_screen = False
                self.in_building_info_screen_building = None
    def handle_in_upgrade_building(self):
        if self.upgrade_building != None:
            id = self.upgrade_building["id"]
            finish_time = self.upgrade_building["finish time"]
            now = time.time()
            time_left = finish_time-now
            if time_left <= 0:
                self.buildings[id]["level"] = str(int(self.buildings[id]["level"]) +1)
                self.upgrade_building = None
                building = self.buildings[id]
                name = building["building name"]
                level = building["level"]
                if name in self.max_production: # a collector
                    building["max money"] = self.max_production[name][level]
                    building["money per sec"] = self.produce_per_sec[name][level]
                if name in self.max_cash_in_storage_by_storage_level: # if a storage
                    max_now = self.max_cash_in_storage_by_storage_level[name][str(int(level)-1)]
                    should_be_max_now = self.max_cash_in_storage_by_storage_level[name][level]
                    add_to_cash = should_be_max_now - max_now
                    if "gold" in name:
                        user.max_gold += add_to_cash
                    elif "iron" in name:
                        user.max_iron += add_to_cash
                    else: # diamonds
                        user.max_diamonds += add_to_cash
                if name == "army camp":
                    army.max_capacity += self.army_camp_capacity_add_by_level[str(int(level)-1)]
                if name == "barracks":
                    if int(barracks_screen.user_highest_barracks_level) < int(level):
                        barracks_screen.user_highest_barracks_level += 1
                if name == "the lab":
                    the_lab_screen.lab_level += 1
                show_notification(name,name+" upgraded to level "+ str(level))
                save_buildings(self.buildings)
                save_in_upgrade_buildings(self.upgrade_building)
                shop.set_buildings_to_buy_dict() # max of a lot of things may change
                user.save_cash_methods()
    def handle_collectors_money_after_reload(self):
        for building in self.buildings:
            id = building
            building = self.buildings[id]
            name = building["building name"]
            x,y = building["pos"]
            level = building["level"]
            if self.upgrade_building == None or self.upgrade_building != None and id != self.upgrade_building["id"]:
                if name in self.collectors_to_take_images:
                    time_passed = time.time() - building["time to produce"]
                    building["money produced"] += int(time_passed)
                    if building["money produced"] > self.max_production[name][level]:
                        building["money produced"] = self.max_production[name][level]
                    building["time to produce"] = time.time()+1

    def move_moving_building(self): # press escape/enter = stop moving this building, move the building
        keys = pygame.key.get_pressed()
        can_place = True
        try:
            building = self.moving_buildings[list(self.moving_buildings)[0]]
            building_rect = pygame.Rect(building["pos"][0],building["pos"][1], self.buildings_sizes[building["building name"]][0],self.buildings_sizes[building["building name"]][1])
            for build in self.buildings:
                id = build
                if id != list(self.moving_buildings)[0]:
                    build = self.buildings[id]
                    x,y = build["pos"]
                    width,height = self.buildings_sizes[build["building name"]]
                    build_rect = pygame.Rect(x,y,width,height)
                    if building_rect.colliderect(build_rect):
                        can_place = False
        except: pass
        if keys[pygame.K_ESCAPE] or keys[pygame.K_RETURN]: # place the building at its final pos
            if can_place == True and self.moving_buildings != {}:
                self.on_building = list(self.moving_buildings)[0]
                self.moving_buildings = {}
                save_buildings(self.buildings)
        
        after_change_pos = None # x,y of the moving building for the under text
        if self.moving_buildings != {}: # move the building
            # move with the arrows text under the building
            building = self.moving_buildings[list(self.moving_buildings)[0]]
            x,y = building["pos"]
            width,height = self.buildings_sizes[building["building name"]]
            after_change_pos = (x,y) # updates the x,y
            
            x_change = 0
            y_change = 0
            # that actual movement
            if keys[pygame.K_LEFT]: # left
                x -= base_bg.tile_size
                x_change -= base_bg.tile_size
            elif keys[pygame.K_RIGHT]: # right
                x += base_bg.tile_size
                x_change += base_bg.tile_size
            elif keys[pygame.K_UP]: # up
                y -= base_bg.tile_size
                y_change -= base_bg.tile_size
            elif keys[pygame.K_DOWN]: # down
                y += base_bg.tile_size
                y_change += base_bg.tile_size
            update = True
            if x < base_bg.tiles[1][0]:
                update = False
            elif x + width > base_bg.tiles[-1][0]+base_bg.tile_size:
                update = False
            elif y < base_bg.tiles[1][1]:
                update = False
            elif y + height + small_font.size("m")[1] > base_bg.tiles[-1][1]+base_bg.tile_size:
                update = False
            if update == True:
                after_change_pos = (x,y) # updates the x,y
                self.buildings[list(self.moving_buildings)[0]]["pos"] = (x,y)
                self.moving_buildings = {list(self.moving_buildings)[0]:self.buildings[list(self.moving_buildings)[0]]}
                if building["building name"] == "army camp":
                    for soldier in self.army_camp_moving_soldiers:
                        #{'name': 'rock machine', 'level': 1, 'capacity': 7, 'angle': 30, 'pos': (361.1672955930054, 471.5), 'in camp': '12'}
                        if list(self.moving_buildings)[0] == soldier["in camp"]:
                            soldier_x,soldier_y = soldier["pos"]
                            soldier_x += x_change
                            soldier_y += y_change
                            soldier["pos"] = (soldier_x,soldier_y)
        if can_place == False: # after the change and all
            self.draw_buildings(True,"r")
        else:
            self.draw_buildings()
        if after_change_pos != None: # draw the under text
            window.blit(small_font.render("move with the arrows",True,(0,0,0)),(after_change_pos[0]+width//2-small_font.size("move with the arrows")[0]//2,after_change_pos[1]+height))
    def check_on_building_valid_pos(self): # check if that building can be in that position(call when closing the game)
        if self.moving_buildings != {}:
            on_building = list(self.moving_buildings)[0]
            valid_pos = True
            on_building_rect = pygame.Rect(self.moving_buildings[on_building]["pos"][0],self.moving_buildings[on_building]["pos"][1],self.buildings_sizes[self.buildings[on_building]["building name"]][0],self.buildings_sizes[self.buildings[on_building]["building name"]][1])
            for build_id in self.buildings:
                if build_id == self.on_building:
                    continue # move for the next iteration
                else:
                    building = self.buildings[build_id]
                    build_rect = pygame.Rect(building["pos"][0],building["pos"][1],self.buildings_sizes[building["building name"]][0],self.buildings_sizes[building["building name"]][1])
                    if on_building_rect.colliderect(build_rect):
                        print("Position is not valid")
                        try:
                            print("Building has been returned to his past position:",self.building_start_moving_pos[on_building])
                        except KeyError:
                            pass
                        valid_pos = False
                        break

            if valid_pos == False:
                if self.buildings[on_building]["building name"] in self.building_start_moving_pos:
                    self.buildings[on_building]["pos"] = self.building_start_moving_pos[on_building]
                else:
                    if self.buildings[on_building]["building name"] not in self.building_start_moving_pos: # return the money
                        building = self.buildings[on_building]
                        building_cost = self.building_cost[building["building name"]]
                        cost_type = self.building_cost_cash_type[building["building name"]]
                        if cost_type == "iron":
                            user.iron += building_cost
                        elif cost_type == "gold":
                            user.gold += building_cost
                        elif cost_type == "diamonds":
                            user.diamonds += building_cost
                        if user.iron > user.max_iron:
                            user.iron = user.max_iron
                        elif user.gold > user.max_gold:
                            user.gold = user.max_gold
                        elif user.diamonds > user.max_diamonds:
                            user.diamonds = user.max_diamonds
                    self.buildings.pop(on_building)
                    self.moving_buildings = {}
buildings = create_buildings()
buildings.handle_collectors_money_after_reload()

loading_screen(phase=2)

class create_upgrade_building_screen():
    def __init__(self):
        self.in_building_upgrade_screen = False
        self.on_building = None
        self.min_window_size = (screen_y//3*2,screen_y//3*2)
        self.min_win_x,self.min_win_y = (screen_x//2-self.min_window_size[0]//2,   screen_y//2-self.min_window_size[1]//2)
        self.min_window_image = pygame.transform.smoothscale(pygame.image.load(folder+"/screens min window.png"),self.min_window_size)

        self.esc_button_size = (bigger_font.size("X")[1]+2,bigger_font.size("X")[1]+2)
        self.esc_button_pos = (self.min_win_x+self.min_window_size[0]-self.esc_button_size[0]-10,self.min_win_y+5)
        self.esc_button_rect = pygame.Rect(self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1])
        
        self.upgrade_btn_size = (60,60)
        self.upgrade_btn = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/upgrade building cost button background.png"),self.upgrade_btn_size)
        self.upgrade_btn_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/upgrade building cost button background mouse on.png"),self.upgrade_btn_size)
        self.upgrade_btn_pos = (self.min_win_x+self.min_window_size[0]//2-self.upgrade_btn_size[0]//2, self.min_win_y+self.min_window_size[1]-font.size("p")[1]-self.upgrade_btn_size[1])
        self.upgrade_btn_rect = pygame.Rect(self.upgrade_btn_pos[0],self.upgrade_btn_pos[1],self.upgrade_btn_size[0],self.upgrade_btn_size[1])

        self.buildings_image_sizes = buildings.buildings_sizes
        self.buildings_images = {}
        self.buildings_guns_images = {}
        index = 0
        for name in buildings.buildings_names:
            self.buildings_images[name] = {}
            for level in range(1,buildings.buildings_levels[index]+1):
                self.buildings_images[name][str(level)] = pygame.transform.smoothscale(pygame.image.load(folder + f"/buildings/{name}/{str(level)}.png").convert_alpha(), self.buildings_image_sizes[name])
                if name in buildings.attacking_buildings_guns_by_building_name:
                    gun_name = buildings.attacking_buildings_guns_by_building_name[name]
                    if gun_name not in self.buildings_guns_images:
                        self.buildings_guns_images[gun_name] = {}
                    image = buildings.buildings_guns_images[gun_name][str(level)]
                    new_img = pygame.transform.smoothscale(image,self.buildings_images[name][str(level)].get_size())
                    self.buildings_guns_images[gun_name][str(level)] = new_img
            index += 1
            
    def draw_screen(self):
        # the screen itself
        win_x,win_y = self.min_win_x,self.min_win_y # easier to get in function
        window.blit(self.min_window_image,(win_x,win_y))

        # esc btn
        pygame.draw.rect(window, (200,0,0),[self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1]])
        pygame.draw.rect(window, (255,64,64),[self.esc_button_pos[0]-2,self.esc_button_pos[1]-2,self.esc_button_size[0]+3,self.esc_button_size[1]+3],2)
        window.blit(bigger_font.render("X",True,(255,255,255)), (self.esc_button_pos[0]+self.esc_button_size[0]//2-bigger_font.size("X")[0]//2,self.esc_button_pos[1]+self.esc_button_size[1]//2-bigger_font.size("X")[1]//2))
        
        start_x = win_x + bigger_font.size("p")[0]
        start_y = win_y + bigger_font.size("p")[1]

        # everything else
        building = buildings.buildings[self.on_building]
        name = building["building name"]
        level = building["level"]
        window.blit(bigger_font.render("Upgrade to level "+str(int(level)+1)+"?",True,(0,0,0)),(start_x+self.min_window_size[0]//2-bigger_font.size("Upgrade to level "+str(int(level)+1)+"?")[0]//2,start_y+10))

        start_y += bigger_font.size("p")[1]*2

        # blits the building image+text
        text_pos = (start_x+10,start_y+bigger_font.size("U")[1])
        window.blit(font.render(name+" "+str(int(level)+1),True,(0,0,0)),text_pos)
        image_pos = (text_pos[0],text_pos[1]+font.size("p")[1]*1.5)
        window.blit(self.buildings_images[name][str(int(level)+1)], image_pos)
        if name in buildings.attacking_buildings_guns_by_building_name:
            gun_name = self.attacking_buildings_guns_by_building_name[name]
            angle = building["gun angle"]
            gun_image = pygame.transform.rotate(self.buildings_guns_images[gun_name][level],angle)
            angle_change_pos_needed = building["angle change pos needed"]
            gun_pos = (pos[0] - angle_change_pos_needed ,pos[1] - angle_change_pos_needed)
            window.blit(gun_image,gun_pos)
        
        # blits the time of the upgrade
        # draw the time above the building
        text = None
        time_left = buildings.upgrade_time[name][level]
        time_left2 = None
        time_type = "sec" # sec
        if time_left > 60: # sec => min
            time_left = time_left // 60
            time_type = "min"
        if time_left > 60: # min => hour
            time_left2 = time_left%60# minutes
            time_left = time_left // 60
            time_type = "h"
        if time_left2 == None:
            text = "time: "+str(time_left) + time_type
        else:
            text = "time: "+str(time_left) + time_type+" "+str(time_left2)+"min"
        pos = (image_pos[0],   image_pos[1]+self.buildings_images[name][str(int(level)+1)].get_height())
        window.blit(font.render(text,True,(0,0,0)), pos)

        text_x = start_x
        text_y = pos[1] + font.size("p")[1]*3
        window.blit(font.render("Changes:",True,(0,0,0)),(text_x,text_y))
        text_y += font.size("p")[1]*1.3

        # showing the building health change
        health_now = buildings.buildings_health[name][level]
        health_at_next_upgrade = buildings.buildings_health[name][str(int(level)+1)]
        health_change = health_at_next_upgrade-health_now
        window.blit(font.render("Health: "+str(health_now)+"+"+str(health_change),True,(0,0,0)),(text_x,text_y))
        text_y += font.size("p")[1]*1.2

        # collector
        if name in buildings.collectors_to_take_images:# shows the change of how much money it gives
            # shows the change of how much money it gives
            produce_per_sec = buildings.buildings[self.on_building]["money per sec"]
            max_production = buildings.buildings[self.on_building]["max money"]
            produce_per_sec_after_upgrade = buildings.produce_per_sec[name][str(int(level)+1)]
            max_production_after_upgrade = buildings.max_production[name][str(int(level)+1)]

            produce_per_sec_text_pos = (text_x,text_y)
            text_y += font.size("p")[1]*1.2
            max_production_text_pos = (text_x,text_y)

            window.blit(font.render("Produce per sec: "+str(produce_per_sec)+"+"+str(produce_per_sec_after_upgrade-produce_per_sec),True,(0,0,0)),produce_per_sec_text_pos)
            window.blit(font.render("Max production: "+str(max_production)+"+"+str(max_production_after_upgrade-max_production),True,(0,0,0)),max_production_text_pos)
        # storage
        elif "storage" in name:# shows the change of how much money it stores
            # shows the change of how much money it stores
            storage_stores_now = buildings.max_cash_in_storage_by_storage_level[name][level]
            storage_stores_after_upgrade = buildings.max_cash_in_storage_by_storage_level[name][str(int(level)+1)]

            window.blit(font.render("Storage capacity: "+str(storage_stores_now)+"+"+str(storage_stores_after_upgrade-storage_stores_now),True,(0,0,0)), (text_x,text_y))
            text_y += font.size("p")[1]*1.2
        # army camp
        elif name == "army camp": # shows the change of how much soldiers it "stores"
            # shows the change of how much soldiers it "stores"
            capacity_now = buildings.army_camp_capacity_by_level[level]
            capacity_change = buildings.army_camp_capacity_add_by_level[level]

            window.blit(font.render("Army capacity: "+str(capacity_now)+"+"+str(capacity_change),True,(0,0,0)), (text_x,text_y))
            text_y += font.size("p")[1]*1.2
        # barracks
        elif name == "barracks": # blits the next soldier he gets
            # blits the next soldier he gets
            soldier_name = list(army.soldiers_by_barracks_level)[int(level)]
            next_soldier_image = army.army_images[soldier_name]["1"]
            x = start_x +self.min_window_size[0] - next_soldier_image.get_width()*4 - bigger_font.size("p")[0]
            y = start_y + next_soldier_image.get_height()*2
            window.blit(medium_font.render("Next soldier:",True,(0,0,0)),(x,y))
            window.blit(font.render(soldier_name,True,(0,0,0)),(x+medium_font.size("Next soldier:")[0]//2-font.size(soldier_name)[0]//2,y+medium_font.size("N")[1]*1.2))
            window.blit(next_soldier_image, (x+medium_font.size("Next soldier:")[0]//2-next_soldier_image.get_width()//2,y+medium_font.size("N")[1]*1.2+font.size("N")[1]*1.4))
        
        # upgrade btn
        upgrade_cost = buildings.upgrade_cost[name][str(level)]
        cost_cash_type = buildings.building_cost_cash_type[name]
        shadow_color = user.cash_types_colors[cost_cash_type]
        cash_type_image = user.cash_types_images[cost_cash_type]
        

        mouse = pygame.mouse.get_pos()

        # upgrade btn
        if self.upgrade_btn_rect.collidepoint(mouse):
            window.blit(self.upgrade_btn_mouse_on,self.upgrade_btn_pos)
        else:
            window.blit(self.upgrade_btn,self.upgrade_btn_pos)
        window.blit(font.render(str(upgrade_cost), True, shadow_color),(self.upgrade_btn_pos[0]+self.upgrade_btn_size[0]//2-font.size(str(upgrade_cost))[0]//2-1,self.upgrade_btn_pos[1]+self.upgrade_btn_size[1]//6-1))
        window.blit(font.render(str(upgrade_cost), True, (255,255,255)),(self.upgrade_btn_pos[0]+self.upgrade_btn_size[0]//2-font.size(str(upgrade_cost))[0]//2,self.upgrade_btn_pos[1]+self.upgrade_btn_size[1]//6))
        window.blit(cash_type_image,(self.upgrade_btn_pos[0]+self.upgrade_btn_size[0]//2-cash_type_image.get_width()//2,self.upgrade_btn_pos[1]+font.size("p")[1]+self.upgrade_btn_size[1]//6))
    def handle_mouse(self):
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == True:
            mouse = pygame.mouse.get_pos()
            mouse_rect = (mouse[0],mouse[1],1,1)
            if self.esc_button_rect.colliderect(mouse_rect):
                self.in_building_upgrade_screen = False
            elif self.upgrade_btn_rect.colliderect(mouse_rect):
                id = self.on_building
                building = buildings.buildings[id]
                name = building["building name"]
                level = building["level"]
                upgrade_cost = buildings.upgrade_cost[name][str(level)]
                # getting the townhall level
                # getting the level you are checking on
                townhall = buildings.buildings["1"] # id=1 is the townhall(first building)
                checking_on_level = str(townhall["level"])
                if int(townhall["level"]) > int(buildings.max_buildings_levels[name]):
                    checking_on_level = str(buildings.max_buildings_levels[name])
                # doing the if statement
                if name == "townhall" or int(buildings.max_upgrade_of_each_building_by_townhall[name][checking_on_level]) > int(level) \
                    or int(list(buildings.max_of_each_building_by_townhall)[-1]) == int(townhall["level"]): # if its the final level of the townhall
                    if buildings.upgrade_building == None: # if no building is being upgrade
                        user_gold = user.gold
                        user_iron = user.iron
                        user_diamonds = user.diamonds
                        upgrade_cost_type = buildings.building_cost_cash_type[name]

                        can_upgrade = False
                        if upgrade_cost_type == "gold":
                            if user_gold >= upgrade_cost:
                                user.gold -= upgrade_cost
                                can_upgrade = True
                        elif upgrade_cost_type == "iron":
                            if user_iron >= upgrade_cost:
                                user.iron -= upgrade_cost
                                can_upgrade = True
                        elif upgrade_cost_type == "diamonds":
                            if user_diamonds >= upgrade_cost:
                                user.diamonds -= upgrade_cost
                                can_upgrade = True
                        if can_upgrade == True:
                            buildings.upgrade_building = {"id":id,"finish time":time.time()+buildings.upgrade_time[name][level]}
                            save_in_upgrade_buildings(buildings.upgrade_building)
                            user.save_cash_methods()
                            self.on_building = None
                            self.in_building_upgrade_screen = False
                        if can_upgrade == False:
                            fade_red_text.append_text("You don't have enough money to upgrade this building")
                    else:
                        fade_red_text.append_text("You can't upgrade more buildings right now")
                else:
                    fade_red_text.append_text("You must upgrade the townhall first")
upgrade_building_screen = create_upgrade_building_screen()

loading_screen(phase=2)

class create_army(): # basically a data class(saves,reload and keep the order of the soldiers in the game)
    """this class doesnt run any real meaningful functions(other classes use its self. variables and the save function)"""
    def __init__(self):
        tile_size = base_bg.tile_size
        army_soldiers_types = return_soldiers_names()
        levels_of_each_type = return_soldiers_levels()
        
        army_info = reload_army_and_capacity()
        self.soldiers_in_camp = army_info[1] # {id:info(name,level,capacity)}
        self.max_capacity = army_info[0][0]["max capacity"] # every soldier type takes some space, this is the max space
        self.capacity = army_info[0][0]["capacity"]
        self.soldier_in_upgrade = army_info[3] # {"name":name, "finish time":time}

        self.army_fixed_info = reload_army_fixed_info() # fixed=>קבוע
        self.soldiers_cost = self.army_fixed_info["soldiers cost"]
        self.soldier_upgrade_cost = self.army_fixed_info["soldiers upgrade cost"] # same cash type as soldiers_cost
        self.soldier_upgrade_duration = self.army_fixed_info["soldiers upgrade duration"]
        self.soldiers_cost_type = self.army_fixed_info["soldiers cost type"]
        # there is in the self.army_fixed info the weapons damage, but the dict is in the attack class
        self.soldiers_health = self.army_fixed_info["soldiers health"]

        self.soldiers_info_when_appending = {
            "killer drone":{"name":"killer drone","level":1,"capacity":5,"health":self.soldiers_health["killer drone"]["1"]},
            "rock machine":{"name":"rock machine","level":1,"capacity":7,"health":self.soldiers_health["rock machine"]["1"]},
            "bomb":{"name":"bomb","level":1,"capacity":4,"health":None},
            "missile":{"name":"missile","level":1,"capacity":6,"health":None}
        }

        self.soldiers_levels = army_info[2][0]
        
        for soldier_name in self.soldiers_levels:
            level = self.soldiers_levels[soldier_name]
            if level > self.soldiers_info_when_appending[soldier_name]["level"]:
                self.soldiers_info_when_appending[soldier_name]["level"] = level


        self.army_images_sizes = {
            "killer drone":(tile_size*3,tile_size*3),
            "rock machine":(int(tile_size*4*0.66666666666666666666666666666667),tile_size*4), # ratio: 612x918  0.66666666666666666666666666666667:1
            "bomb":(int(tile_size*3*0.71875),int(tile_size*3)), # 506x704  0.71875:1
            "missile":(int(tile_size*6*0.33),int(tile_size*6)), # 500:1700   0.33:1
        }
        self.army_soldiers_speed = {
            "killer drone":4,
            "rock machine":1.5,
            "bomb":7,
            "missile":7
        }
        self.army_soldiers_acceleration = { # only to some soldiers
            "bomb":0.07,
            "missile":0.07
        }
        self.army_soldiers_shoot_time_delay = {
            "killer drone":2,
            "rock machine":3,
            "bomb":None, # not shooting
            "missile":None, # not shooting
        }
        self.soldiers_by_barracks_level = { # soldier_name:from what barracks level
            "killer drone":1,
            "rock machine":2,
            "bomb":3,
            "missile":4,
        }

        self.army_images = {} # {"name":{"level":image,"level":image}}
        index = 0
        for soldier_type in army_soldiers_types:
            self.army_images[soldier_type] = {}
            for level in levels_of_each_type[index]:
                self.army_images[soldier_type][level] = pygame.transform.smoothscale(pygame.image.load(folder+"\\army\\"+soldier_type+"\\"+level+".png"), self.army_images_sizes[soldier_type])
            index += 1

    def set_army_ids(self): # does that the army ids will be from 1- and not from n-  (when not using all of the soldiers you trained it leaves the big id)
        # saves the string bits
        # use the sys.getsizeof(string) to get the size of a string in bytes
        soldiers_ids = list(self.soldiers_in_camp)
        new_ids = []
        for num in range(len(soldiers_ids)):
            new_ids.append(str(num+1))
        new_soldiers_dict = {}
        i = 0
        for soldier_id in new_ids:
            new_soldiers_dict[soldier_id] = self.soldiers_in_camp[soldiers_ids[i]]
            i += 1
        self.soldiers_in_camp = new_soldiers_dict
    def save_army(self):
        self.set_army_ids()
        # saves the army,capacity
        # (made a function for that because it was easier to handle the variables with self. , its looking better in the save_all() function)
        save_army_and_capacity(self.soldiers_in_camp,(self.capacity,self.max_capacity),[self.soldiers_levels],[self.soldier_in_upgrade])
army = create_army()

loading_screen(phase=3)

class create_user():
    def __init__(self):
        cash_methods = reload_cash_methods()
        self.gold = cash_methods["gold"]
        self.iron = cash_methods["iron"]
        self.diamonds = cash_methods["diamonds"]
        
        self.max_gold = cash_methods["max gold"]
        self.max_iron = cash_methods["max iron"]
        self.max_diamonds = cash_methods["max diamonds"]

        self.cash_types_colors = {
            "gold":(255,215,0),
            "iron":(128,132,135),
            "diamonds":(158,254,250)
        }
        self.cash_types_images = {
            "gold":pygame.transform.smoothscale(pygame.image.load(folder+"/gold coin.png"),(30,30)),
            "iron":pygame.transform.smoothscale(pygame.image.load(folder+"/iron.png"),(30,int(30*0.6875))), # 1:0.6875
            "diamonds":pygame.transform.smoothscale(pygame.image.load(folder+"/diamond.png"),(30,int(30*0.758))) # 500x379   1:0.758
        }

        self.gold_color = self.cash_types_colors["gold"] # gold color(kind of yellow)
        self.gold_coin = self.cash_types_images["gold"]
        self.gold_coin_pos = (10,40+base_bg.tile_size*3) # shown after the trophies

        self.iron_color = self.cash_types_colors["iron"]
        self.iron_img = self.cash_types_images["iron"] # 1:0.6875
        self.iron_pos = ((10,self.gold_coin_pos[1]+self.gold_coin.get_height()+10))

        self.diamond_color = self.cash_types_colors["diamonds"] # diamond color(kind of bright blue)
        self.diamond_img = self.cash_types_images["diamonds"] # 500x379   1:0.758
        self.diamond_pos =(10,self.gold_coin_pos[1]+self.gold_coin.get_height()+10+self.iron_img.get_height()+10)

        self.trophy = pygame.transform.smoothscale(pygame.image.load(folder+"/trophy.png"),(int(base_bg.tile_size*2*0.92),base_bg.tile_size*2)) # 500x543 0.92:1
        self.trophy_pos = (10,40)
        self.num_of_trophies = reload_user_trophies()
    def draw_payment_methods(self):
        if attack.attacking == False:
            window.blit(font.render(user_profile.profile_info["username"]+"'s base",True,(0,0,0)),(10,10))
        y = self.gold_coin_pos[1]+2
        window.blit(self.gold_coin, self.gold_coin_pos)
        pygame.draw.rect(window, self.gold_color, [self.gold_coin_pos[0]+self.gold_coin.get_width()+10,y, self.gold*(200/self.max_gold) ,22])
        pygame.draw.rect(window, (0,0,0), [self.gold_coin_pos[0]+self.gold_coin.get_width()+10,y,200,22],2)
        window.blit(font.render(str(self.gold),True,(0,0,0)), (self.gold_coin_pos[0]+self.gold_coin.get_width()+13,y+1))
        window.blit(font.render(str(self.gold),True,(0,0,0)), (self.gold_coin_pos[0]+self.gold_coin.get_width()+15,y+3))
        window.blit(font.render(str(self.gold),True,self.gold_color), (self.gold_coin_pos[0]+self.gold_coin.get_width()+14,y+2)) # 2 shadow for it to be all around the letter
        if self.gold == self.max_gold:
            draw_transparent_square(window,( self.gold*(200/self.max_gold) ,22),50,(255,0,0),(self.gold_coin_pos[0]+self.gold_coin.get_width()+10,y))
        
        window.blit(self.iron_img, self.iron_pos)
        pygame.draw.rect(window, self.iron_color, [self.iron_pos[0]+self.iron_img.get_width()+10,y+self.gold_coin.get_height()+5, self.iron*(200/self.max_iron) ,22])
        pygame.draw.rect(window, (0,0,0), [self.iron_pos[0]+self.iron_img.get_width()+10,y+self.gold_coin.get_height()+5,200,22],2)
        window.blit(font.render(str(self.iron),True,(0,0,0)), (self.iron_pos[0]+self.iron_img.get_width()+13,y+1+self.gold_coin.get_height()+5))
        window.blit(font.render(str(self.iron),True,(0,0,0)), (self.iron_pos[0]+self.iron_img.get_width()+15,y+3+self.gold_coin.get_height()+5))
        window.blit(font.render(str(self.iron),True,self.iron_color), (self.iron_pos[0]+self.iron_img.get_width()+14,y+2+self.gold_coin.get_height()+5)) # 2 shadow for it to be all around the letter
        if self.iron == self.max_iron:
            draw_transparent_square(window,( self.iron*(200/self.max_iron) ,22),50,(255,0,0),(self.iron_pos[0]+self.iron_img.get_width()+10,y+self.gold_coin.get_height()+5))
        
        window.blit(self.diamond_img, self.diamond_pos)
        pygame.draw.rect(window, self.diamond_color, [self.diamond_pos[0]+self.diamond_img.get_width()+10,y+self.gold_coin.get_height()+5+self.iron_img.get_height()+10, self.diamonds*(200/self.max_diamonds) ,22])
        pygame.draw.rect(window, (0,0,0), [self.diamond_pos[0]+self.diamond_img.get_width()+10,y+self.gold_coin.get_height()+5+self.iron_img.get_height()+10,200,22],2)
        window.blit(font.render(str(self.diamonds),True,(0,0,0)), (self.diamond_pos[0]+self.diamond_img.get_width()+13,y+1+self.gold_coin.get_height()+5+self.iron_img.get_height()+10))
        window.blit(font.render(str(self.diamonds),True,(0,0,0)), (self.diamond_pos[0]+self.diamond_img.get_width()+15,y+3+self.gold_coin.get_height()+5+self.iron_img.get_height()+10))
        window.blit(font.render(str(self.diamonds),True,self.diamond_color), (self.diamond_pos[0]+self.diamond_img.get_width()+14,y+2+self.gold_coin.get_height()+5+self.iron_img.get_height()+10)) # 2 shadow for it to be all around the letter
        if self.diamonds == self.max_diamonds:
            draw_transparent_square(window,( self.diamonds*(200/self.max_diamonds) ,22),100,(255,0,0),(self.diamond_pos[0]+self.diamond_img.get_width()+10,y+self.gold_coin.get_height()+5+self.iron_img.get_height()+10))
    def save_cash_methods(self):
        cash_methods = {
            "gold":self.gold,
            "max gold":self.max_gold,
            "iron":self.iron,
            "max iron":self.max_iron,
            "diamonds":self.diamonds,
            "max diamonds":self.max_diamonds
        }
        save_cash_methods(cash_methods)
    def draw_howmany_builders_left(self):
        builders_left = 0
        if buildings.upgrade_building == None: builders_left = 1
        max_builders = 1
        window.blit(
            bigger_font.render(f"Builders: {str(builders_left)}/{str(max_builders)}",True,(0,0,0)), (screen_x//2-bigger_font.size(f"Builders: {str(builders_left)}/{str(max_builders)}")[0]//2,10)
        )
    def draw_trophies_in_base(self):
        window.blit(self.trophy,self.trophy_pos)
        window.blit(bigger_font.render(str(self.num_of_trophies),True,(255,255,255)),(self.trophy_pos[0]+self.trophy.get_width()+5,self.trophy_pos[1]+self.trophy.get_height()//2-bigger_font.size("0")[1]//2))
user = create_user()


class create_barracks_screen():
    def __init__(self):
        self.in_barracks_screen = False

        self.esc_button_size = (bigger_font.size("X")[1]+2,bigger_font.size("X")[1]+2)
        self.esc_button_pos = (screen_x-self.esc_button_size[0]-10,10)

        self.soldier_card_size = (200,300)
        self.soldier_to_display_card_size = (200,200) # the size of the cards of the soldiers you trained
        self.minus_1_soldier_btn_size  = (30,30)
        self.minus_1_btn = pygame.transform.smoothscale(pygame.image.load(folder+"\\minus 1 btn.png"),self.minus_1_soldier_btn_size)

        self.soldiers = {} # {name:name, pos:(x,y)}
        self.soldiers_images = {} # {name:image}

        self.user_highest_barracks_level = None
        for build in buildings.buildings:
            building = buildings.buildings[build]
            if building["building name"] == "barracks":
                level = int(building["level"])
                if self.user_highest_barracks_level == None or level > self.user_highest_barracks_level:
                    self.user_highest_barracks_level = level
        self.soldiers_by_levels = army.soldiers_by_barracks_level
        
    def set_soldiers_dicts(self):
        x = 10
        y = screen_y//2-self.soldier_card_size[1]//2
        for name in army.soldiers_by_barracks_level:
            self.soldiers[name] = {}
            self.soldiers[name]["name"] = name
            self.soldiers[name]["pos"] = (x,y)
            self.soldiers_images[name] = pygame.transform.smoothscale(pygame.image.load(folder+"\\army\\"+name+"\\1.png"),(int(army.army_images[name]["1"].get_width()*1.5),int(army.army_images[name]["1"].get_height()*1.5)))

            x += self.soldier_card_size[0]+10
    
    def has_enough_money_to_train(self,name):
        cash_type = army.soldiers_cost_type[name]
        cost = army.soldiers_cost[name]
        can_buy = False
        if cash_type == "iron":
            if user.iron >= cost:
                can_buy = True
        
        return can_buy

    def draw_screen(self):
        pygame.draw.rect(window, (200,0,0),[self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1]])
        pygame.draw.rect(window, (255,64,64),[self.esc_button_pos[0]-2,self.esc_button_pos[1]-2,self.esc_button_size[0]+3,self.esc_button_size[1]+3],2)
        window.blit(bigger_font.render("X",True,(255,255,255)), (self.esc_button_pos[0]+self.esc_button_size[0]//2-bigger_font.size("X")[0]//2,self.esc_button_pos[1]+self.esc_button_size[1]//2-bigger_font.size("X")[1]//2))

        window.blit(bigger_font.render("capacity left: "+str(army.max_capacity-army.capacity),True,(0,0,0)), (screen_x//2-bigger_font.size("capacity left: "+str(army.max_capacity-army.capacity))[0]//2,100))

        # soldiers cards  (the upper cards)
        for name in self.soldiers:
            soldier = self.soldiers[name]
            image = self.soldiers_images[name]
            can_buy = self.has_enough_money_to_train(name)
            can_train_from_level = self.soldiers_by_levels[name]
            if can_train_from_level > self.user_highest_barracks_level:
                can_buy = False

            x,y = soldier["pos"]
            pygame.draw.rect(window, (54,100,139), [x,y,self.soldier_card_size[0],self.soldier_card_size[1]])
            pygame.draw.rect(window, (0,0,0), [x-1,y-1,self.soldier_card_size[0]+2,self.soldier_card_size[1]+2],1)
            window.blit(font.render(name,True,(0,0,0)),(x+self.soldier_card_size[0]//2-font.size(name)[0]//2,y+5))
            window.blit(image, 
                (x+self.soldier_card_size[0]//2-image.get_width()//2,y+5+font.size(name)[1]+5)
            )

            cost_type_image = user.cash_types_images[army.soldiers_cost_type[name]]
            window.blit(font.render(str(army.soldiers_cost[name]),True,(0,0,0)),(x+5,y+self.soldier_card_size[1]-font.size("p")[1]-5))
            window.blit(cost_type_image, (x+5+font.size(str(army.soldiers_cost[name]))[0]+5,y+self.soldier_card_size[1]-font.size("p")[1]-5))

            window.blit(font.render("capacity: "+str(army.soldiers_info_when_appending[name]["capacity"]),True,(0,0,0)),(x+5,y+self.soldier_card_size[1]-font.size("p")[1]*2-10))
            if army.max_capacity - army.capacity < army.soldiers_info_when_appending[name]["capacity"]:
                draw_transparent_square(window,(self.soldier_card_size[0],self.soldier_card_size[1]),100,(0,0,0),(x,y))
            if can_buy == False:
                draw_transparent_square(window,(self.soldier_card_size[0],self.soldier_card_size[1]),100,(0,0,0),(x,y))
            level = army.soldiers_levels[name]
            window.blit(font.render("Level: "+str(level),True,(0,0,0)),(x+self.soldier_card_size[0]//10,y+self.soldier_card_size[1]+10))
            
        
        # draws below the card how much there is of each soldier type(image and above it number)
        # create the dict
        how_much_of_each1 = list(army.soldiers_by_barracks_level) # {name:how_much...}
        how_much_of_each = {}
        for name in how_much_of_each1:
            how_much_of_each[name] = {}
        for soldier_id in army.soldiers_in_camp:
            soldier = army.soldiers_in_camp[soldier_id]
            name = soldier["name"]
            try:
                how_much_of_each[name] += 1
            except:
                how_much_of_each[name] = 1
        # draw the cards
        y = self.soldiers[list(self.soldiers)[0]]["pos"][1]+self.soldier_card_size[1]*1.5
        x = 10
        for soldier_type in how_much_of_each:
            if how_much_of_each[soldier_type] != {}:
                card_start_y = y-font.size("paragraph")[1]*1.5-10
                image = self.soldiers_images[soldier_type]
                how_much = how_much_of_each[soldier_type]
                pygame.draw.rect(window, (122,225,190), [x,y-font.size("paragraph")[1]*1.5-10,self.soldier_to_display_card_size[0],self.soldier_to_display_card_size[1]])
                pygame.draw.rect(window, (0,0,0), [x,y-font.size("paragraph")[1]*1.5-10,self.soldier_to_display_card_size[0],self.soldier_to_display_card_size[1]],1)
                window.blit(image, (x+self.soldier_to_display_card_size[0]//2-image.get_width()//2,y))
                window.blit(font.render(str(how_much)+" "+soldier_type,True,(0,0,0)),(x+self.soldier_to_display_card_size[0]//2-font.size(str(how_much)+soldier_type)[0]//2,y-font.size("paragraph")[1]*1.5))
                
                # minus 1 soldier btn
                minus_1_btn_pos = (x+self.minus_1_soldier_btn_size[1]*0.2,card_start_y+self.soldier_to_display_card_size[1]-self.minus_1_soldier_btn_size[1]*1.2)
                window.blit(self.minus_1_btn, minus_1_btn_pos)
                #pygame.draw.rect(window, (255,0,0),[minus_1_btn_pos[0],minus_1_btn_pos[1],self.minus_1_soldier_btn_size[0],self.minus_1_soldier_btn_size[1]])
                #window.blit(small_font.render("-1",True,(0,0,0)),(minus_1_btn_pos[0]+self.minus_1_soldier_btn_size[0]//2-small_font.size("-1")[0]//2,minus_1_btn_pos[1]+self.minus_1_soldier_btn_size[0]//2-small_font.size("-1")[1]//2))
                
                x += self.soldier_to_display_card_size[0]+10

    def handle_mouse(self):
        mouse = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == True: # press left btn
            # esc button
            if mouse[0] > self.esc_button_pos[0]-2 and mouse[0] < self.esc_button_pos[0] - 2 + self.esc_button_size[0]+3:
                if mouse[1] > self.esc_button_pos[1] - 2 and mouse[1] < self.esc_button_pos[1] - 2 + self.esc_button_size[1]+3:
                    self.army_camp_for_soldiers_info = [] # stores all of the army camps info(the building info)
                    self.army_camp_moving_soldiers = [] # [soldier dict,soldier dict]
                    self.in_barracks_screen = False
                    
                    buildings.army_camp_for_soldiers_info = [] # stores all of the army camps info(the building info)
                    buildings.army_camp_moving_soldiers = [] # [soldier dict,soldier dict]
            # train a soldier
            for name in self.soldiers:
                soldier = self.soldiers[name]
                x,y = soldier["pos"]
                if mouse[0] > x and mouse[0] < x+self.soldier_card_size[0]:
                    if mouse[1] > y and mouse[1] < y+self.soldier_card_size[1]:
                        cash_type = army.soldiers_cost_type[name]
                        can_buy = self.has_enough_money_to_train(name)
                        can_train_from_level = self.soldiers_by_levels[name]
                        if can_train_from_level > self.user_highest_barracks_level:
                            can_buy = False
                        if can_buy == True:
                            new_id = None
                            try:
                                last_id = list(army.soldiers_in_camp)[-1]
                                new_id = int(last_id)+1
                            except:
                                new_id = 1
                            capacity = army.soldiers_info_when_appending[name]["capacity"]
                            army.capacity += capacity
                            if army.capacity > army.max_capacity: # if their is no space in the camp for this soldier
                                army.capacity -= capacity
                            else:
                                # appends to the dict
                                army.soldiers_in_camp[str(new_id)] = army.soldiers_info_when_appending[name]
                                cash_type = army.soldiers_cost_type[name]
                                cost = army.soldiers_cost[name]
                                if cash_type == "iron":
                                    user.iron -= cost
                                army.save_army()
                                user.save_cash_methods()
                        else:
                            fade_red_text.append_text("Collect more money or upgrade the barracks to train this soldier")#You can't train this soldier right now
            
            # check if pressed to untrain a soldier
            how_much_of_each1 = list(army.soldiers_by_barracks_level) # {name:how_much...}
            how_much_of_each = {}
            for name in how_much_of_each1:
                how_much_of_each[name] = {}
            for soldier_id in army.soldiers_in_camp:
                soldier = army.soldiers_in_camp[soldier_id]
                name = soldier["name"]
                try:
                    how_much_of_each[name] += 1
                except:
                    how_much_of_each[name] = 1
            
            to_pop_names = []
            for name in how_much_of_each:
                if how_much_of_each[name] == {} or how_much_of_each[name] == 0:
                    to_pop_names.append(name)
            for name in to_pop_names:
                how_much_of_each.pop(name)

            y = self.soldiers[list(self.soldiers)[0]]["pos"][1]+self.soldier_card_size[1]*1.5
            x = 10
            for soldier_type in how_much_of_each:
                card_start_y = y-font.size("paragraph")[1]*1.5-10
                minus_1_btn_pos = (x+self.minus_1_soldier_btn_size[1]*0.2,card_start_y+self.soldier_to_display_card_size[1]-self.minus_1_soldier_btn_size[1]*1.2)
                btn_rect = pygame.Rect(minus_1_btn_pos[0],minus_1_btn_pos[1],self.minus_1_soldier_btn_size[0],self.minus_1_soldier_btn_size[1])
                mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)
                deleted = False # use to know if to stop the loop
                if btn_rect.colliderect(mouse_rect):
                    for soldier_id in army.soldiers_in_camp:
                        if army.soldiers_in_camp[soldier_id]["name"] == soldier_type:
                            cash_type = army.soldiers_cost_type[name]
                            cost = army.soldiers_cost[name]
                            if cash_type == "iron":
                                user.iron += cost
                                if user.iron > user.max_iron:
                                    user.iron = user.max_iron

                            army.capacity -= army.soldiers_in_camp[soldier_id]["capacity"]
                            army.soldiers_in_camp.pop(soldier_id)
                            army.save_army()
                            user.save_cash_methods()
                            deleted = True
                            break
                if deleted == True:
                    break
                x += self.soldier_to_display_card_size[0]+10
barracks_screen = create_barracks_screen()
barracks_screen.set_soldiers_dicts()

class create_the_lab_screen():
    # the user can upgrade the soldier to the barracks level
    def __init__(self):
        self.in_the_lab_screen = False

        self.lab_level = 0
        for building_id in buildings.buildings:
            building = buildings.buildings[building_id]
            if building["building name"] == "the lab":
                self.lab_level = int(building["level"])

        self.esc_button_size = (bigger_font.size("X")[1]+2,bigger_font.size("X")[1]+2)
        self.esc_button_pos = (screen_x-self.esc_button_size[0]-10,10)
        self.esc_button_rect = pygame.Rect(self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1])

        self.soldier_card_size = (200,300)

        self.soldiers = {}
    
    def set_soldiers_dict(self):
        x = 10
        y = screen_y//2-self.soldier_card_size[1]//2
        for name in army.soldiers_by_barracks_level:
            self.soldiers[name] = {}
            self.soldiers[name]["name"] = name
            self.soldiers[name]["pos"] = (x,y)
            self.soldiers[name]["level"] = army.soldiers_levels[name]

            x += self.soldier_card_size[0]+10
    def draw_screen(self):
        pygame.draw.rect(window, (200,0,0),[self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1]])
        pygame.draw.rect(window, (255,64,64),[self.esc_button_pos[0]-2,self.esc_button_pos[1]-2,self.esc_button_size[0]+3,self.esc_button_size[1]+3],2)
        window.blit(bigger_font.render("X",True,(255,255,255)), (self.esc_button_pos[0]+self.esc_button_size[0]//2-bigger_font.size("X")[0]//2,self.esc_button_pos[1]+self.esc_button_size[1]//2-bigger_font.size("X")[1]//2))
        
        text_color = (152,245,255)

        if self.soldiers == {}:
            self.set_soldiers_dict()
        # the soldiers cards
        for soldier_name in self.soldiers:
            soldier = self.soldiers[soldier_name]
            name = soldier_name
            image = barracks_screen.soldiers_images[name]

            x,y = soldier["pos"]
            level = soldier["level"]
            pygame.draw.rect(window, (54,100,139), [x,y,self.soldier_card_size[0],self.soldier_card_size[1]])
            pygame.draw.rect(window, (0,0,0), [x-1,y-1,self.soldier_card_size[0]+2,self.soldier_card_size[1]+2],1)
            window.blit(font.render(name,True,(0,0,0)),(x+self.soldier_card_size[0]//2-font.size(name)[0]//2,y+5))
            window.blit(image, 
                (x+self.soldier_card_size[0]//2-image.get_width()//2,y+5+font.size(name)[1]+5)
            )

            if army.soldier_in_upgrade != None and name == army.soldier_in_upgrade["name"]: # if there is a soldier that is being upgraded
                finish_time = army.soldier_in_upgrade["finish time"]
                time_left = finish_time - time.time()
                time_text = ""
                hours = int(time_left//60//60)
                minutes = int(time_left//60 % 60)
                seconds = int(time_left % 60)
                
                if hours != 0:
                    time_text = str(hours)+":"+str(minutes)+":"+str(seconds)
                else:
                    if minutes < 10:
                        minutes = "0"+str(minutes)
                    if seconds < 10:
                        seconds = "0"+str(seconds)
                    if minutes != 0 and minutes != "00":
                        time_text = str(minutes)+":"+str(seconds)
                    else:
                        time_text = str(seconds)+"sec"
                window.blit(medium_font.render(time_text,True,(0,0,0)),(x+self.soldier_card_size[0]//2-medium_font.size(time_text)[0]//2,y-medium_font.size("S")[1]))

                draw_transparent_square(window,(self.soldier_card_size[0],self.soldier_card_size[1]),100,(0,0,0),(x,y))
                window.blit(bigger_font.render("In Upgrade",True,text_color),(x+self.soldier_card_size[0]//2-bigger_font.size("In Upgrade")[0]//2, y+self.soldier_card_size[1]//2-bigger_font.size("L")[1]//2))


            level_text = "Lvl. "+str(level)
            Lvl_pos = (x+self.soldier_card_size[0]//2-medium_font.size(level_text)[0]//2, y+self.soldier_card_size[1]-medium_font.size("L")[1]*1.2)
            window.blit(medium_font.render(level_text,True,(255,255,255)),Lvl_pos)
            
            try:
                cost_type = army.soldiers_cost_type[name]
                cost = army.soldier_upgrade_cost[name][str(level)]
                cost_text = str(cost)
                cost_pos = (x+self.soldier_card_size[0]//2-medium_font.size(cost_text)[0]//2, Lvl_pos[1]- medium_font.size("L")[1]*1.2)
                cost_type_image = user.cash_types_images[cost_type]
                cost_color = ()
                if cost_type == "gold":
                    cost_color = user.gold_color
                elif cost_type == "iron":
                    cost_color = user.iron_color
                elif cost_type == "diamonds":
                    cost_color = user.diamond_color
                cost_pos = (cost_pos[0] - cost_type_image.get_width()//2,cost_pos[1])

                window.blit(medium_font.render(cost_text,True,(0,0,0)),(cost_pos[0]-1,cost_pos[1]-1)) # shadow (for it to look better)
                window.blit(medium_font.render(cost_text,True,cost_color),cost_pos)
                window.blit(cost_type_image, (cost_pos[0]+medium_font.size(cost_text)[0]+5,cost_pos[1]))
            except KeyError: # in case it doesnt have any upgrades(should happen only in case of a bug)
                #print("This soldier doesnt have upgrades")
                pass
            except Exception as e:
                print("the lab screen error:\n",e)


            can_upgrade = True
            if level > self.lab_level or int(list(army.army_images[name])[-1]) == level:
                draw_transparent_square(window,(self.soldier_card_size[0],self.soldier_card_size[1]),100,(0,0,0),(x,y))

                if int(list(army.army_images[name])[-1]) == level:
                    window.blit(bigger_font.render("Max Lvl",True,text_color),(x+self.soldier_card_size[0]//2-bigger_font.size("Max Lvl")[0]//2, y+self.soldier_card_size[1]//2-bigger_font.size("L")[1]//2))
                    can_upgrade = False
                else:
                    window.blit(font.render("Upgrade the lab",True,text_color),(x+self.soldier_card_size[0]//2-font.size("Upgrade the lab")[0]//2, y+self.soldier_card_size[1]//2-font.size("L")[1]//2))
                    window.blit(font.render("first",True,text_color),(x+self.soldier_card_size[0]//2-font.size("first")[0]//2, y+self.soldier_card_size[1]//2-font.size("L")[1]//2+font.size("L")[1]*1.2))
            
            soldier_damage = None
            soldier_weapon = None
            try:
                soldier_damage = attack.weapons_damage[name][str(level)]
                soldier_damage = attack.weapons_damage[name][str(level)]
                soldier_weapon = name # because its the throwable, it has no weapon
            except KeyError: # not the throwable
                soldier_weapon = attack.weapons_by_soldiers[name]
                soldier_damage = attack.weapons_damage[soldier_weapon][str(level)]
            soldier_health = str(army.soldiers_health[name][str(level)])
            if soldier_health == None or soldier_health == "None":
                soldier_health = ""
            if can_upgrade == True:
                # the changes text
                start_x = x + 5
                start_y = y + self.soldier_card_size[1]+font.size("p")[1]*0.5
                window.blit(font.render("Changes:",True,(0,0,0)),(start_x,start_y))
                start_y += font.size("p")[1]*1.3
                if soldier_health != "":
                    health_next_level = army.soldiers_health[name][str(level+1)]
                    window.blit(font.render("Health:"+soldier_health+"+"+str(health_next_level - int(soldier_health)),True,(0,0,0)),(start_x,start_y))
                else:
                    window.blit(font.render("Health:"+soldier_health,True,(0,0,0)),(start_x,start_y))
                start_y += font.size("p")[1]*1.2

                damage_in_next_level = attack.weapons_damage[soldier_weapon][str(level+1)]
                window.blit(font.render("Damage: "+str(soldier_damage)+"+"+str(damage_in_next_level-soldier_damage),True,(0,0,0)),(start_x,start_y))

                start_y += font.size("p")[1]*1.2
                upgrade_duration = army.army_fixed_info["soldiers upgrade duration in minutes"][name][str(level)]
                window.blit(font.render("Upgrade time: "+upgrade_duration,True,(0,0,0)),(start_x,start_y))
            else:
                start_x = x + 5
                start_y = y + self.soldier_card_size[1]+font.size("p")[1]*0.5
                window.blit(font.render("Stats:",True,(0,0,0)),(start_x,start_y))
                start_y += font.size("p")[1]*1.3
                window.blit(font.render("Health:"+soldier_health,True,(0,0,0)),(start_x,start_y))
                start_y += font.size("p")[1]*1.2

                window.blit(font.render("Damage: "+str(soldier_damage),True,(0,0,0)),(start_x,start_y))
                

    def handle_mouse(self):
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] == True:
            mouse = pygame.mouse.get_pos()
            if self.esc_button_rect.collidepoint(mouse):
                self.in_the_lab_screen = False
            
            for soldier_name in self.soldiers:
                soldier = self.soldiers[soldier_name]
                name = soldier["name"]
                level = soldier["level"]
                x,y = soldier["pos"]

                soldier_rect = pygame.Rect(x,y,self.soldier_card_size[0],self.soldier_card_size[1])
                if soldier_rect.collidepoint(mouse):
                    if level > self.lab_level: # if the user is at the same lab level
                        fade_red_text.append_text("You must upgrade the lab first")
                    elif  int(list(army.army_images[name])[-1]) == level: # if the soldier is at its final/max level
                        pass
                    elif army.soldier_in_upgrade != None:
                        if army.soldier_in_upgrade["name"] == name:
                            fade_red_text.append_text("You are upgrading this soldier right now")
                        else:
                            fade_red_text.append_text("You can't upgrade two soldiers at the same time")
                    else:
                        cost_type = army.soldiers_cost_type[name]
                        cost = army.soldier_upgrade_cost[name][str(level)]
                        upgraded = False
                        if cost_type == "iron":
                            if user.iron - cost >= 0:
                                user.iron -= cost
                                upgraded = True
                            else:
                                fade_red_text.append_text("You dont have enough "+cost_type+" to upgrade the "+name)

                        if upgraded == True:
                            army.soldier_in_upgrade = {
                                "name":name,
                                "finish time": time.time() + army.soldier_upgrade_duration[name][str(level)]
                            }
                            """army.soldiers_info_when_appending[name]["level"] += 1
                            army.soldiers_levels[name] += 1
                            for soldier_id in army.soldiers_in_camp:
                                soldier = army.soldiers_in_camp[soldier_id]
                                if soldier["name"] == name:
                                    soldier["level"] += 1"""
                            self.set_soldiers_dict()
                            user.save_cash_methods()
                            army.save_army()
    def handle_in_upgrade_soldier(self):
        if army.soldier_in_upgrade != None:
            finish_time = army.soldier_in_upgrade["finish time"]
            if finish_time <= time.time():
                name = army.soldier_in_upgrade["name"]
                army.soldiers_info_when_appending[name]["level"] += 1
                army.soldiers_levels[name] += 1
                for soldier_id in army.soldiers_in_camp:
                    soldier = army.soldiers_in_camp[soldier_id]
                    if soldier["name"] == name:
                        soldier["health"] = army.soldiers_health[name][str(soldier["level"]+1)]
                        soldier["level"] += 1
                army.soldier_in_upgrade = None
                army.save_army()
                self.set_soldiers_dict()
    def handle_keyboard(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.in_the_lab_screen = False
the_lab_screen = create_the_lab_screen()

loading_screen(phase=3)

class create_shop():
    def __init__(self):
        self.in_shop = False

        self.button_size = (60,60) # 616x265  1:1
        self.button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/shop button.png"),self.button_size)
        self.button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/shop button mouse on.png"),self.button_size)
        self.button_pos = (10,screen_y-self.button_size[1]-10)
        self.button_rect = pygame.Rect(self.button_pos[0],self.button_pos[1],self.button_size[0],self.button_size[1])

        self.esc_button_size = (bigger_font.size("X")[1]+2,bigger_font.size("X")[1]+2)
        self.esc_button_pos = (screen_x-self.esc_button_size[0]-10,10)

        self.buildings_names = buildings.buildings_names
        self.buildings_names.remove("townhall")
        self.buildings_to_buy = {} # positions of the buildings: {building name:{has:0,max:2, pos:(x,y)}}
        
        self.buildings_images = {} # ONLY level 1
        self.buildings_guns_images = {} # only level 1
        self.building_card_size = (200,250) # width set in the next for loop (by the building that has the most width)
        for name in list(buildings.buildings_sizes)[1:]:
            size = buildings.buildings_sizes[name]
            image = buildings.buildings_images[name]["1"]
            if self.building_card_size[0] == None or self.building_card_size[0] < size[0]:
                self.building_card_size = (size[0],self.building_card_size[1])
            if size[0] > self.building_card_size[0]:
                self.building_card_size = (size[0],self.building_card_size[1])
            self.buildings_images[name] = image
        for building_gun_name in buildings.buildings_guns_names:
            building_name = buildings.attacking_buildings_guns_by_gun_name[building_gun_name]
            image = buildings.buildings_guns_images[building_gun_name]["1"]
            self.buildings_guns_images[building_gun_name] = image
        self.in_shop_moving_speed_original = 5
        self.in_shop_moving_speed = 5 # this will change if the user is moving with the cursor

    def set_buildings_to_buy_dict(self):
        index = 0
        for name in self.buildings_names:
            self.buildings_to_buy[name] = {}
            self.buildings_to_buy[name]["has"] = 0 # change in the for loop
            # by the townhall level, id=1 1 is the townhall always
            self.buildings_to_buy[name]["max"] = buildings.max_of_each_building_by_townhall[buildings.buildings["1"]["level"]][name]
            x = 10 + index * self.building_card_size[0]
            y = screen_y//2 - self.building_card_size[1]//2
            self.buildings_to_buy[name]["pos"] = (x,y)
            for id in buildings.buildings:
                if buildings.buildings[id]["building name"] == name:
                    self.buildings_to_buy[name]["has"] = self.buildings_to_buy[name]["has"] + 1
            index += 1.1 # for that there will be a little space between every card

    def draw_button(self):
        mouse = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse):
            window.blit(self.button_mouse_on,self.button_pos)
        else:
            window.blit(self.button,self.button_pos)
        # counts how many things the user has to buy
        num_of_things_has_to_buy = 0
        for building in self.buildings_to_buy:
            building = self.buildings_to_buy[building]
            has,max = building["has"],building["max"]

            if has != max:
                num_of_things_has_to_buy += 1
        if num_of_things_has_to_buy != 0: # if he has things to buy
            # show the number of the things he has to buy in the bottom right of the btn
            window.blit(small_font.render(str(num_of_things_has_to_buy),True,(255,255,255)),(self.button_pos[0]+self.button_size[0]-font.size("8")[0]*1.2,self.button_pos[1]+self.button_size[1]-font.size("8")[1]))
    def press_button_check(self):
        mouse = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        if mouse_press[0] == True:
            if self.button_rect.collidepoint(mouse):
                self.in_shop = True
                self.set_buildings_to_buy_dict()
    def press_esc_button_check(self):
        mouse = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        if mouse_press[0] == True:
            if mouse[0] > self.esc_button_pos[0]-2 and mouse[0] < self.esc_button_pos[0] - 2 + self.esc_button_size[0]+3:
                if mouse[1] > self.esc_button_pos[1] - 2 and mouse[1] < self.esc_button_pos[1] - 2 + self.esc_button_size[1]+3:
                    self.army_camp_for_soldiers_info = [] # stores all of the army camps info(the building info)
                    self.army_camp_moving_soldiers = [] # [soldier dict,soldier dict]
                    self.in_shop = False
    
    def draw_shop(self):
        # esc button (right up)
        pygame.draw.rect(window, (200,0,0),[self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1]])
        pygame.draw.rect(window, (255,64,64),[self.esc_button_pos[0]-2,self.esc_button_pos[1]-2,self.esc_button_size[0]+3,self.esc_button_size[1]+3],2)
        window.blit(bigger_font.render("X",True,(255,255,255)), (self.esc_button_pos[0]+self.esc_button_size[0]//2-bigger_font.size("X")[0]//2,self.esc_button_pos[1]+self.esc_button_size[1]//2-bigger_font.size("X")[1]//2))

        # the actual things you can buy
        for building in self.buildings_to_buy:
            name = building
            building = self.buildings_to_buy[name]
            x,y = building["pos"]
            finish_x,finish_y = x+self.building_card_size[0], y+self.building_card_size[1]
            has,max = building["has"],building["max"]
            pygame.draw.rect(window, (54,100,139), [x,y,self.building_card_size[0],self.building_card_size[1]])
            pygame.draw.rect(window, (0,0,0), [x-1,y-1,self.building_card_size[0]+2,self.building_card_size[1]+2],1)
            window.blit(bigger_font.render(name, True, (255,255,255)), (x+self.building_card_size[0]//2-bigger_font.size(name)[0]//2,y+2))
            window.blit(self.buildings_images[name], (x + self.building_card_size[0]//2 - self.buildings_images[name].get_width()//2,y+bigger_font.size(name)[1]*1.5))
            if name in buildings.attacking_buildings_guns_by_building_name:
                gun_name = buildings.attacking_buildings_guns_by_building_name[name]
                gun_image = self.buildings_guns_images[gun_name]
                window.blit(gun_image, (x + self.building_card_size[0]//2 - gun_image.get_width()//2,y+bigger_font.size(name)[1]*1.5))
            window.blit(font.render("max: "+str(max)+",  has: "+str(has),True,(0,0,0)),(x+5,finish_y-font.size("max:")[1]*3))

            cost_type = buildings.building_cost_cash_type[name]
            cost_type_image = user.cash_types_images[cost_type]
            cost_color = user.cash_types_colors[cost_type]

            cost_pos = (x+5,finish_y-font.size("max:")[1]*1.5)
            
            cost_text = "cost: "+str(buildings.building_cost[name])
            window.blit(font.render(cost_text,True,(0,0,0)),(cost_pos[0]-1,cost_pos[1]-1)) # shadow
            window.blit(font.render(cost_text,True,cost_color),cost_pos)
            window.blit(cost_type_image, (cost_pos[0] + font.size(cost_text)[0]+5,cost_pos[1]))

            if has == max:
                draw_transparent_square(window,(self.building_card_size[0],self.building_card_size[1]),150,(0,0,0),(x,y))
                can_get_from_townhall = None
                for townhall_level in buildings.max_of_each_building_by_townhall:
                    levels_info = buildings.max_of_each_building_by_townhall[townhall_level]
                    building_level_info = levels_info[name]
                    if max != building_level_info and building_level_info > max:
                        can_get_from_townhall = townhall_level
                        break
                text = "Lvl. "+str(can_get_from_townhall)
                if can_get_from_townhall == None:
                    text = "Max"
                window.blit(bigger_font.render(text,True,(152,245,255) ),(x+self.building_card_size[0]//2-bigger_font.size(text)[0]//2,y+self.building_card_size[1]//2-bigger_font.size("L")[1]//2))
            if len(buildings.buildings) == 1:
                if name == "gold mine" or name == "iron mine":
                    pygame.draw.rect(window,(255,255,0),[x,y,self.building_card_size[0],self.building_card_size[1]],2)
    def handle_mouse_in_shop(self): # check if the user pressed to buy anything, if yes handle by this
        pressed_mouse = pygame.mouse.get_pressed()
        if pressed_mouse[0] == True: # if pressed the mouse, start checking things
            mouse = pygame.mouse.get_pos()
            for building in self.buildings_to_buy:
                name = building
                building = self.buildings_to_buy[name]
                x,y = building["pos"]
                finish_x,finish_y = x+self.building_card_size[0], y+self.building_card_size[1]
                has,max = building["has"],building["max"]
                if mouse[0] > x and mouse[0] < finish_x:
                    if mouse[1] > y and mouse[1] < finish_y:
                        if has < max: # check if can put another one and if has enough money
                            # will do the buy thing
                            """does:
                            1. putting the building in the dict buildings.buildings
                            2. putting the building in the center position(need to be by the tiles)
                            3. putting the building in the buildings.moving_building variable(maybe the building is in a place it can't be
                            4. changing the variable self.in_shop to be False and let the user resume the game"""
                            user_gold = user.gold
                            user_iron = user.iron
                            user_diamonds = user.diamonds
                            payment_type = buildings.building_cost_cash_type[name]
                            cost = buildings.building_cost[name]
                            id = int(list(buildings.buildings)[-1])+1
                            
                            place = False
                            if payment_type == "gold":
                                if user_gold >= cost:
                                    place = True
                            elif payment_type == "iron":
                                if user_iron >= cost:
                                    place = True
                            elif payment_type == "diamonds":
                                if user_diamonds >= cost:
                                    place = True
    
                            if list(buildings.buildings)[-1] == "1":
                                if not name == "gold mine" and not name == "iron mine":
                                    place = False
                                    fade_red_text.append_text("You must buy gold,iron collectors first")
                            elif list(buildings.buildings)[-1] == "2":
                                if "gold" in buildings.buildings["2"] and "iron" in name:
                                    place = True
                                elif "iron" in buildings.buildings["2"] and "gold" in name:
                                    place = True
                        
                            if place == True:
                                buildings.buildings[str(id)] = {"building name":name,"pos":(base_bg.tiles[0][0]-base_bg.tile_size*2,base_bg.tiles[0][1]-base_bg.tile_size*2),"level":"1"}
                                if name in buildings.collectors_to_take_images:
                                    buildings.buildings[str(id)]["money per sec"] = buildings.produce_per_sec[name]["1"]
                                    buildings.buildings[str(id)]["money produced"] = 0
                                    buildings.buildings[str(id)]["max money"] = buildings.max_production[name]["1"]
                                    buildings.buildings[str(id)]["time to produce"] = time.time()+1
                                if name == "gold storage" or name == "iron storage" or name == "diamonds storage":
                                    max_storage = buildings.max_cash_in_storage_by_storage_level[name]["1"]
                                    if "gold" in name:
                                        user.max_gold += max_storage
                                    elif "iron" in name:
                                        user.max_iron += max_storage
                                    elif "diamonds" in name:
                                        user.max_diamonds += max_storage
                                if name in buildings.attacking_buildings_guns_by_building_name:
                                    angle = random.randint(1,360)
                                    buildings.buildings[str(id)]["gun angle"] = angle
                                    angle_change_pos_needed = 0
                                    if angle == 0 or angle == 90 or angle == 180 or angle == 270 or angle == 360:
                                        pass
                                    if angle <= 100:
                                        angle_change_pos_needed = 7
                                    elif angle > 100 and angle <= 150:
                                        angle_change_pos_needed = 20
                                    elif angle > 150 and angle <= 250:
                                        angle_change_pos_needed = 10
                                    elif angle > 250 and angle < 350:
                                        angle_change_pos_needed = 15
                                    buildings.buildings[str(id)]["angle change pos needed"] =  angle_change_pos_needed
                                if name == "army camp":
                                    army.max_capacity += buildings.army_camp_capacity_change_by
                                    army.save_army()
                                buildings.moving_buildings = {str(id):buildings.buildings[str(id)]}
                                self.set_buildings_to_buy_dict()

                                if payment_type == "gold" and user_gold >= buildings.building_cost[name]:
                                    user.gold -= buildings.building_cost[name]
                                elif payment_type == "iron" and user_iron >= buildings.building_cost[name]:
                                    user.iron -= buildings.building_cost[name]
                                elif payment_type == "diamonds" and user_diamonds >= buildings.building_cost[name]:
                                    user.diamonds -= buildings.building_cost[name]
                                if name == "barracks":
                                    # set the barracks level(used to check in what soldier the user can use)
                                    if barracks_screen.user_highest_barracks_level == None:
                                        barracks_screen.user_highest_barracks_level = 1
                                if name == "the lab":
                                    the_lab_screen.lab_level = 1
                                user.save_cash_methods()
                                self.in_shop = False
                            else:
                                if list(buildings.buildings)[-1] != "1":
                                    fade_red_text.append_text("You don't have enough money to buy this building")
    def move(self,direction): # moves all of the buildings images
        on_dict = self.buildings_to_buy.copy()
        if direction == "left":
            to = self.in_shop_moving_speed
        elif direction == "right": # right
            to = -self.in_shop_moving_speed
        for build in on_dict:
            on_dict[build]["pos"] = (on_dict[build]["pos"][0]+to,on_dict[build]["pos"][1])
        
        first_pos = on_dict[list(on_dict)[0]]["pos"]
        last_pos = on_dict[list(on_dict)[-1]]["pos"]
        """
        direction = left to = 5
        direction = right to = -5"""
        if direction == "left" and first_pos[0] < 20:
            pass
        elif direction == "right" and last_pos[0] + self.building_card_size[0] > screen_x-20:
            pass
        else:
            for build in on_dict:
                on_dict[build]["pos"] = (on_dict[build]["pos"][0]-to,on_dict[build]["pos"][1])
            self.buildings_to_buy = on_dict
    def handle_keyboard_in_shop(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: # move right
            self.move("right")
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]: # move left
            self.move("left") 
shop = create_shop()
shop.set_buildings_to_buy_dict()

loading_screen(phase=1)

class create_user_profile():
    def __init__(self):
        self.made_profile,self.profile_info = reload_profile()
        # self.made_profile - True/False
    def save_profile(self):
        save_profile(self.made_profile,self.profile_info)
user_profile = create_user_profile()

if user_profile.made_profile == False: # if didnt create a profile yet it wil now(happens only when playing for the first time)
    set_profile()
    user_profile.made_profile,user_profile.profile_info = reload_profile()
    if user_profile.profile_info == {}:
        user_profile.made_profile = False
        user_profile.save_profile()
        exit()

loading_screen(phase=1)


class create_movement():
    def __init__(self):
        self.arrows = pygame.transform.scale(pygame.image.load(folder + "/movement arrows.png"), (int(screen_y/10.1),int(screen_y/10.1)))
        self.arrows_pos = (screen_x-self.arrows.get_width()-5,screen_y-self.arrows.get_height()-5)
        self.arrows_rect = pygame.Rect(self.arrows_pos[0],self.arrows_pos[1],self.arrows.get_width(),self.arrows.get_height())
        self.move_speed = 10 # speed in px
    def draw_arrows(self):
        window.blit(self.arrows, self.arrows_pos)
    def handle_mouse(self,mouse): # gets mouse pos, checks if on the arrows and move by this
        mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)
        if mouse_rect.colliderect(self.arrows_rect):
            if mouse[0] < self.arrows_pos[0]+self.arrows.get_width()/2: # left
                print("move left")
                self.move("left")
            if mouse[0] > self.arrows_pos[0]+self.arrows.get_width()/2: # right
                print("move right")
                self.move("right")
            if mouse[1] < self.arrows_pos[1]+self.arrows.get_height()/2: # up
                print("move up")
                self.move("up")
            if mouse[1] > self.arrows_pos[1]+self.arrows.get_height()/2: # down
                print("move down")
                self.move("down")
    def handle_keyboard_arrows(self,keys): # same as handle_mouse() but with the keyboard arrows 
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            print("move left")
            self.move("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            print("move right")
            self.move("right")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            print("move up")
            self.move("up")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            print("move down")
            self.move("down")
    
    def move_buildings(self,x_change,y_change): # used in the function move()
        index = 0
        for building in buildings.buildings:
            id = building
            building = buildings.buildings[id]
            name = building["building name"]
            pos = building["pos"]
            pos = (pos[0] + x_change,pos[1] + y_change)
            level = building["level"]
            buildings.buildings[id]["pos"] = pos
            index += 1
        base_bg.start_pos = (base_bg.start_pos[0]+x_change,  base_bg.start_pos[1]+y_change)
    def move(self,to): # moves the tiles+everything else to where it needs to move(move if possible)
        # to = "up"/"down"/"left"/"right"
        tiles_copy = base_bg.tiles.copy()
        if to == "left": # left
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                x += self.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
        elif to == "right": # right
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                x -= self.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
        elif to == "up": # up
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                y += self.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
        else: # down
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                y -= self.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
        rightest = base_bg.tiles[1]
        leftest = base_bg.tiles[1] # this one wont change in the loop(first one always leftest+toppest)
        toppest = base_bg.tiles[1] # this one wont change in the loop(first one always leftest+toppest)
        lowest = base_bg.tiles[-1]

        for tile in base_bg.tiles:
            x,y,color,image = tile
            if x > rightest[0]:
                rightest = tile
            if y > lowest[1]:
                lowest = tile
        update_pos = True
        base_bg.draw_sea = False
        # the sea is 3 tiles long
        sea_size = base_bg.tile_size*3
        if leftest[0] - sea_size + base_bg.tile_size > 0 and to == "left":
            update_pos = False
        elif rightest[0] + sea_size < screen_x and to == "right":
            update_pos = False
        if toppest[1] - sea_size + base_bg.tile_size > 0 and to == "up":
            update_pos = False
        elif lowest[1] + sea_size < screen_y and to == "down":
            update_pos = False
    
        if leftest[0] + base_bg.tile_size >= 0:
            base_bg.draw_sea = True
        if rightest[0] <= screen_x:
            base_bg.draw_sea = True
        if toppest[1] + base_bg.tile_size >= 0:
            base_bg.draw_sea = True
        if lowest[1] <= screen_y:
            base_bg.draw_sea = True

        if update_pos == False: # in case the ifs above do not work well
            base_bg.draw_sea = True
        if update_pos == True:
            base_bg.tiles = tiles_copy

            # only when its sure the moving is ok the buildings move too
            """ifs build like this:
            condition:
                move buildings(the ones that are in their place)
                end condition"""
            x_change = 0
            y_change = 0
            if to == "left": # left
                self.move_buildings(self.move_speed,0)
                x_change = self.move_speed
            elif to == "right": # right
                self.move_buildings(-self.move_speed,0)
                x_change = -self.move_speed
            elif to == "up": # up
                self.move_buildings(0,self.move_speed)
                y_change = self.move_speed
            else: # down
                self.move_buildings(0,-self.move_speed)
                y_change = -self.move_speed
            index = 0
            for soldier in buildings.army_camp_moving_soldiers:
                x,y = soldier["pos"]
                x += x_change
                y += y_change
                soldier["pos"] = (x,y)
                buildings.army_camp_moving_soldiers[index] = soldier
                index += 1
movement = create_movement()

loading_screen(phase=2)

class create_fade_red_text():
    """this is the red fade text that showed when the user can't buy/do something"""
    def __init__(self):
        self.text = [] # [text,fade_level(alpha level), position(x,y)]
    def append_text(self,text):
        if self.text == []:
            to_append = [
                text,
                255, # the max alpha level
               (screen_x//2-font.size(text)[0]//2, screen_y//3)
            ]
            self.text.append(to_append)
        elif self.text != []:
            if self.text[-1][0] != text or not self.text[-1][1] > 200: # if its not the same text as the last one or if its the same one but the last one is fading
                # move everything 1 line up
                index = 0
                for text2 in self.text:
                    x,y = text2[2]
                    y -= font.size("p")[1]*1.5
                    self.text[index][2] = (x,y)
                    index += 1
                
                to_append = [
                    text,
                    255, # the max alpha level
                (screen_x//2-font.size(text)[0]//2,self.text[-1][2][1]+font.size("p")[1]*1.5)
                ]
                self.text.append(to_append)
    def show_text(self):
        for text in self.text:
            x,y = text[2]
            alpha_level = int(text[1])
            text = text[0]
            blit_fade_text(window,text,font,alpha_level,(x,y),(255,0,0))
            self.fade_text()
    def fade_text(self):
        index = 0
        for text in self.text:
            alpha_level = text[1]
            if alpha_level > 150:
                alpha_level -= 1
            else:
                alpha_level -= 2
            if alpha_level < 0:
                self.text.remove(self.text[index])
            else:
                self.text[index][1] = alpha_level
            index +=1 
fade_red_text = create_fade_red_text()

class create_collect_money_effect():
    """how it will look options:
    the specific money type coming out of the collector
    the specific money type coming out of the collector to the cash bar
    the money will go to the storages
    there will be a faded text of '+how much he earned'(example- +100) right to the cash type bar
    there will be faded text above each collector that says how much he took from this specific collector

    ***the chosen one: faded text in the middle of the screen
    """
    def __init__(self):
        self.text = [] # [{"cash type":type,"how much money":money}...]
        self.colors = {
            "gold": user.gold_color,
            "iron": user.iron_color,
            "diamonds": user.diamond_color
        }
    def append(self,cash_type,money_earned):
        text_dict = {
            "cash type":cash_type,
            "how much money":money_earned,
            "alpha level": 255
        }
        self.text.append(text_dict)
    def draw_screen(self):
        for text in self.text:
            cash_type = text["cash type"]
            how_much_money = text["how much money"]
            alpha_level = text["alpha level"]
            to_blit_text = "+"+str(how_much_money)

            x = screen_x//2 - huge_font.size(to_blit_text)[0]//2
            y = screen_y//6

            blit_fade_text(window,to_blit_text,huge_font,alpha_level,(x-2,y-2),self.colors[cash_type])
            blit_fade_text(window,to_blit_text,huge_font,alpha_level,(x,y),(255,255,255))
        self.fade_text()
    def fade_text(self):
        index = 0
        for text in self.text:
            alpha_level = text["alpha level"]
            if alpha_level > 150:
                alpha_level -= 2
            else:
                alpha_level -= 4

            if alpha_level <= 0:
                self.text.remove(text)
            else:
                self.text[index]["alpha level"] = alpha_level
            index += 1
collect_money_effect = create_collect_money_effect()

loading_screen(phase=2)


class create_attack():
    def __init__(self):
        self.attacking = False
        self.show_done_attacking_screen = False

        # button
        self.button_size = shop.button_size # 60x60   image real size 600x600
        self.button_pos = (shop.button_pos[0]+shop.button_size[0]+10,screen_y-self.button_size[1]-10)
        self.button_rect = pygame.Rect(self.button_pos[0],self.button_pos[1],self.button_size[0],self.button_size[1])
        self.button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/attack base button.png"),self.button_size)
        self.button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/attack base button mouse on.png"),self.button_size)
        
        self.gold_coin_image = pygame.transform.smoothscale(user.gold_coin,(int(self.button_size[0]*0.4),int(self.button_size[1]*0.4)))
        self.gold_coin_image_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/gold coin 50 darker.png"),(int(self.button_size[0]*0.4),int(self.button_size[1]*0.4)))

        self.move_base_button_size = (int(60*2.36),60) # 650x275 1:0.42  2.36:1
        self.move_base_button_pos = (screen_x-self.move_base_button_size[0]-5,screen_y-self.button_size[1]-10)
        self.move_base_button_rect = pygame.Rect(self.move_base_button_pos[0],self.move_base_button_pos[1],self.move_base_button_size[0],self.move_base_button_size[1])
        self.move_base_button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/change base button.png"),self.move_base_button_size)
        self.move_base_button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/change base button mouse on.png"),self.move_base_button_size)

        self.base_here_sign_size = (50,50)
        self.base_here_sign = pygame.transform.smoothscale(pygame.image.load(folder+"/base here sign.png"),self.base_here_sign_size)
        self.base_here_sign.set_alpha(220) # fade it by 35 for a bit fade effect

        self.done_attack_screen_width,self.done_attack_screen_height = 500,500
        self.done_attack_screen_x,self.done_attack_screen_y = screen_x/2-self.done_attack_screen_width/2,  screen_y/2-self.done_attack_screen_height/2

        self.done_attack_backToBase_button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/back to base button in done attack screen.png"),(90,int(90*0.454))) # 666x303   1:0.454
        self.done_attack_backToBase_button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/back to base button in done attack screen mouse on.png"),(90,int(90*0.454))) # 666x303   1:0.454
        self.done_attack_backToBase_button_size = self.done_attack_backToBase_button.get_size()#(bigger_font.size("Back T")[0],bigger_font.size("B")[1]*1.8)
        self.done_attack_backToBase_button_pos = (screen_x//2-self.done_attack_backToBase_button_size[0]//2,self.done_attack_screen_y+self.done_attack_screen_height-self.done_attack_backToBase_button_size[1]*1.5)
        self.done_attack_backToBase_button_rect = pygame.Rect(self.done_attack_backToBase_button_pos[0],self.done_attack_backToBase_button_pos[1],self.done_attack_backToBase_button_size[0],self.done_attack_backToBase_button_size[1])
        
        self.buildings_health_line_size = (50,5)
        self.soldiers_health_line_size = (50,5)

        self.base_buildings = {} # id:{"building name":name,"pos":[x,y],"level":level,"frame":frame}
        self.destroyed_buildings = {} # id:{"building name":name,"pos":[x,y],"destroyed image":image}
        self.total_num_of_buildings = 0
        self.active_attack_time = None
        self.attack_time = 60*3 # 3 minutes
        self.tiles = [] # like the other tiles
        self.draw_sea = False
        self.attack_cost = 20 # 20 gold coins
        self.start_attacking = False
        self.soldiers_in_base = [] # {"soldier type":"type","soldier level":"level","pos":(x,y),"attack building":"building id"}
        self.card_size = (base_bg.tile_size*5,base_bg.tile_size*6)
        self.on_soldier_card = None
        self.on_soldier_card_level = None
        self.money_for_attack = {
            "iron":None,
            "gold":None,
            "diamonds":None
        }
        self.trophies_for_attack = None

        self.attacking_soldiers = {} # by id
        self.place_soldier_time_delay = 0.1 # you can place soldier every 0.1 seconds
        self.place_soldier_time = time.time()+self.place_soldier_time_delay

        self.buildings_space_radius = 150 # the space between every building center to the soldier(in a circle way)

        weapons_types = os.listdir(folder+"/army weapons")
        index = 0
        for weapon_type in weapons_types:
            weapon_type = weapon_type.split(".")[0]
            weapons_types[index] = weapon_type
            index += 1
        tile_size = base_bg.tile_size
        self.weapons_by_soldiers = {
            "rock machine":"rock ball",
            "killer drone":"lazer",
            "bomb":"bomb", # throwable
            "missile":"missile",
        }
        self.soldiers_by_weapons = {}
        for soldier_name,weapon_name in self.weapons_by_soldiers.items():
            self.soldiers_by_weapons[weapon_name] = soldier_name

        # soldiers weapons
        self.weapons_names = return_weapons_names()
        self.weapons_levels = return_weapons_levels()
        self.weapons_sizes = {
            "lazer":(int(tile_size*1*0.22),tile_size*1), # 143x649 0.22:1
            "rock ball":(int(tile_size*4*0.66666666666666666666666666666667),int(tile_size*4*0.66666666666666666666666666666667*0.968)) # 500x484   1:0.968
        }
        self.weapons_images = { } # weapon:{level:image...}
        
        index = 0
        for weapon_name in self.weapons_names:
            self.weapons_images[weapon_name] = {}
            for weapon_level in range(self.weapons_levels[index]):
                weapon_level = str(weapon_level+1)
                self.weapons_images[weapon_name][weapon_level] = pygame.transform.smoothscale(  pygame.image.load(folder+"/army weapons/"+weapon_name+"/"+weapon_level+".png"),self.weapons_sizes[weapon_name]  )
            index += 1

        self.weapons_speed = {
            "lazer":5,
            "rock ball":4,
            "bomb":7, # same as in the army class
            "missile":7
        }
        self.weapons_damage = army.army_fixed_info["weapons damage"]
        self.weapons_in_air = {} # {id:{name:name,angle:angle,attack_build_id:attack build id}}
        
        # buildings guns weapons
        self.buildings_guns_weapons_names = return_buildings_guns_weapons_names()
        self.buildings_guns_weapons_levels = return_buildings_guns_weapons_levels()
        self.buildings_guns_weapons_sizes = {
            "lazer":(int(tile_size*1*0.22),tile_size*1), # 143x649 0.22:1
        }
        self.buildings_guns_weapons_images = {} #  weapon:{level:image...}

        index = 0
        for weapon_name in self.buildings_guns_weapons_names:
            self.buildings_guns_weapons_images[weapon_name] = {}
            for weapon_level in range(self.buildings_guns_weapons_levels[index]):
                weapon_level = str(weapon_level+1)
                self.buildings_guns_weapons_images[weapon_name][weapon_level] = pygame.transform.smoothscale(  pygame.image.load(folder+"/army weapons/"+weapon_name+"/"+weapon_level+".png"),self.buildings_guns_weapons_sizes[weapon_name]  )
            index += 1
        self.buildings_guns_weapons_speed = {
            "lazer":5
        }
        self.buildings_guns_weapons_damage = {
            "lazer":{
                "1":15
            }
        }
        self.weapons_by_building_name = {
            "lazer tower":"lazer"
        }
        self.buildings_guns_weapons_shoot_delay = { # its by the bullet name
            "lazer tower":1
        } # {gun_name:time...}
        self.buildings_guns_weapons_in_air = {} # {id:{name:name,pos:(x,y),level:level,angle:angle,damage:damage}}


        # for the create attack function
        self.n_buildings_by_townhall_level = {}
        for level in buildings.max_of_each_building_by_townhall:
            self.n_buildings_by_townhall_level[level] = 0
            buildings1 = buildings.max_of_each_building_by_townhall[level]
            for build in buildings1.items():
                name,times = build
                self.n_buildings_by_townhall_level[level] += times
        self.sea_animation_image = pygame.transform.smoothscale(pygame.image.load(folder + "/sea animation change attack base.png").convert_alpha(), (screen_x,int(screen_x*0.3)))
        self.destroyed_building_animation = { # will change its size for each building
            "1":pygame.image.load(folder+"/destroy building animation/"+"1.png").convert_alpha(),
            "2":pygame.image.load(folder+"/destroy building animation/"+"2.png").convert_alpha(),
            "3":pygame.image.load(folder+"/destroy building animation/"+"3.png").convert_alpha()
        }
        self.explosion_frames = {} # 1-6
        self.explosions = {} # id:{pos:pos,frame:frame,change frame time:time}
        self.change_explosion_frame_time = 0.05
        bomb_size = army.army_images_sizes["bomb"]
        for num in range(1,7):
            path = folder+f"/explosion/{str(num)}.png"
            image = pygame.transform.smoothscale(pygame.image.load(path).convert_alpha(),bomb_size)
            self.explosion_frames[str(num)] = image
    # button outside attack screen
    def draw_button_in_normal(self):
        x,y = self.button_pos
        mouse = pygame.mouse.get_pos()
        if self.button_rect.collidepoint(mouse):
            window.blit(self.button_mouse_on,(x,y))
            window.blit(self.gold_coin_image_mouse_on,(x+self.button_size[0]-self.gold_coin_image.get_width()*1.4,y+self.button_size[1]-self.gold_coin_image.get_height()*1.28))
        else:
            window.blit(self.button,(x,y))
            window.blit(self.gold_coin_image,(x+self.button_size[0]-self.gold_coin_image.get_width()*1.4,y+self.button_size[1]-self.gold_coin_image.get_height()*1.28))
    def press_button_check_in_normal(self):
        mouse = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        if mouse_press[0] == True:
            mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)
            if self.button_rect.colliderect(mouse_rect):
                if army.soldiers_in_camp != {}:
                    if user.gold >= self.attack_cost:
                        self.base_buildings = {}
                        self.create_base()
                        user.gold -= self.attack_cost
                        user.save_cash_methods()
                        self.attacking_soldiers = {}
                        buildings.army_camp_moving_soldiers = [] # reset this so in the next time when being at the base it will reset
                        self.weapons_in_air = {}
                        self.buildings_guns_weapons_in_air = {}
                        self.attacking = True
                    else:
                        fade_red_text.append_text("You don't have enough money")
                else:
                    fade_red_text.append_text("You don't have soldiers to attack with")
    
    # button to move base
    def draw_move_base_button(self):
        x,y = self.move_base_button_pos
        mouse = pygame.mouse.get_pos()
        if self.move_base_button_rect.collidepoint(mouse):
            window.blit(self.move_base_button_mouse_on,(x,y))
            window.blit(self.gold_coin_image_mouse_on,(x+self.gold_coin_image.get_width()*1.7,y+self.move_base_button_size[1]-self.gold_coin_image.get_height()*1.28))
        else:
            window.blit(self.move_base_button,(x,y))
            window.blit(self.gold_coin_image,(x+self.gold_coin_image.get_width()*1.7,y+self.move_base_button_size[1]-self.gold_coin_image.get_height()*1.28))
    def press_move_base_button_check(self):
        mouse = pygame.mouse.get_pos()
        mouse_press = pygame.mouse.get_pressed()
        if self.show_done_attacking_screen == False:
            if mouse_press[0] == True:
                mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)
                if self.move_base_button_rect.colliderect(mouse_rect):
                    if user.gold >= self.attack_cost:
                        # move the wave
                        wave_height = -self.sea_animation_image.get_height()
                        while wave_height <= screen_y+self.sea_animation_image.get_height():
                            self.draw_tiles()
                            for build_id in self.base_buildings:
                                building = self.base_buildings[build_id]
                                name = building["building name"]
                                x,y = building["pos"]
                                level = building["level"]
                                build_image = buildings.buildings_images[name][level]
                                window.blit(build_image, (x,y))
                                # bliting the gun
                                if name in buildings.attacking_buildings_guns_by_building_name:
                                    gun_name  = buildings.attacking_buildings_guns_by_building_name[name]
                                    gun_image = pygame.transform.rotate(buildings.buildings_guns_images[gun_name][level],building["gun angle"])
                                    gun_pos = (x + build_image.get_width()//2-gun_image.get_width()//2,y + build_image.get_height()//2-gun_image.get_height()//2)
                                    window.blit(gun_image, gun_pos)
                            user.draw_payment_methods()
                            pygame.draw.rect(window, (0,160,222), [0,0,screen_x,wave_height])
                            window.blit(self.sea_animation_image, (0,wave_height-10))
                            wave_height += 5
                            
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                            pygame.display.update()
                            
                        self.base_buildings = {}
                        self.weapons_in_air = {}
                        self.buildings_guns_weapons_in_air = {}
                        self.attacking_soldiers = {}
                        self.tiles = []
                        self.create_base()
                        user.gold -= self.attack_cost
                        user.save_cash_methods()

                        # fading the sea for the buildings(after that while the buildings will show)
                        alpha_level = 250
                        while alpha_level >= 1:
                            for build_id in self.base_buildings:
                                building = self.base_buildings[build_id]
                                name = building["building name"]
                                x,y = building["pos"]
                                level = building["level"]
                                build_image = buildings.buildings_images[name][level]
                                window.blit(build_image, (x,y))
                                # bliting the gun
                                if name in buildings.attacking_buildings_guns_by_building_name:
                                    gun_name  = buildings.attacking_buildings_guns_by_building_name[name]
                                    gun_image = pygame.transform.rotate(buildings.buildings_guns_images[gun_name][level],building["gun angle"])
                                    gun_pos = (x + build_image.get_width()//2-gun_image.get_width()//2,y + build_image.get_height()//2-gun_image.get_height()//2)
                                    window.blit(gun_image, gun_pos)
                            user.draw_payment_methods()
                            draw_transparent_square(window,(screen_x,screen_y),alpha_level,(0,160,222),(0,0))
                            
                            if alpha_level <= 150:
                                alpha_level -= 1
                            else:
                                alpha_level -= 2
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                            pygame.display.update()
                        # fading the sea for the tiles(after that while the tiles will show)
                        alpha_level = 250
                        while alpha_level >= 1:
                            self.draw_tiles()
                            draw_transparent_square(window,(screen_x,screen_y),alpha_level,(0,160,222),(0,0))
                            for build_id in self.base_buildings:
                                building = self.base_buildings[build_id]
                                name = building["building name"]
                                x,y = building["pos"]
                                level = building["level"]
                                build_image = buildings.buildings_images[name][level]
                                window.blit(build_image, (x,y))
                                # bliting the gun
                                if name in buildings.attacking_buildings_guns_by_building_name:
                                    gun_name  = buildings.attacking_buildings_guns_by_building_name[name]
                                    gun_image = pygame.transform.rotate(buildings.buildings_guns_images[gun_name][level],building["gun angle"])
                                    gun_pos = (x + build_image.get_width()//2-gun_image.get_width()//2,y + build_image.get_height()//2-gun_image.get_height()//2)
                                    window.blit(gun_image, gun_pos)
                            user.draw_payment_methods()
                            
                            if alpha_level <= 150:
                                alpha_level -= 1
                            else:
                                alpha_level -= 2
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    exit()
                            pygame.display.update()
                        print("Base changed")
                    else:
                        fade_red_text.append_text("You don't have enough money")

    # create and draw base
    def check_build_on_tiles(self,build_x,build_y,build_width,build_height): # gets a building rect and check if its on the tiles, not on the sea
        tiles_x,tiles_y = self.tiles[1][0],self.tiles[1][1]
        tiles_width = base_bg.tile_size*100
        tiles_height = tiles_width

        good_pos = True

        if build_x + build_width > tiles_x + tiles_width:
            good_pos = False
        elif build_x < tiles_x: # doing this with build_x and not with build_x+build_width because even if the smallest part is in the sea the pos is not good
            good_pos = False
        elif build_y + build_height > tiles_y + tiles_height:
            good_pos = False
        elif build_y < tiles_y:
            good_pos = False
        return good_pos
    def create_base(self):
        self.destroyed_buildings = {}
        self.tiles = base_bg.tiles

        possible_positions = [] # in columns (same x y change until...)
        start_pos = base_bg.tiles[1]
        start_x,start_y = start_pos[:2]
        end_pos = base_bg.tiles[-1]
        end_x,end_y = end_pos[0],end_pos[1]
        for x in range(start_x,end_x,base_bg.tile_size):
            for y in range(start_y,end_y,base_bg.tile_size):
                possible_positions.append((x,y))
        
        # place the townhall
        townhall_level = str(random.randint( 1,int(list(buildings.max_upgrade_of_each_building_by_townhall["townhall"])[-1] ) ))
        townhall =  {
                "building name": "townhall",
                "pos": [],
                "level": townhall_level,
                "frame": "1",
                "health":buildings.buildings_health["townhall"][townhall_level],
                "condition":"normal", # normal-not attacked, under attack-under attack, destroyed=destroyed
            }
        good_townhall_pos = False
        while good_townhall_pos == False:
            x,y = possible_positions[random.randint(0,len(possible_positions)-1)]
            if x + buildings.buildings_sizes[townhall["building name"]][0] <= possible_positions[-1][0] and \
                y + buildings.buildings_sizes[townhall["building name"]][1] <= possible_positions[-1][1]:
                townhall["pos"] = (x,y)
                good_townhall_pos = True
        self.base_buildings["1"] = townhall
        
        # place the other things
        """algorithm explanatin:
        gets the building name
        gets width,height
        gets all of the positions that are possible around the buildings that have been placed
        place the building in a random place from the ones in the phase before
        redo it with the next one"""
        possible_positions = []
        
        # appending the buildings names(each can be more then 1)
        buildings_to_build = []
        townhall_level = townhall["level"]
        while len(buildings_to_build) != self.n_buildings_by_townhall_level[townhall_level]:
            random_build = buildings.buildings_names[random.randint(0,len(buildings.buildings_names)-1)]
            if random_build != "townhall":
                n_times_by_townhall = buildings.max_of_each_building_by_townhall[townhall_level][random_build]
                times_now = buildings_to_build.count(random_build)
                if times_now < n_times_by_townhall:
                    buildings_to_build.append(random_build)

        # implementing the buildings names to buildings and adding to the dict
        for name in buildings_to_build:
            width,height = buildings.buildings_sizes[name]
            place_build_x,place_build_y = None,None
            # getting the possible positions
            # going over every building that has been placed and gets all of the positions around it into the possible_positions list: [(x,y),(x,y),(x,y)...]
            for build_id in self.base_buildings:
                build = self.base_buildings[build_id]
                x,y = build["pos"]
                build_width,build_height = buildings.buildings_sizes[build["building name"]]
                # set the "base" position (lest to the building)
                if place_build_x == None and place_build_y == None:
                    place_build_x,place_build_y = x - width,y
                possible_positions.append((place_build_x,place_build_y))
                # set all of the other positions(around the building)
                placed_all = False
                iterations = 0
                """the iterations is a system for if the loop does not go well it will run only 50 times"""
                while placed_all == False and iterations < 50:
                    # changing the positions
                    # (changing the x/y by how much we need)
                    # changing the x,y every time by adding the tile size(for more possible positions)
                    if place_build_x == x - width: # left to the building
                        if not place_build_y == y + build_height:
                            place_build_y += base_bg.tile_size
                    elif place_build_x == x + build_width: # right to the building
                        if not place_build_y == y - height:
                            place_build_y -= base_bg.tile_size

                    if place_build_y == y + build_height: # under the building
                        if not place_build_x == x + build_width:
                            place_build_x += base_bg.tile_size
                    elif place_build_y == y - height: # above the building
                        if not place_build_x == x:
                            place_build_x -= base_bg.tile_size
                    
                    # y fix
                    if place_build_y > y + build_height:
                        place_build_y = y + build_height
                    elif place_build_y < y - height:
                        place_build_y = y - height
                    # x fix
                    if place_build_x > x + build_width:
                        place_build_x = x+build_width
                    elif place_build_x < x - width:
                        place_build_x = x - width
                    
                    if place_build_x <= x - width and place_build_y <= y - height:
                        placed_all = True


                    if (place_build_x,place_build_y) not in possible_positions:
                        possible_positions.append((place_build_x,place_build_y))
                    iterations += 1
                place_build_x,place_build_y = None,None
                
            
            # deciding the final position
            final_pos = possible_positions[random.randint(0,len(possible_positions)-1)]
            final_x = final_pos[0]
            final_y = final_pos[1]
            size = buildings.buildings_sizes[name]
            # check if the position is good and possible(DO NOT CHANGE)
            # check if the building is on another one, if yes it gets the random position again and do the check again
            good_pos = False
            while good_pos == False:
                build_rect = pygame.Rect(final_x,final_y,size[0],size[1])
                colide = False
                for build_id in self.base_buildings:
                    x,y = self.base_buildings[build_id]["pos"]
                    build_size = buildings.buildings_sizes[self.base_buildings[build_id]["building name"]]
                    check_on_build_rect = pygame.Rect(x,y,build_size[0],build_size[1])
                    if build_rect.colliderect(check_on_build_rect):
                        colide = True
                if colide == False:
                    # the pos is good
                    if self.check_build_on_tiles(final_x,final_y,size[0],size[1]) == True:
                        good_pos = True
                if good_pos == False:
                    final_pos = possible_positions[random.randint(0,len(possible_positions)-1)]
                    final_x = final_pos[0]
                    final_y = final_pos[1]
            # making the building dict and implementing in the self. dict
            final_townhall_level = townhall_level
            done = False
            while done == False:
                try:
                    build_level = str( random.randint(1,int(buildings.max_upgrade_of_each_building_by_townhall[name][final_townhall_level])) )
                    if int(buildings.max_upgrade_of_each_building_by_townhall[name][final_townhall_level]) == 1:
                        build_level = "1"
                    done = True
                except:
                    final_townhall_level = int(final_townhall_level)
                    final_townhall_level -= 1
                final_townhall_level = str(final_townhall_level)
            build = {
                "building name":name,
                "pos":[
                    final_x,final_y
                ],
                "level":build_level,
                "frame":"1",
                "health":buildings.buildings_health[name][build_level],
                "condition":"normal", # normal-not attacked, under attack-under attack, destroyed=destroyed
            }
            if name in buildings.attacking_buildings_guns_by_building_name:
                angle = random.randint(1,360)
                build["gun angle"] = angle
                build["shoot time"] = time.time() + self.buildings_guns_weapons_shoot_delay[name]
                build["attack soldier id"] = None
            
            new_id = str(int(list(self.base_buildings)[-1])+1)
            self.base_buildings[new_id] = build
        self.total_num_of_buildings = len(self.base_buildings)

        n_iron_mines = 0
        n_gold_mines = 0
        n_diamonds_mines = 0
        for build_id in self.base_buildings:
            building = self.base_buildings[build_id]
            name = building["building name"]
            level = building["level"]
            if "iron mine" == name:
                n_iron_mines += int(level)
            elif "gold mine" == name:
                n_gold_mines += int(level)
            elif "diamonds mine" == name:
                n_diamonds_mines += int(level)
        self.money_for_attack["iron"] = n_iron_mines * 200
        self.money_for_attack["gold"] = n_gold_mines * 200
        self.money_for_attack["diamonds"] = n_diamonds_mines * 50
        self.trophies_for_attack = int(townhall_level) * random.randint(8,10) # you can get between 8-10 multiply by the townhall level

    def draw_attack_base(self):
        # draw the transparent circles behind the buildings(the circles of where he cant place soldiers)
        transparent_circle_positions = [] # [(x,y),(x,y),(x,y),(x,y)...]
        # append to the list
        for build_id in self.base_buildings:
            building = self.base_buildings[build_id]
            name = building["building name"]
            x,y = building["pos"]
            # draw the circle of the places he cant place the soldiers in
            transparent_circle_positions.append((x+buildings.buildings_sizes[name][0]//2,y+buildings.buildings_sizes[name][1]//2))
        # draw the positions from the list
        for transparent_circle_pos in transparent_circle_positions:
            x,y = transparent_circle_pos
            draw_transparent_circle(window,x,y,self.buildings_space_radius,(255,0,0),50)

        button_pos = ()
        point_size = self.base_here_sign_size[0]
        buildings_above_line_info = [] # {"pos":(x,y),"health":num,"max health":num}
        # draw buildings
        for build_id in self.base_buildings:
            building = self.base_buildings[build_id]
            name = building["building name"]
            x,y = building["pos"]
            level = building["level"]

            
            # draw the circle of the places he cant place the soldiers in
            transparent_circle_positions.append((x+buildings.buildings_sizes[name][0]//2,y+buildings.buildings_sizes[name][1]//2))
            #draw_transparent_circle(window,x+buildings.buildings_sizes[name][0]//2,y+buildings.buildings_sizes[name][1]//2,self.buildings_space_radius,(0,0,0),50)

            build_image = buildings.buildings_images[name][level]
            window.blit(build_image, (x,y))
            # bliting the gun
            if name in buildings.attacking_buildings_guns_by_building_name:
                gun_angle = building["gun angle"]
                if gun_angle == None:
                    gun_angle = 0
                gun_name  = buildings.attacking_buildings_guns_by_building_name[name]
                gun_image = pygame.transform.rotate(buildings.buildings_guns_images[gun_name][level],gun_angle)
                gun_pos = (x + build_image.get_width()//2-gun_image.get_width()//2,y + build_image.get_height()//2-gun_image.get_height()//2)
                window.blit(gun_image, gun_pos)

            buildings_above_line_info.append({"pos":(x+buildings.buildings_sizes[name][0]//2-self.buildings_health_line_size[0]//2,y-self.buildings_health_line_size[1]*2),  "health":building["health"],"max health":buildings.buildings_health[name][str(level)]})
            if name == "townhall":
                townhall_rect = pygame.Rect(x,y,buildings.buildings_sizes[name][0],buildings.buildings_sizes[name][1])
                if not townhall_rect.colliderect(pygame.Rect(0,0,screen_x,screen_y)):
                    # draw an arrow that points to the townhall
                    new_x = x
                    new_y = y
                    if new_x > screen_x: new_x = screen_x - point_size*1.5
                    if new_x < 0: new_x = point_size*0.5
                    if new_y > screen_y: new_y = screen_y - point_size*1.5
                    if new_y < 0: new_y = point_size*0.5
                    button_pos = (new_x,new_y)
            # if its a shooting building it will re get the angle... and shoot at the soldier
            if name in self.buildings_guns_weapons_shoot_delay:
                if self.attacking_soldiers != {}:
                    building["gun angle"] = None
                    building["angle change pos needed"] = None
                    # getting the closest soldier and its angle...
                    closest_soldier_id = None
                    closest_soldier_distance = None
                    closest_soldier_pos = None
                    for soldier_id in self.attacking_soldiers:
                        # soldier => {'name':'killer drone','level':2,'pos':(378,429),'attacking build id':'3','going angle':321.16084289761847,'shoot time':1662809667}
                        soldier = self.attacking_soldiers[soldier_id]
                        if soldier["name"] != "missile" and soldier["name"] != "bomb":
                            soldier_pos = soldier["pos"]
                            dist_x = x - soldier_pos[0]
                            dist_y = y - soldier_pos[1]
                            # using the pythagorean theorem(משפט פיתגורס)
                            dist_from_soldier_to_building = math.sqrt(math.pow(dist_x,2) + math.pow(dist_y,2))
                            if closest_soldier_id == None or closest_soldier_distance > dist_from_soldier_to_building:
                                closest_soldier_id = soldier_id
                                closest_soldier_distance = dist_from_soldier_to_building
                                closest_soldier_pos = soldier_pos
                    if closest_soldier_id != None:
                        angle = self.get_angle_between_two_points((x,y),closest_soldier_pos)
                        building["gun angle"] = angle
                        building["attack soldier id"] = closest_soldier_id

                        # shooting by the gun angle
                        if building["shoot time"] < time.time():
                            bullet_id = "1"
                            try:
                                bullet_id = str(int(list(self.buildings_guns_weapons_in_air)[-1])+1)
                            except IndexError:
                                pass
                            weapon_name = self.weapons_by_building_name[name]
                            closest_soldier_size = army.army_images_sizes[self.soldiers_by_weapons[weapon_name]]
                            #id:{name:name,pos:(x,y),level:level,angle:angle,damage:damage}
                            bullet_dict = {
                                "name":weapon_name,
                                "pos":(x + build_image.get_width()//2,y+build_image.get_height()//2),
                                "level":level,
                                "angle":None,
                                "attack soldier pos":(closest_soldier_pos[0]+closest_soldier_size[0]//2,closest_soldier_pos[1]+closest_soldier_size[1]//2),
                                "iteration":0,
                                "damage":self.buildings_guns_weapons_damage[weapon_name][level]
                            }
                            self.buildings_guns_weapons_in_air[bullet_id] = bullet_dict
                            building["shoot time"] = time.time() + self.buildings_guns_weapons_shoot_delay[name]
        # the health line above the buildings
        for building_info in buildings_above_line_info:
            pos = building_info["pos"]
            health = building_info["health"]
            max_health = building_info["max health"]
            health_percent = health/max_health
            if health != max_health: # will draw the line
                pygame.draw.rect(window,(0,0,0),[pos[0]-2,pos[1]-2,self.buildings_health_line_size[0]+4,self.buildings_health_line_size[1]+4],2)
                pygame.draw.rect(window,(0,255,0),[pos[0],pos[1],int(self.buildings_health_line_size[0]*health_percent),self.buildings_health_line_size[1]])
        if button_pos != ():
            window.blit(self.base_here_sign,button_pos)
            #pygame.draw.rect(window, (0,0,0), [button_pos[0],button_pos[1],point_size,point_size])
            #window.blit(small_font.render("Base",True,(255,255,0)), button_pos)
            #window.blit(small_font.render("here",True,(255,255,0)), (button_pos[0],button_pos[1]+small_font.size("B")[1]*1.5))
        self.draw_soldiers_cards()
        if self.start_attacking == False:
            user.draw_payment_methods()
        if self.show_done_attacking_screen == False:
            self.draw_move_base_button()
            self.press_move_base_button_check()
    def draw_tiles(self):
        if self.draw_sea == True:
            window.fill((0,160,222))
        for tile in self.tiles[1:]:
            if screen_rect.colliderect(pygame.Rect(tile[0],tile[1],base_bg.tile_size,base_bg.tile_size)):
                window.blit(base_bg.tile[tile[3]],(tile[0],tile[1]))
        pygame.draw.rect(window, self.tiles[0][2], [self.tiles[0][0]+2,self.tiles[0][1]+2,base_bg.tile_size-4,base_bg.tile_size-4]) # red
        pygame.draw.rect(window, (255,255,0), [self.tiles[0][0]+base_bg.tile_size//2//2,self.tiles[0][1]+base_bg.tile_size//2//2 # yellow
            ,base_bg.tile_size//2,base_bg.tile_size//2])
    def draw_soldiers_cards(self):
        soldiers_types = [] # {"name":name,"level":level}
        num_of_each = {}
        for soldier_id in army.soldiers_in_camp:
            soldier = army.soldiers_in_camp[soldier_id]
            soldier_dict = {"name":soldier["name"],"level":soldier["level"]}
            if soldier_dict not in soldiers_types:
                soldiers_types.append(soldier_dict)
            if soldier["name"] not in num_of_each:
                num_of_each[soldier["name"]] = 1
            else:
                num_of_each[soldier["name"]] += 1
        x = 10
        y = screen_y - self.card_size[1]-10
        for soldier_type_dict in soldiers_types:
            draw_transparent_square(window,self.card_size,150,(0,0,0),(x,y))

            window.blit(small_font.render("x"+str(num_of_each[soldier_type_dict["name"]]),True,(255,255,255)),(x+self.card_size[0]-small_font.size("x"+str(num_of_each[soldier_type_dict["name"]]))[0]-3,y))
            image = army.army_images[soldier_type_dict["name"]][str(soldier_type_dict["level"])]
            window.blit(image, (x+self.card_size[0]//2-image.get_width()//2, y+small_font.size("x1")[1]*1.5))
            window.blit(font.render("Level: "+str(soldier_type_dict["level"]),True,(255,255,255)),(x,y+self.card_size[1]-font.size("P")[1]))

            # draw the card that the user is currently on
            if soldier_type_dict["name"] == self.on_soldier_card:
                pygame.draw.rect(window, (255,255,255),[x,y,self.card_size[0],self.card_size[1]],1)

            x += self.card_size[0] + 5
    def move(self,to):
        # to = "up"/"down"/"left"/"right"
        tiles_copy = self.tiles.copy()
        x_change = 0
        y_change = 0
        if to == "left": # left
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                x += movement.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
            x_change += movement.move_speed
        elif to == "right": # right
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                x -= movement.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
            x_change -= movement.move_speed
        elif to == "up": # up
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                y += movement.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
            y_change += movement.move_speed
        else: # down
            index = 0
            for tile in tiles_copy:
                x,y,color,image = tile
                y -= movement.move_speed
                tiles_copy[index] = (x,y,color,image)
                index += 1
            y_change -= movement.move_speed
        rightest = self.tiles[1]
        leftest = self.tiles[1] # this one wont change in the loop(first one always leftest+toppest)
        toppest = self.tiles[1] # this one wont change in the loop(first one always leftest+toppest)
        lowest = self.tiles[-1]

        for tile in self.tiles:
            x,y,color,image = tile
            if x > rightest[0]:
                rightest = tile
            if y > lowest[1]:
                lowest = tile
        update_pos = True
        self.draw_sea = False
        # the sea is 3 tiles long
        sea_size = self.card_size[1]+base_bg.tile_size
        if leftest[0] - sea_size + base_bg.tile_size > 0 and to == "left":
            update_pos = False
        elif rightest[0] + sea_size < screen_x and to == "right":
            update_pos = False
        if toppest[1] - sea_size + base_bg.tile_size > 0 and to == "up":
            update_pos = False
        elif lowest[1] + sea_size < screen_y and to == "down":
            update_pos = False
    
        if leftest[0] + base_bg.tile_size >= 0:
            self.draw_sea = True
        if rightest[0] <= screen_x:
            self.draw_sea = True
        if toppest[1] + base_bg.tile_size >= 0:
            self.draw_sea = True
        if lowest[1] <= screen_y:
            self.draw_sea = True

        if update_pos == False: # in case the ifs above do not work well
            self.draw_sea = True
        if update_pos == True:
            for build_id in self.base_buildings:
                self.base_buildings[build_id]["pos"] = (
                    self.base_buildings[build_id]["pos"][0] + x_change,
                    self.base_buildings[build_id]["pos"][1] + y_change)
            for build_id in self.destroyed_buildings:
                self.destroyed_buildings[build_id]["pos"] = (
                    self.destroyed_buildings[build_id]["pos"][0] + x_change,
                    self.destroyed_buildings[build_id]["pos"][1] + y_change)
            for weapon_id in self.weapons_in_air:
                self.weapons_in_air[weapon_id]["pos"] = (
                    self.weapons_in_air[weapon_id]["pos"][0] + x_change,
                    self.weapons_in_air[weapon_id]["pos"][1] + y_change
                )
            for weapon_id in self.buildings_guns_weapons_in_air:
                self.buildings_guns_weapons_in_air[weapon_id]["pos"] = (
                    self.buildings_guns_weapons_in_air[weapon_id]["pos"][0] + x_change,
                    self.buildings_guns_weapons_in_air[weapon_id]["pos"][1] + y_change
                )
            for explode_id in self.explosions:
                explosion = self.explosions[explode_id]
                explosion["pos"] = (explosion["pos"][0] + x_change,explosion["pos"][1] + y_change)
            self.tiles = tiles_copy
            for soldier_id in self.attacking_soldiers:
                soldier = self.attacking_soldiers[soldier_id]
                soldier["pos"] = (soldier["pos"][0] + x_change,soldier["pos"][1] + y_change)
                if soldier["name"] == "bomb" or soldier["name"] == "missile":
                    soldier["shoot at"] = (soldier["shoot at"][0] + x_change,soldier["shoot at"][1] + y_change)
    def handle_keyboard(self): # move buildings
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            print("move left")
            self.move("left")
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            print("move right")
            self.move("right")
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            print("move up")
            self.move("up")
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            print("move down")
            self.move("down")
        if keys[pygame.K_ESCAPE]:
            self.reset_class()
            self.attacking = False
    
    def handle_soldiers_nav(self):
        pressed_mouse = pygame.mouse.get_pressed()
        if pressed_mouse[0] == True:
            soldiers_types = [] # {"name":name,"level":level}
            num_of_each = {}
            for soldier_id in army.soldiers_in_camp:
                soldier = army.soldiers_in_camp[soldier_id]
                soldier_dict = {"name":soldier["name"],"level":soldier["level"]}
                if soldier_dict not in soldiers_types:
                    soldiers_types.append(soldier_dict)
                if soldier["name"] not in num_of_each:
                    num_of_each[soldier["name"]] = 1
                else:
                    num_of_each[soldier["name"]] += 1
            
            mouse = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)

            x = 10
            y = screen_y - self.card_size[1]-10
            for soldier_type_dict in soldiers_types:
                soldier_card_rect = pygame.Rect(x,y,self.card_size[0],self.card_size[1])
                if soldier_card_rect.colliderect(mouse_rect):
                    self.on_soldier_card = soldier_type_dict["name"]
                    self.on_soldier_card_level = soldier_type_dict["level"]
                x += self.card_size[0] + 5
    # handle all of the soldiers stuff
    def place_soldiers(self):
        if self.on_soldier_card != None:
            mouse_press = pygame.mouse.get_pressed()
            if mouse_press[0] == True: # left button
                mouse = pygame.mouse.get_pos()
                mouse_rect = pygame.Rect(mouse[0],mouse[1],1,1)

                can_place = True
                # on building
                for build_id in self.base_buildings:
                    build = self.base_buildings[build_id]
                    x,y = build["pos"]
                    width,height = buildings.buildings_sizes[build["building name"]]
                    build_rect = pygame.Rect(x,y,width,height)
                    if build_rect.colliderect(mouse_rect):
                        can_place = False
                    
                    else:
                        name = build["building name"]
                        circle_pos = (x+buildings.buildings_sizes[name][0]//2,y+buildings.buildings_sizes[name][1]//2)
                        not_place = False
                        not_place = self.check_soldier_in_building_radius(circle_pos[0],circle_pos[1],mouse[0],mouse[1]) #                                             (x,y)
                        soldier_size = army.army_images_sizes[self.on_soldier_card]
                        if not_place == False:
                            not_place = self.check_soldier_in_building_radius(circle_pos[0],circle_pos[1],mouse[0]+soldier_size[0],mouse[1]) #                         (x+,y)
                            if not_place == False:
                                not_place = self.check_soldier_in_building_radius(circle_pos[0],circle_pos[1],mouse[0],mouse[1]+soldier_size[1]) #                     (x,y+)
                                if not_place == False:
                                    not_place = self.check_soldier_in_building_radius(circle_pos[0],circle_pos[1],mouse[0]+soldier_size[0],mouse[1]+soldier_size[1]) # (x+,y+)
                        if not_place == True: # cant place
                            can_place = False

                
                if self.on_soldier_card == "bomb" or self.on_soldier_card == "missile": # the bomb needs to be placed on a building
                    can_place = True

                # on the cards nav
                if mouse[1] >= screen_y - self.card_size[1]-10:
                    can_place = False

                if can_place == True:
                    if self.on_soldier_card != None and self.place_soldier_time <= time.time():
                        x,y = mouse
                        soldier_id = 1
                        try:
                            soldier_id  = int(list(self.attacking_soldiers)[-1])+1
                        except:
                            pass
                        try:
                            self.start_attacking = True
                            found_soldier = False
                            for soldier_id_in_army_camp in army.soldiers_in_camp:
                                soldier = army.soldiers_in_camp[soldier_id_in_army_camp]
                                if self.on_soldier_card == soldier["name"]:
                                    army.capacity -= army.soldiers_info_when_appending[soldier["name"]]["capacity"]
                                    health = army.soldiers_health[soldier["name"]][str(soldier["level"])]
                                    soldier_dict = {
                                        "name":self.on_soldier_card,
                                        "level":self.on_soldier_card_level,
                                        "pos": (x,y-army.army_images_sizes[soldier["name"]][1]//2),
                                        "attacking build id":None,
                                        "going angle":None,
                                        "shoot time":None, # starts in None (shoots at the second the user places it)
                                        "health":health,
                                    }
                                    if self.on_soldier_card == "bomb" or self.on_soldier_card == "missile":
                                        soldier_dict.pop("attacking build id")
                                        soldier_dict.pop("going angle")
                                        soldier_dict.pop("shoot time")
                                        soldier_dict["shoot at"] = mouse # the pos he is being shot at
                                        soldier_dict["pos"] = (x,0-army.army_images_sizes[soldier["name"]][1])
                                        soldier_dict["speed"] = army.army_soldiers_speed[self.on_soldier_card]
                                    self.attacking_soldiers[str(soldier_id)] = soldier_dict
                                    print("placed soldier")
                                    army.soldiers_in_camp.pop(soldier_id_in_army_camp)
                                    found_soldier = True
                            if found_soldier == False:
                                # need that it wont add a soldier and it will happen if an error will raise
                                raise TypeError
                        except: # when removing some soldiers from the camp and still running it can cause an error
                            pass

                        # reset the time
                        self.place_soldier_time = time.time()+self.place_soldier_time_delay
                        army.save_army()
    def get_angle_between_two_points(self,point1,point2):
        """took the angle line code from here:
        https://stackoverflow.com/questions/20162302/pygame-point-image-towards-mouse"""
        angle = 360-math.atan2(point2[1]-point1[1],point2[0]-point1[0])*180/math.pi +100

        return angle
    def move_by_angle_and_speed(self,old_xy,speed,angle):
        new_x,new_y = old_xy

        movement_x = math.cos(angle) * speed
        movement_y = math.sin(angle) * speed
        new_x -= movement_x
        new_y += movement_y

        return new_x, new_y

    def draw_soldiers(self):
        for soldier_id in self.attacking_soldiers:
            soldier = self.attacking_soldiers[soldier_id]
            image = army.army_images[soldier["name"]][str(soldier["level"])]
            x,y = soldier["pos"]

            if soldier["name"] != "bomb" and soldier["name"] != "missile":
                try:
                    build_x,build_y = None,None
                    space_between_build_and_soldier = None # math.dist((x,y),(x,y)), gets the space between the two points
                    closest_build_id = None
                    build_name = None
                    # math.dist() returns the length of the line between the points, it ALWAYS returns positive numbers
                    for build_id in self.base_buildings:
                        build = self.base_buildings[build_id]
                        x1,y1 = build["pos"]
                        if closest_build_id == None: # it means that the y is also None
                            build_x,build_y = x1,y1
                            space_between_build_and_soldier = math.dist((x,y),(x1,y1))
                            closest_build_id = build_id
                            build_name = build["building name"]
                        else:
                            # if its not the first time
                            space_between_the_soldier_to_building = math.dist((x,y),(x1,y1))
                            if space_between_the_soldier_to_building < space_between_build_and_soldier:
                                build_x,build_y = x1,y1
                                space_between_build_and_soldier = math.dist((x,y),(x1,y1))
                                closest_build_id = build_id
                                build_name = build["building name"]

                    soldier_center_pos = (x+army.army_images_sizes[soldier["name"]][0]//2,y+army.army_images_sizes[soldier["name"]][1]//2)
                    build_center_pos = (build_x+buildings.buildings_sizes[build_name][0]//2,build_y+buildings.buildings_sizes[build_name][0]//2)
                    angle_between_the_points = self.get_angle_between_two_points( soldier_center_pos, build_center_pos )
                    image = pygame.transform.rotate(image, angle_between_the_points)
                    if soldier["attacking build id"] == None: # if he is not attacking a building
                        soldier["attacking build id"] = closest_build_id
                        self.base_buildings[str(closest_build_id)]
                    
                    if soldier["going angle"] != None:
                        space_between_angles = soldier["going angle"] - angle_between_the_points
                        if space_between_angles > 20 or space_between_angles < -20:
                            pass
                        else:
                            soldier["going angle"] = angle_between_the_points
                    else:
                        soldier["going angle"] = angle_between_the_points
                    
                except Exception as e:
                    pass
                window.blit(image, (x,y))
            elif soldier["name"] == "bomb" or soldier["name"] == "missile":
                if soldier["name"] == "missile":
                    window.blit(pygame.transform.rotate(image,180), (x,y))
                else:
                    window.blit(image, (x,y))

            health = soldier["health"]
            max_health = army.soldiers_health[soldier["name"]][str(soldier["level"])]
            if health != max_health:
                health_percent = health/max_health
                pygame.draw.rect(window,(0,0,0),[x-2,y-2,self.soldiers_health_line_size[0]+4,self.soldiers_health_line_size[1]+4],2)
                pygame.draw.rect(window,(0,255,0),[x,y,int(self.soldiers_health_line_size[0]*health_percent),self.soldiers_health_line_size[1]])

    def check_soldier_in_building_radius(self,circle_x,circle_y,soldier_x,soldier_y):
        """same function as check in but returns the opposite"""
        sqx = (soldier_x - circle_x) ** 2
        sqy = (soldier_y - circle_y) ** 2
        if math.sqrt(sqx + sqy) < self.buildings_space_radius:
            return True
        else:
            return False
    def move_soldiers(self):
        to_pop_ids = [] # for the throwable weapons
        for soldier_id in self.attacking_soldiers:
            soldier = self.attacking_soldiers[soldier_id]
            if soldier["name"] != "bomb" and soldier["name"] != "missile":
                if soldier["attacking build id"] != None:
                    soldier_speed = army.army_soldiers_speed[soldier["name"]]
                    soldier_angle = soldier["going angle"]
                    x,y = soldier["pos"]
                    attack_build = self.base_buildings[soldier["attacking build id"]]
                    attack_build_pos = attack_build["pos"]
                    build_size = buildings.buildings_sizes[attack_build["building name"]]
                    attack_build_center_pos = (attack_build_pos[0]+build_size[0]//2,attack_build_pos[1]+build_size[1]//2)
                    """the check here checks if the soldier needs to keep moving or not(if entered the radius of the building(same radius for every building))"""
                    not_move = False
                    not_move = self.check_soldier_in_building_radius(attack_build_center_pos[0],attack_build_center_pos[1],x,y) #                                             (x,y)
                    soldier_size = army.army_images_sizes[soldier["name"]]
                    if not_move == False:
                        not_move = self.check_soldier_in_building_radius(attack_build_center_pos[0],attack_build_center_pos[1],x+soldier_size[0],y) #                         (x+,y)
                        if not_move == False:
                            not_move = self.check_soldier_in_building_radius(attack_build_center_pos[0],attack_build_center_pos[1],x,y+soldier_size[1]) #                     (x,y+)
                            if not_move == False:
                                not_move = self.check_soldier_in_building_radius(attack_build_center_pos[0],attack_build_center_pos[1],x+soldier_size[0],y+soldier_size[1]) # (x+,y+)

                    if not_move == False:
                        new_x,new_y = self.move_by_angle_and_speed((x,y),soldier_speed,soldier_angle)
                        soldier["pos"] = (new_x,new_y)
                    else: # not move == True
                        if soldier["shoot time"] == None or soldier["shoot time"] <= time.time():
                            weapon_id = "1"
                            try:
                                weapon_id = str(int(list(self.weapons_in_air)[-1])+1)
                            except: pass

                            weapon_name = self.weapons_by_soldiers[soldier["name"]]
                            pos = (x+soldier_size[0]//2-self.weapons_images[weapon_name][str(soldier["level"])].get_width()//2,y+soldier_size[1]//2-self.weapons_images[weapon_name][str(soldier["level"])].get_height()//2)
                            weapon_dict = {
                                "name":weapon_name,
                                "pos":pos,
                                "angle":soldier_angle,
                                "attack build id":soldier["attacking build id"],
                                "shooting soldier id":soldier_id,
                                "level":str(soldier["level"])
                            }
                            self.weapons_in_air[weapon_id] = weapon_dict

                            soldier["shoot time"] = time.time() + army.army_soldiers_shoot_time_delay[soldier["name"]]
                            self.attacking_soldiers[soldier_id] = soldier
            elif soldier["name"] == "bomb" or soldier["name"] == "missile": # bomb=>{'name': 'bomb', 'level': 1, 'pos': (429, 265), 'shoot at': (446, 493)}
                x,y = soldier["pos"]
                y += soldier["speed"]
                soldier["speed"] += army.army_soldiers_acceleration[soldier["name"]] # acceleration
                soldier["pos"] = (x,y)
                aimed_pos = soldier["shoot at"]
                soldier_size = army.army_images_sizes[soldier["name"]]
                aimed_pos_rect = pygame.Rect(aimed_pos[0]-soldier_size[0]//2,aimed_pos[1]-soldier_size[1]//2,int(soldier_size[0]*1.5),int(soldier_size[1]*1.5))
                soldier_rect = pygame.Rect(x,y,soldier_size[0],soldier_size[1])
                
                
                if soldier_rect.colliderect(aimed_pos_rect):
                    for build_id in self.base_buildings:
                        building = self.base_buildings[build_id]
                        pos = building["pos"]
                        take_down_damage = check_point_in_circle(x,y,soldier_size[1],pos[0],pos[1])
                        if take_down_damage == False:
                            take_down_damage = check_point_in_circle(x,y+soldier_size[1],soldier_size[1],pos[0],pos[1])
                            
                        if take_down_damage == False:
                            build_size = buildings.buildings_sizes[building["building name"]]
                            take_down_damage = check_point_in_circle(x,y,soldier_size[1],pos[0]+build_size[0],pos[1])
                            if take_down_damage == False:
                                take_down_damage = check_point_in_circle(x,y,soldier_size[1],pos[0],pos[1]+build_size[1])
                                if take_down_damage == False:
                                    take_down_damage = check_point_in_circle(x,y,soldier_size[1],pos[0]+build_size[0],pos[1]+build_size[1])
                        if take_down_damage == False: # check if a less precise way
                            build_size = buildings.buildings_sizes[building["building name"]]
                            build_rect = pygame.Rect(pos[0],pos[1],buildings.buildings_sizes[building["building name"]][0],buildings.buildings_sizes[building["building name"]][1])
                            if soldier_rect.colliderect(build_rect):
                                take_down_damage = True
                        if take_down_damage == True:
                            building["condition"] = "under attack"
                            building["health"] -= self.weapons_damage[soldier["name"]][str(soldier["level"])]
                            if building["health"] <= 0:
                                building["condition"] = "destroyed"
                    explode_id = "1"
                    if self.explosions != {}:
                        explode_id = str(int(list(self.explosions)[-1])+1)
                    if soldier["name"] == "missile":
                        y += army.army_images_sizes[soldier["name"]][1] - self.explosion_frames["1"].get_height()//3
                    self.explosions[explode_id] = {"pos":(x,y),"frame":1,"change frame time":time.time()+self.change_explosion_frame_time} # id:{pos:pos,frame:frame,change frame time:time}
                    to_pop_ids.append(soldier_id)
        for soldier_id in to_pop_ids:
            self.attacking_soldiers.pop(soldier_id)

    def draw_and_handle_explosion(self):
        to_pop_ids = []
        for explode_id in self.explosions:
            explosion = self.explosions[explode_id]
            x,y = explosion["pos"]
            frame = explosion["frame"]
            window.blit(self.explosion_frames[str(frame)],(x,y))
            
            change_time = explosion["change frame time"]
            if time.time() >= change_time:
                frame += 1
                if frame > int(list(self.explosion_frames)[-1]):
                    to_pop_ids.append(explode_id)
                explosion["frame"] += 1
                explosion["change frame time"] = time.time() + self.change_explosion_frame_time
        for explode_id in to_pop_ids:
            self.explosions.pop(explode_id)
    
    def draw_weapons_in_air(self):
        for weapon_id in self.weapons_in_air:
            weapon = self.weapons_in_air[weapon_id]
            name = weapon["name"]
            x,y = weapon["pos"]
            angle = weapon["angle"]
            image = pygame.transform.rotate(self.weapons_images[name][str(weapon["level"])],angle)
            window.blit(image, (x,y))
    def move_weapons_in_air(self):
        to_pop_ids = []
        for weapon_id in self.weapons_in_air:
            # weapon varible => {'name': 'lazer', 'pos': (813.2520346938929, 626.4730843851877), 'angle': 454.5734058567937, 'attack build id': '14'}
            weapon = self.weapons_in_air[weapon_id]
            x,y = weapon["pos"]
            angle = weapon["angle"]
            speed = self.weapons_speed[weapon["name"]]
            
            if not weapon["shooting soldier id"] in self.attacking_soldiers: # can cause when two bullets hit at the same time
                continue
            shooting_soldier_angle = self.attacking_soldiers[weapon["shooting soldier id"]]["going angle"]
            if shooting_soldier_angle - angle > 10:
                angle = shooting_soldier_angle
                weapon["angle"] = angle

            try:
                attack_build_id = weapon["attack build id"]
                attack_build_pos = self.base_buildings[attack_build_id]["pos"]
                new_x,new_y = self.move_by_angle_and_speed((x,y),speed,angle)
                weapon["pos"] = (new_x,new_y)

                attack_build_size = buildings.buildings_sizes[self.base_buildings[attack_build_id]["building name"]]
                build_rect = pygame.Rect(attack_build_pos[0],attack_build_pos[1],attack_build_size[0],attack_build_size[1])
                weapon_rect = pygame.Rect(new_x,new_y,self.weapons_images[weapon["name"]][weapon["level"]].get_width(),self.weapons_images[weapon["name"]][weapon["level"]].get_height()) # the top left

                weapon["pos"] = (new_x,new_y)
                self.weapons_in_air[weapon_id] = weapon

                if build_rect.colliderect(weapon_rect):
                    self.base_buildings[attack_build_id]["condition"] = "under attack"
                    self.base_buildings[attack_build_id]["health"] -= self.weapons_damage[weapon["name"]][str(self.attacking_soldiers[weapon["shooting soldier id"]]["level"])]
                    if self.base_buildings[attack_build_id]["health"] <= 0:
                        self.base_buildings[attack_build_id]["condition"] = "destroyed"
                    to_pop_ids.append(weapon_id)
            except KeyError: # in case the remove bullet part of the destroy buildings function didn't work
                self.weapons_in_air.pop(weapon_id)
                break
        
        for weapon_id in to_pop_ids:
            self.weapons_in_air.pop(weapon_id)
    def draw_buildings_guns_bullets_in_air(self):
        for bullet_id in self.buildings_guns_weapons_in_air:
            bullet = self.buildings_guns_weapons_in_air[bullet_id]
            name = bullet["name"]
            x,y = bullet["pos"]
            angle = bullet["angle"]
            if angle != None:
                image = pygame.transform.rotate(self.buildings_guns_weapons_images[name][str(bullet["level"])],angle)
                window.blit(image, (x,y))
    def move_buildings_guns_bullets_in_air(self):
        to_pop_ids = []
        for bullet_id in self.buildings_guns_weapons_in_air:
            bullet = self.buildings_guns_weapons_in_air[bullet_id]
            # bullet => {'name': 'lazer', 'pos': (1476., 1137.), 'level': '1', 'angle': 613., 'attack soldier pos': (951., 900.), 'iteration': 5, 'damage': 20}
            name = bullet["name"]
            x,y = bullet["pos"]
            angle = bullet["angle"]
            speed = self.buildings_guns_weapons_speed[name]
            if bullet["iteration"] < 5:
                soldier_pos = bullet["attack soldier pos"]
                angle = self.get_angle_between_two_points((x,y),soldier_pos)
                bullet["angle"] = angle
                bullet["iteration"] += 1
            new_x,new_y = self.move_by_angle_and_speed((x,y),speed,angle)
            bullet["pos"] = (new_x,new_y)

            soldiers_to_pop_ids = []
            for soldier_id in self.attacking_soldiers:
                # soldier => {'name': 'killer drone', 'level': 2, 'pos': (929, 716), 'attacking build id': '3', 'going angle': 417, 'shoot time': None,health:110}
                soldier = self.attacking_soldiers[soldier_id]
                soldier_name = soldier["name"]
                pos = soldier["pos"]
                soldier_rect = pygame.Rect(pos[0],pos[1],army.army_images_sizes[soldier_name][0],army.army_images_sizes[soldier_name][1])
                if soldier_rect.collidepoint(x,y):
                    damage = self.buildings_guns_weapons_damage[bullet["name"]][bullet["level"]]
                    soldier["health"] -= damage
                    if soldier["health"] <= 0:
                        soldiers_to_pop_ids.append(soldier_id)
                    to_pop_ids.append(bullet_id)
            for soldier_id in soldiers_to_pop_ids:
                try:
                    self.attacking_soldiers.pop(soldier_id)
                except KeyError:
                    pass
        for bullet_id in to_pop_ids:
            try:
                self.buildings_guns_weapons_in_air.pop(bullet_id)
            except KeyError:
                pass

    def check_for_destroyed_buildings(self):
        destroyed_buildings_ids = []
        for building_id in self.base_buildings:
            building = self.base_buildings[building_id]
            if building["condition"] == "destroyed":
                to_pop_weapon_ids = []
                for weapon_id in self.weapons_in_air:
                    """base weapon dict
                    weapon_dict = {
                        "name":weapon_name,
                        "pos":pos,
                        "angle":soldier_angle,
                        "attack build id":soldier["attacking build id"],
                        "shooting soldier id":soldier_id
                    }"""
                    weapon = self.weapons_in_air[weapon_id]
                    if weapon["attack build id"] == weapon_id:
                        to_pop_weapon_ids.append(weapon_id)
                for weapon_id in to_pop_weapon_ids:
                    self.weapons_in_air.pop(weapon_id)
                for soldier_id in self.attacking_soldiers:
                    """base soldier dict
                    soldier_dict = {
                        "name":self.on_soldier_card,
                        "level":self.on_soldier_card_level,
                        "pos": (x-army.army_images_sizes[soldier["name"]][0]//2,y-army.army_images_sizes[soldier["name"]][1]//2),
                        "attacking build id":None,
                        "going angle":None,
                        "shoot time":None, # starts in None (shoots at the second the user places it)
                    }"""
                    soldier = self.attacking_soldiers[soldier_id]
                    if soldier["name"] != "bomb" and soldier["name"] != "missile":
                        if soldier["attacking build id"] == building_id:
                            soldier["attacking build id"] = None
                            soldier["going angle"] = None
                destroyed_buildings_ids.append(building_id)
        for build_id in destroyed_buildings_ids:
            building = self.base_buildings[build_id].copy()
            self.base_buildings.pop(build_id)

            # handle the destroyed buildings dict
            #self.destroyed_buildings = {} # id:{"building name":name,"pos":[x,y],"destroyed image":image}
            building.pop("level")
            building.pop("frame")
            img = self.destroyed_building_animation[str(random.randint(1,len(self.destroyed_building_animation)-1))]
            building["destroyed image"] = pygame.transform.smoothscale(img,buildings.buildings_sizes[building["building name"]])
            self.destroyed_buildings[build_id] = building

        if destroyed_buildings_ids != []:
            if self.base_buildings == {}:
                print("destroyed base!")
                self.show_done_attacking_screen = True
    def draw_destroyed_buildings(self):
        for build_id in self.destroyed_buildings:
            building = self.destroyed_buildings[build_id]
            x,y = building["pos"]
            img = building["destroyed image"]
            window.blit(img,(x,y))

    def handle_timer(self):
        if self.start_attacking == True and self.active_attack_time == None:
            self.active_attack_time = time.time() + self.attack_time
        if self.active_attack_time != None and not self.show_done_attacking_screen == True:
            if time.time() >= self.active_attack_time:
                self.show_done_attacking_screen = True
    def draw_timer(self):
        if self.active_attack_time != None:
            time_left = self.active_attack_time - time.time()
            seconds = int(time_left % 60)
            minutes = int(time_left // 60)
            if seconds < 10:
                seconds = "0"+str(seconds)
            to_show = str(minutes)+":"+str(seconds)
            
            color = (255,255,255)
            if minutes == 0 and int(seconds) < 10:
                color = (255,0,0)
            window.blit(bigger_font.render(to_show,True,(0,0,0)),(screen_x//2-bigger_font.size(to_show)[0]//2-1.5,10-1.5))
            window.blit(bigger_font.render(to_show,True,color),(screen_x//2-bigger_font.size(to_show)[0]//2,10))

    def draw_attack_reward(self): # in middle attack
        iron = self.money_for_attack["iron"]
        gold = self.money_for_attack["gold"]
        diamonds = self.money_for_attack["diamonds"]

        window.blit(user.trophy,user.trophy_pos)
        window.blit(bigger_font.render(str(self.trophies_for_attack),True,(255,255,255)),(user.trophy_pos[0]+user.trophy.get_width()+5,user.trophy_pos[1]+user.trophy.get_height()//2-bigger_font.size("0")[1]//2))

        y = user.gold_coin_pos[1]+2
        window.blit(font.render("Loot:",True,(255,255,255)),(user.gold_coin_pos[0]+user.gold_coin.get_width()+10,10))
        window.blit(user.gold_coin, user.gold_coin_pos)
        pygame.draw.rect(window, user.gold_color, [user.gold_coin_pos[0]+user.gold_coin.get_width()+10,y, 200 ,22])
        pygame.draw.rect(window, (0,0,0), [user.gold_coin_pos[0]+user.gold_coin.get_width()+10,y,200,22],2)
        window.blit(font.render(str(gold),True,(0,0,0)), (user.gold_coin_pos[0]+user.gold_coin.get_width()+13,y+1))
        window.blit(font.render(str(gold),True,(0,0,0)), (user.gold_coin_pos[0]+user.gold_coin.get_width()+15,y+3))
        window.blit(font.render(str(gold),True,user.gold_color), (user.gold_coin_pos[0]+user.gold_coin.get_width()+14,y+2)) # 2 shadow for it to be all around the letter
        
        window.blit(user.iron_img, user.iron_pos)
        pygame.draw.rect(window, user.iron_color, [user.iron_pos[0]+user.iron_img.get_width()+10,y+user.gold_coin.get_height()+5, 200 ,22])
        pygame.draw.rect(window, (0,0,0), [user.iron_pos[0]+user.iron_img.get_width()+10,y+user.gold_coin.get_height()+5,200,22],2)
        window.blit(font.render(str(iron),True,(0,0,0)), (user.iron_pos[0]+user.iron_img.get_width()+13,y+1+user.gold_coin.get_height()+5))
        window.blit(font.render(str(iron),True,(0,0,0)), (user.iron_pos[0]+user.iron_img.get_width()+15,y+3+user.gold_coin.get_height()+5))
        window.blit(font.render(str(iron),True,user.iron_color), (user.iron_pos[0]+user.iron_img.get_width()+14,y+2+user.gold_coin.get_height()+5)) # 2 shadow for it to be all around the letter
        
        window.blit(user.diamond_img, user.diamond_pos)
        pygame.draw.rect(window, user.diamond_color, [user.diamond_pos[0]+user.diamond_img.get_width()+10,y+user.gold_coin.get_height()+5+user.iron_img.get_height()+10, 200 ,22])
        pygame.draw.rect(window, (0,0,0), [user.diamond_pos[0]+user.diamond_img.get_width()+10,y+user.gold_coin.get_height()+5+user.iron_img.get_height()+10,200,22],2)
        window.blit(font.render(str(diamonds),True,(0,0,0)), (user.diamond_pos[0]+user.diamond_img.get_width()+13,y+1+user.gold_coin.get_height()+5+user.iron_img.get_height()+10))
        window.blit(font.render(str(diamonds),True,(0,0,0)), (user.diamond_pos[0]+user.diamond_img.get_width()+15,y+3+user.gold_coin.get_height()+5+user.iron_img.get_height()+10))
        window.blit(font.render(str(diamonds),True,user.diamond_color), (user.diamond_pos[0]+user.diamond_img.get_width()+14,y+2+user.gold_coin.get_height()+5+user.iron_img.get_height()+10)) # 2 shadow for it to be all around the letter
    def draw_done_attacking_screen(self):
        n_buildings_left = len(self.base_buildings)
        one_percent = self.total_num_of_buildings / 100
        left_percent = int(n_buildings_left * one_percent*100)
        destroyed_percent = int(100-left_percent)
        if self.base_buildings == {}:
            destroyed_percent = 100
        elif len(self.base_buildings) == self.total_num_of_buildings:
            destroyed_percent = 0

        width,height = self.done_attack_screen_width,self.done_attack_screen_height
        x,y = self.done_attack_screen_x,self.done_attack_screen_y

        draw_transparent_square(window,(width,height),170,(0,0,0),(x,y))
        window.blit(bigger_font.render("Total Damage",True,(255,255,255)),(x+width/2-bigger_font.size("Total Damage")[0]//2,y+10))
        window.blit(bigger_font.render(str(destroyed_percent)+"%",True,(255,255,255)),(x+width/2-bigger_font.size(str(destroyed_percent)+"%")[0]//2,y+10+bigger_font.size("D")[1]+5))

        # the ifs are in case of a bug
        earned_iron = 0
        if self.money_for_attack["iron"] != None:
            earned_iron = int(self.money_for_attack["iron"] * (destroyed_percent/100))
        earned_gold = 0
        if self.money_for_attack["gold"] != None:
            earned_gold = int(self.money_for_attack["gold"] * (destroyed_percent/100))
        earned_diamonds = 0
        if self.money_for_attack["diamonds"] != None:
            earned_diamonds = int(self.money_for_attack["diamonds"] * (destroyed_percent/100))

        y += bigger_font.size("D")[1]*4


        trophy_x = x + 10
        window.blit(user.trophy,(trophy_x,y))
        earned_trophies = 0
        if destroyed_percent == 0:
            earned_trophies = -30
        elif destroyed_percent < 40:
            earned_trophies = -int(left_percent/100*self.trophies_for_attack)
        elif destroyed_percent == 40:
            earned_trophies = 0
        else: # destroyed_percent > 40
            earned_trophies = int(destroyed_percent/100*self.trophies_for_attack)
        window.blit(bigger_font.render(str(earned_trophies),True,(255,255,255)),(x+user.trophy.get_width()+15,y+user.trophy.get_height()//2-bigger_font.size("0")[1]//2))
        y += bigger_font.size("D")[1]*2

        money_x = x +10
        # gold
        window.blit(user.gold_coin,(money_x,y))
        window.blit(bigger_font.render(str(earned_gold)+"/"+str(self.money_for_attack["gold"]),True,user.gold_color),(money_x+user.gold_coin.get_width()+5,y+user.gold_coin.get_height()//2-bigger_font.size("0")[1]//2))
        y += user.gold_coin.get_height()*1.4
        # iron
        window.blit(user.iron_img,(money_x,y))
        window.blit(bigger_font.render(str(earned_iron)+"/"+str(self.money_for_attack["iron"]),True,user.iron_color),(money_x+user.iron_img.get_width()+5,y+user.iron_img.get_height()//2-bigger_font.size("0")[1]//2))
        y += user.iron_img.get_height()*1.4
        # diamonds
        window.blit(user.diamond_img,(money_x,y))
        window.blit(bigger_font.render(str(earned_diamonds)+"/"+str(self.money_for_attack["diamonds"]),True,user.diamond_color),(money_x+user.diamond_img.get_width()+5,y+user.diamond_img.get_height()//2-bigger_font.size("0")[1]//2))
        y += user.diamond_img.get_height()*1.4

        mouse = pygame.mouse.get_pos()
        if self.done_attack_backToBase_button_rect.collidepoint(mouse):
            window.blit(self.done_attack_backToBase_button_mouse_on,self.done_attack_backToBase_button_pos)
        else:
            window.blit(self.done_attack_backToBase_button,self.done_attack_backToBase_button_pos)
    def handle_mouse_in_done_attacking_screen(self):
        mouse_press = pygame.mouse.get_pressed()
        mouse = pygame.mouse.get_pos()
        if mouse_press[0] == True:
            if self.done_attack_backToBase_button_rect.collidepoint(mouse): # same as colliderect but gets a point(checks with the rect of 1x1)
                n_buildings_left = len(self.base_buildings)
                one_percent = self.total_num_of_buildings / 100
                left_percent = int(n_buildings_left * one_percent*100)
                destroyed_percent = int(100-left_percent)
                if self.base_buildings == {}:
                    destroyed_percent = 100
                elif len(self.base_buildings) == self.total_num_of_buildings:
                    destroyed_percent = 0
                earned_iron = 0
                if self.money_for_attack["iron"] != None:
                    earned_iron = int(self.money_for_attack["iron"] * (destroyed_percent/100))
                earned_gold = 0
                if self.money_for_attack["gold"] != None:
                    earned_gold = int(self.money_for_attack["gold"] * (destroyed_percent/100))
                earned_diamonds = 0
                if self.money_for_attack["diamonds"] != None:
                    earned_diamonds = int(self.money_for_attack["diamonds"] * (destroyed_percent/100))

                user.gold += earned_gold
                user.iron += earned_iron
                user.diamonds += earned_diamonds
                earned_trophies = 0
                if destroyed_percent == 0:
                    earned_trophies = -30
                elif destroyed_percent < 40:
                    earned_trophies = -int(left_percent/100*self.trophies_for_attack)
                elif destroyed_percent == 40:
                    earned_trophies = 0
                else: # destroyed_percent > 40
                    earned_trophies = int(destroyed_percent/100*self.trophies_for_attack)
                user.num_of_trophies += earned_trophies
                if user.num_of_trophies < 0: # if he lose at the first time
                    user.num_of_trophies = 0
                save_user_trophies(user.num_of_trophies)

                if user.gold > user.max_gold:
                    user.gold = user.max_gold
                if user.iron > user.max_iron:
                    user.iron = user.max_iron
                if user.diamonds > user.max_diamonds:
                    user.diamonds = user.max_diamonds
                
                self.reset_class()
                self.attacking = False
                self.show_done_attacking_screen = False

    # reset the things that needs to be in their default each time
    def reset_class(self):
        self.on_soldier_card = None
        self.on_soldier_card_level = None
        self.start_attacking = False
        self.total_num_of_buildings = 0
        self.money_for_attack = {
            "iron":None,
            "gold":None,
            "diamonds":None
        }
        self.trophies_for_attack = None
        self.active_attack_time = None
attack = create_attack()

loading_screen(phase=3)


class create_reset_handler():
    def reset_buildings(self):
        buildings.buildings = {
                "1": {
                    "building name": "townhall",
                    "pos": [
                        490,
                        610
                    ],
                    "level": "1",
                    "frame": "1"
                }
            } # the townhall is the first building
        buildings.upgrade_building = None
    def reset_cash_methods(self):
        """
        max gold without storage: 1000
        max iron without storage: 1000
        max diamonds without storage: 250
        
        all of the cash types at the beginning are max(gold:1000,iron:1000,diamonds:250)"""
        user.max_gold = 1000
        user.gold = user.max_gold
        user.max_iron = 1000
        user.iron = user.max_iron
        user.max_diamonds = 250
        user.diamonds = user.max_diamonds
    def reset_army(self):
        """deletes the army he can attacks with and reset the capacity,max capacity to 0"""
        army.capacity = 0
        army.max_capacity = 0
        army.soldiers_in_camp = {}
        army.soldier_in_upgrade = None
    def reset_trophies(self):
        user.num_of_trophies = 0
    def reset_game(self): # call this function in the in game menu
        """reset everything except the profile"""
        self.reset_buildings()
        self.reset_army()
        self.reset_cash_methods()
        self.reset_trophies()

        save_all() # to update all of the changes
reset_handler = create_reset_handler()

class create_how_to_play_screen():
    def __init__(self):
        self.in_how_to_play_screen = False

        self.win_size = upgrade_building_screen.min_window_size
        self.win_pos = (screen_x//2-self.win_size[0]//2,screen_y//2-self.win_size[1]//2)

        self.movement_keys_size = (100,int(100*0.65)) # 490x322 1:0.65
        self.wasd_keys = pygame.transform.smoothscale(pygame.image.load(folder+"/keyboard keys/wasd.png"),self.movement_keys_size)
        self.arrow_keys = pygame.transform.smoothscale(pygame.image.load(folder+"/keyboard keys/arrows.png"),self.movement_keys_size)

        self.esc_button_size = (bigger_font.size("X")[1]+2,bigger_font.size("X")[1]+2)
        self.esc_button_pos = (screen_x-self.esc_button_size[0]-10,10)
        self.esc_button_rect = pygame.Rect(self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1])
    def draw_screen(self):
        window.blit(upgrade_building_screen.min_window_image,self.win_pos)

        start_x = self.win_pos[0]+font.size("p")[0]*1.5
        start_y = self.win_pos[1]+font.size("p")[1]*1.5
        window.blit(bigger_font.render("How To Play?",True,(0,0,0)), (start_x+self.win_size[0]//2-bigger_font.size("How To Play?")[0]//2,start_y+bigger_font.size("H")[1]*0.5))
        
        # esc button (right up)
        pygame.draw.rect(window, (200,0,0),[self.esc_button_pos[0],self.esc_button_pos[1],self.esc_button_size[0],self.esc_button_size[1]])
        pygame.draw.rect(window, (255,64,64),[self.esc_button_pos[0]-2,self.esc_button_pos[1]-2,self.esc_button_size[0]+3,self.esc_button_size[1]+3],2)
        window.blit(bigger_font.render("X",True,(255,255,255)), (self.esc_button_pos[0]+self.esc_button_size[0]//2-bigger_font.size("X")[0]//2,self.esc_button_pos[1]+self.esc_button_size[1]//2-bigger_font.size("X")[1]//2))
        
        # movement in base
        movement_text_pos = (start_x+10,start_y+bigger_font.size("H")[1]*2)
        window.blit(font.render("Moving with:",True,(16,78,139)),movement_text_pos)
        window.blit(self.wasd_keys,(movement_text_pos[0],movement_text_pos[1]+font.size("M")[1]*1.5))
        window.blit(self.arrow_keys,(movement_text_pos[0]+5+self.movement_keys_size[0],movement_text_pos[1]+font.size("M")[1]*1.5))

        # attack
        attack_text_pos = [start_x+10,start_y+bigger_font.size("H")[1]*2+self.movement_keys_size[1]*2]
        window.blit(font.render("How to attack:",True,(16,78,139)),(attack_text_pos))
        attack_text_pos[1] += font.size("H")[1]*1.4
        window.blit(font.render("1. Buy the barracks, army camp",True,(16,78,139)),(attack_text_pos))
        attack_text_pos[1] += font.size("H")[1]*1.25
        window.blit(font.render("2. Press on the attack button",True,(16,78,139)),(attack_text_pos))
        attack_text_pos[1] += font.size("H")[1]*1.25
        window.blit(font.render("3. Choose a soldier to place",True,(16,78,139)),(attack_text_pos))
        attack_text_pos[1] += font.size("H")[1]*1.25
        window.blit(font.render("4. Place the soldier on the map",True,(16,78,139)),(attack_text_pos))
        attack_text_pos[1] += font.size("H")[1]*1.25
        window.blit(font.render("5. And that's it, you can attack now",True,(16,78,139)),(attack_text_pos))
    def handle_mouse(self):
        pressed_mouse = pygame.mouse.get_pressed()
        if pressed_mouse[0] == True:
            mouse = pygame.mouse.get_pos()
            if self.esc_button_rect.collidepoint(mouse):
                self.in_how_to_play_screen = False
    def handle_keyboard(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.in_how_to_play_screen = False
            in_game_menu.in_in_game_menu = True
how_to_play_screen = create_how_to_play_screen()

class create_in_game_menu():
    def __init__(self):
        self.in_in_game_menu = False

        self.reset_screen_size = (400,600)
        self.reset_screen_pos = (screen_x//2-self.reset_screen_size[0]//2,screen_y//2-self.reset_screen_size[1]//2)

        self.last_frame_mouse = None # to check if the mouse is let go(pressing and then when he let go the mouse it will be a press)

        self.reset_game_button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/reset game button.png"),(120,int(120*0.5)))
        self.reset_game_button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/reset game button mouse on.png"),self.reset_game_button.get_size())
        self.reset_game_btn_size = self.reset_game_button.get_size()
        self.reset_game_btn_pos = (screen_x//2-self.reset_game_btn_size[0]//2,self.reset_screen_pos[1]+(self.reset_screen_size[1]//8))
        self.reset_game_btn_rect = pygame.Rect(self.reset_game_btn_pos[0],self.reset_game_btn_pos[1],self.reset_game_btn_size[0],self.reset_game_btn_size[1])

        self.how_to_play_button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/how to play button.png"),(120,int(120*0.53))) # 564x303 1:0.53
        self.how_to_play_button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/how to play button mouse on.png"),self.how_to_play_button.get_size())
        self.how_to_play_btn_size = self.how_to_play_button.get_size()
        self.how_to_play_btn_pos = (screen_x//2-self.how_to_play_btn_size[0]//2,self.reset_screen_pos[1]+(self.reset_screen_size[1]//8*2))
        self.how_to_play_btn_rect = pygame.Rect(self.how_to_play_btn_pos[0],self.how_to_play_btn_pos[1],self.how_to_play_btn_size[0],self.how_to_play_btn_size[1])
        
        self.more_games_button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/more games button.png"),(120,int(120*0.5))) # 600x300 1:0.5
        self.more_games_button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/more games button mouse on.png"),(120,int(120*0.5))) # 600x300 1:0.5
        self.more_games_btn_pos = (screen_x//2-self.more_games_button.get_width()//2,self.reset_screen_pos[1]+(self.reset_screen_size[1]//8*3))
        self.more_games_btn_rect = pygame.Rect(self.more_games_btn_pos[0],self.more_games_btn_pos[1],self.more_games_button.get_width(),self.more_games_button.get_height())

        self.exit_button = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/exit button.png"),(120,int(120*0.5))) # 666x333 1:0.5
        self.exit_button_mouse_on = pygame.transform.smoothscale(pygame.image.load(folder+"/game buttons/exit button mouse on.png"),self.exit_button.get_size()) # 666x333 1:0.5
        self.exit_game_btn_pos = (screen_x//2-self.exit_button.get_width()//2,self.reset_screen_pos[1]+self.reset_screen_size[1]-(self.reset_screen_size[1]//8)*1.5)
        self.exit_game_btn_rect = pygame.Rect(self.exit_game_btn_pos[0],self.exit_game_btn_pos[1],self.exit_button.get_width(),self.exit_button.get_height())
    def draw_buttons(self):
        # background
        pygame.draw.rect(window,(255,255,255),[self.reset_screen_pos[0],self.reset_screen_pos[1],self.reset_screen_size[0],self.reset_screen_size[1]],2)
        draw_transparent_square(window,self.reset_screen_size,200,(83,134,139),self.reset_screen_pos)
        window.blit(huge_font.render("Game Menu",True,(255,255,255)),(self.reset_screen_pos[0]+self.reset_screen_size[0]//2-huge_font.size("Game Menu")[0]//2,self.reset_screen_pos[1]+10))

        mouse = pygame.mouse.get_pos()
        # buttons
        # reset game button
        if self.reset_game_btn_rect.collidepoint(mouse):
            window.blit(self.reset_game_button_mouse_on, self.reset_game_btn_pos)
        else:
            window.blit(self.reset_game_button, self.reset_game_btn_pos)
        # how to play button
        if self.how_to_play_btn_rect.collidepoint(mouse):
            window.blit(self.how_to_play_button_mouse_on, self.how_to_play_btn_pos)
        else:
            window.blit(self.how_to_play_button, self.how_to_play_btn_pos)
        # exit button
        if self.exit_game_btn_rect.collidepoint(mouse):
            window.blit(self.exit_button_mouse_on, self.exit_game_btn_pos)
        else:
            window.blit(self.exit_button, self.exit_game_btn_pos)
        # more games button
        if self.more_games_btn_rect.collidepoint(mouse):
            window.blit(self.more_games_button_mouse_on, self.more_games_btn_pos)
        else:
            window.blit(self.more_games_button, self.more_games_btn_pos)
    def handle_mouse_in_in_menu_screen(self):
        if self.last_frame_mouse == None:
            self.last_frame_mouse = pygame.mouse.get_pressed()
        pressed_mouse = pygame.mouse.get_pressed()
        if self.last_frame_mouse[0] == True and pressed_mouse[0] == False: # means he let go the button
            mouse = pygame.mouse.get_pos()
            if self.reset_game_btn_rect.collidepoint(mouse):
                reset_handler.reset_game()
                show_notification("game reset","the game has been reset but needed to be open again")
                exit()
            elif self.how_to_play_btn_rect.collidepoint(mouse):
                self.in_in_game_menu = False
                how_to_play_screen.in_how_to_play_screen = True
            elif self.exit_game_btn_rect.collidepoint(mouse):
                save_all()
                pygame.quit()
                exit() # stops the program
            elif self.more_games_btn_rect.collidepoint(mouse):
                webbrowser.open_new_tab("https://yair-mizrachi.itch.io/")
        self.last_frame_mouse = pressed_mouse
in_game_menu = create_in_game_menu()

def save_all():
    save_buildings(buildings.buildings)
    save_in_upgrade_buildings(buildings.upgrade_building)
    user.save_cash_methods()
    user_profile.save_profile()
    save_user_trophies(user.num_of_trophies)
    tiles_start_pos = open("user data/tiles start pos.txt","w")
    tiles_start_pos.write(str(base_bg.start_pos[0])+","+str(base_bg.start_pos[1]))
    tiles_start_pos.close()
    army.save_army()

def main():
    clock = pygame.time.Clock()
    game_on = True
    pygame.mouse.set_pos([screen_x//2,screen_y//2]) # change mouse position
    cursor_image = pygame.transform.smoothscale(pygame.image.load(folder+"/cursor.png").convert_alpha(), (30,30))

    in_main_screen = True
    while game_on:
        clock.tick(30) # optimize fps for pygame

        mouse = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        pressed_mouse = pygame.mouse.get_pressed() # left,center,right

        if not attack.attacking:
            # things that can change before the draw
            buildings.handle_in_upgrade_building()

            base_bg.draw_tiles()
            buildings.draw_buildings(draw_moving_building = False,check_mouse_press = False)
            movement.draw_arrows()
            the_lab_screen.handle_in_upgrade_soldier()

        in_main_screen = False
        # if the main screen
        if shop.in_shop == False and barracks_screen.in_barracks_screen == False and upgrade_building_screen.in_building_upgrade_screen == False and attack.attacking == False and in_game_menu.in_in_game_menu == False and how_to_play_screen.in_how_to_play_screen == False and the_lab_screen.in_the_lab_screen == False:
            in_main_screen = True
            # if the user didnt press on anything and no building is active
            if buildings.in_building_info_screen == False:
                if buildings.moving_buildings == {} and buildings.on_building == None:
                    if pressed_mouse[0] == True: # pressed left mouse button
                        movement.handle_mouse(mouse)
                        buildings.handle_mouse()
                    if keys != (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0):
                        movement.handle_keyboard_arrows(keys)
                else: # if a building is moving/the user is on it
                    buildings.move_moving_building()
                    if pressed_mouse[0] == True:
                        buildings.handle_mouse()
                
                # draw the things that on the top of everything
                user.draw_howmany_builders_left()
                user.draw_payment_methods()
                user.draw_trophies_in_base()
                shop.draw_button()
                shop.press_button_check()
                attack.draw_button_in_normal()
                attack.press_button_check_in_normal()
            else:
                user.draw_howmany_builders_left()
                user.draw_payment_methods()
                shop.draw_button()
                draw_transparent_square(window,(screen_x,screen_y),200,(102,177,255),(0,0))
                # the info
                buildings.draw_building_info_screen()
                buildings.handle_mouse_in_building_info_screen()
        elif in_game_menu.in_in_game_menu == True:
            buildings.draw_buildings()
            user.draw_howmany_builders_left()
            user.draw_payment_methods()
            user.draw_trophies_in_base()

            draw_transparent_square(window,(screen_x,screen_y),200,(0,0,0),(0,0))
            in_game_menu.draw_buttons()
            in_game_menu.handle_mouse_in_in_menu_screen()
        elif how_to_play_screen.in_how_to_play_screen == True:
            buildings.draw_buildings()
            user.draw_howmany_builders_left()
            user.draw_payment_methods()
            user.draw_trophies_in_base()

            draw_transparent_square(window,(screen_x,screen_y),200,(0,0,0),(0,0))
            how_to_play_screen.draw_screen()
            how_to_play_screen.handle_mouse()
            how_to_play_screen.handle_keyboard()
        # in upgrade building screen      (show what will change)
        elif upgrade_building_screen.in_building_upgrade_screen == True:
            user.draw_howmany_builders_left()
            user.draw_payment_methods()
            draw_transparent_square(window,(screen_x,screen_y),150,(102,177,255),(0,0))
            upgrade_building_screen.draw_screen()
        # in shop
        elif shop.in_shop == True: # in shop
            draw_transparent_square(window,(screen_x,screen_y),200,(102,177,255),(0,0))
            shop.draw_shop()
            shop.press_esc_button_check()
            shop.handle_mouse_in_shop() # buy things
            shop.handle_keyboard_in_shop()

            # draw the things that on the top of everything
            user.draw_howmany_builders_left()
            user.draw_payment_methods()
        # in barracks screen(training soldiers)
        elif barracks_screen.in_barracks_screen == True: # in barracks screen(train soldiers)
            # draw the things that behind everything
            user.draw_howmany_builders_left()
            user.draw_trophies_in_base()
            user.draw_payment_methods()

            # next line is in the for event loop
            draw_transparent_square(window,(screen_x,screen_y),200,(132,207,255),(0,0))
            user.draw_payment_methods()
            barracks_screen.draw_screen()
        elif the_lab_screen.in_the_lab_screen == True:
            # draw the things that behind everything
            user.draw_howmany_builders_left()
            user.draw_trophies_in_base()
            user.draw_payment_methods()

            # next line is in the for event loop
            draw_transparent_square(window,(screen_x,screen_y),200,(132,207,255),(0,0))
            the_lab_screen.draw_screen()
            the_lab_screen.handle_keyboard()
        elif attack.attacking == True:
            if attack.show_done_attacking_screen == False:
                attack.draw_tiles()
                attack.draw_destroyed_buildings()
                attack.draw_attack_base()
                attack.handle_keyboard()

                attack.handle_soldiers_nav()
                attack.place_soldiers()
                attack.move_soldiers()
                attack.draw_soldiers()
                attack.draw_and_handle_explosion()
                attack.draw_weapons_in_air()
                attack.move_weapons_in_air()
                attack.draw_buildings_guns_bullets_in_air()
                attack.move_buildings_guns_bullets_in_air()
                attack.draw_attack_reward()

                attack.handle_timer()
                attack.draw_timer()

                attack.check_for_destroyed_buildings()
            else: #attack.show_done_attacking_screen == True
                attack.draw_tiles()
                attack.draw_attack_base()

                attack.draw_soldiers()
                attack.draw_weapons_in_air()
                
                draw_transparent_square(window,(screen_x,screen_y),100,(0,0,0),(0,0))
                attack.draw_done_attacking_screen()
                attack.handle_mouse_in_done_attacking_screen()
        
        window.blit(bigger_font.render("fps: " + str(clock.get_fps())[:2],True,(0,0,0)),(screen_x-bigger_font.size("fps: " + str(clock.get_fps())[:2])[0],10))
        fade_red_text.show_text()
        collect_money_effect.draw_screen()


        pygame.mouse.set_visible(False) # hides the mouse
        if pressed_mouse[0] == True:
            pygame.draw.circle(window,(255,255,255),[mouse[0],mouse[1]], 3)
        window.blit(cursor_image, (mouse[0],mouse[1])) # shows the new mouse
        pygame.display.flip() # faster than .update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                buildings.check_on_building_valid_pos()
                save_all()
                pygame.quit()
                exit() # stops the program
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    if shop.in_shop == False and barracks_screen.in_barracks_screen == False and upgrade_building_screen.in_building_upgrade_screen == False and buildings.in_building_info_screen == False and attack.attacking == False and in_game_menu.in_in_game_menu == False:
                        in_game_menu.in_in_game_menu = True
                    elif shop.in_shop == True:
                        # leave the shop
                        shop.in_shop = False
                    elif barracks_screen.in_barracks_screen == True:
                        # leave the barracks screen
                        buildings.army_camp_for_soldiers_info = [] # stores all of the army camps info(the building info)
                        buildings.army_camp_moving_soldiers = [] # [soldier dict,soldier dict]
                        barracks_screen.in_barracks_screen = False
                    elif upgrade_building_screen.in_building_upgrade_screen == True:
                        upgrade_building_screen.in_building_upgrade_screen = False
                    elif buildings.in_building_info_screen == True:
                        buildings.in_building_info_screen = False
                    
                    elif in_game_menu.in_in_game_menu == True:
                        in_game_menu.in_in_game_menu = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if the_lab_screen.in_the_lab_screen == True:
                    the_lab_screen.handle_mouse()
                if in_main_screen == True:
                    buildings.draw_buildings(check_mouse_press = True)
                if barracks_screen.in_barracks_screen == True:
                    barracks_screen.handle_mouse()
                if upgrade_building_screen.in_building_upgrade_screen == True:
                    upgrade_building_screen.handle_mouse()
                if event.button == 4: # scroll up
                    # move left
                    if shop.in_shop == True:
                        shop.in_shop_moving_speed = shop.in_shop_moving_speed*4
                        shop.move("left")
                        shop.in_shop_moving_speed = shop.in_shop_moving_speed_original       
                elif event.button == 5: # scroll down
                    # move right
                    if shop.in_shop == True:
                        shop.in_shop_moving_speed = shop.in_shop_moving_speed*4
                        shop.move("right")
                        shop.in_shop_moving_speed = shop.in_shop_moving_speed_original


main()