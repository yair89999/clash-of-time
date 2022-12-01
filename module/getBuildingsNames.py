import os

folder = "images"
def return_buildings_names():
    # get the names of the folders(every building name)
    buildings = []

    directory = folder+'/buildings'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        building_name = f.split("\\")[-1]
        buildings.append(building_name)
    return buildings
def return_buildings_levels():
    # get the levels of the buildings(every building level)
    levels = []

    directory = folder+'/buildings'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        building_name = f.split("\\")[-1]
        building_levels_num = len(os.listdir(directory+"/"+building_name))
        levels.append(building_levels_num)
    return levels

def return_buildings_guns_names():
    # get the names of the folders(every building name)
    buildings_guns = []

    directory = folder+'/buildings guns'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        building_gun_name = f.split("\\")[-1]
        buildings_guns.append(building_gun_name)
    return buildings_guns
def return_buildings_guns_levels():
    # get the levels of the buildings(every building level)
    levels = []

    directory = folder+'/buildings guns'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        building_gun_name = f.split("\\")[-1]
        building_gun_levels_num = len(os.listdir(directory+"/"+building_gun_name))
        levels.append(building_gun_levels_num)
    return levels


def return_soldiers_names(): # returns the soldiers types
    # get the names of the folders(every building name)
    buildings = []

    directory = folder+'/army'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        building_name = f.split("\\")[-1]
        buildings.append(building_name)
    return buildings

def return_soldiers_levels():
    # get the levels of the buildings(every building level)
    levels = []

    directory = folder+'/army'

    index = 0
    for filename in os.listdir(directory):
        levels.append([])
        f = os.path.join(directory, filename)
        for filename2 in os.listdir(f):
            level = filename2[:-4] # without the .png
            levels[index].append(level)
        index += 1
    return levels


def return_weapons_names():
    # get the names of the folders(every building name)
    weapons = []

    directory = folder+'/army weapons'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        weapon_name = f.split("\\")[-1]
        weapons.append(weapon_name)
    return weapons
def return_weapons_levels():
    # get the levels of the buildings(every building level)
    levels = []

    directory = folder+'/army weapons'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        weapon_name = f.split("\\")[-1]
        weapon_levels_num = len(os.listdir(directory+"/"+weapon_name))
        levels.append(weapon_levels_num)
    return levels

def return_buildings_guns_weapons_names():
    # get the names of the folders(every building name)
    weapons = []

    directory = folder+'/buildings guns weapons'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        weapon_name = f.split("\\")[-1]
        weapons.append(weapon_name)
    return weapons
def return_buildings_guns_weapons_levels():
    # get the levels of the buildings(every building level)
    levels = []

    directory = folder+'/buildings guns weapons'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        weapon_name = f.split("\\")[-1]
        weapon_levels_num = len(os.listdir(directory+"/"+weapon_name))
        levels.append(weapon_levels_num)
    return levels