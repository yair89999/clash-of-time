import json,os

buildings_path = "user data/buildings.json"

def save_buildings(buildings):
    # saves in the json file
    what_to_save = {"buildings":[buildings]}
    with open(buildings_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

def reload_buildings():
    # returns the users dict
    with open(buildings_path) as file:
        data = json.load(file)
        data = data["buildings"][0]
        # in json there is no tuple so changing to tuple
        for id in data:
            data[id]["pos"] = tuple(data[id]["pos"])
        return data


in_upgrade_buildings_path = "user data/in upgrade buildings.json"

def save_in_upgrade_buildings(buildings):
    # saves in the json file
    what_to_save = {"buildings":[buildings]}
    with open(in_upgrade_buildings_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

def reload_in_upgrade_buildings():
    # returns the users dict
    with open(in_upgrade_buildings_path) as file:
        data = json.load(file)
        data = data["buildings"][0]
        if data == {}: data = None
        return data


cash_methods_path = "user data/cash methods.json"

def save_cash_methods(cash_methods):
    # saves in the json file
    what_to_save = {"cash methods":[cash_methods]}
    with open(cash_methods_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

def reload_cash_methods():
    # returns the users dict
    with open(cash_methods_path) as file:
        data = json.load(file)
        data = data["cash methods"][0]
        return data


army_and_capacity_path = "user data/army info.json"

def save_army_and_capacity(army,capacity,soldiers_levels,soldier_in_upgrade):
    # saves in the json file
    capacity = {"capacity":capacity[0],"max capacity":capacity[1]}
    what_to_save = {"capacity":[capacity],"soldiers levels":soldiers_levels,"soldier in upgrade":soldier_in_upgrade,"army":[army]}
    with open(army_and_capacity_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

def reload_army_and_capacity():
    # returns the users dict
    with open(army_and_capacity_path) as file:
        data = json.load(file)
        capacity = data["capacity"]
        soldiers_levels = data["soldiers levels"]
        army = data["army"][0]
        soldier_in_upgrade = data["soldier in upgrade"][0]
        return capacity,army,soldiers_levels,soldier_in_upgrade


buildings_info_path = "user data/buildings info.json"

def get_buildings_info():
    with open(buildings_info_path) as file:
        data = json.load(file)
        info = data["buildings info"][0]
        return info


profile_path = "user data/profile_info.json"

def save_profile(made_profile,profile_info):
    # saves in the json file
    
    what_to_save = {"made profile":made_profile,"profile info":[profile_info]}
    with open(profile_path, "w") as file:
        json.dump(what_to_save, file,  indent=4)

def reload_profile():
    # returns the users dict
    with open(profile_path) as file:
        data = json.load(file)
        did_profile = data["made profile"]
        profile_info = data["profile info"][0]
        return did_profile,profile_info


buildings_costs_path = "user data/buildings_costs.json"

def reload_buildings_costs():
    # returns the users dict
    with open(buildings_costs_path) as file:
        data = json.load(file)["data"][0]
        return data

user_trophies_path = "user data/num of trophies.txt"
def reload_user_trophies():
    file = open(user_trophies_path)
    n_trophies = int(file.read())
    file.close()
    return n_trophies
def save_user_trophies(trophies):
    file = open(user_trophies_path,"w")
    file.write(str(trophies))
    file.close()

army_fixed_info_path = "user data/army fixed info.json"

def reload_army_fixed_info():
    with open(army_fixed_info_path) as file:
        data = json.load(file)
        return data