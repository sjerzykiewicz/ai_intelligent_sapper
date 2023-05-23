from itertools import product

posibilities = {
    "dist_from_flag": ["<=10", ">10"],
    "bomb_type": ["landmine", "claymore", "hcb"],
    "surface_type": ["unpaved_road", "grass", "sand"],
    "weather": ["sunny", "rainy"],
    "time_of_day": ["day", "night"],
    "is_barrel_nearby": ["yes", "no"],
    "sapper_type": ["standard", "rain_defusing"],
    "is_low_temp": ["yes", "no"],
    "action": ["defuse"],
}

keys, values = zip(*posibilities.items())
perms = [dict(zip(keys, v)) for v in product(*values)]
for perm in perms:
    if perm["surface_type"] == "sand":
        perm["action"] = "defuse"
    if perm["surface_type"] == "unpaved_road":
        perm["action"] = "move"
    if perm["bomb_type"] == "claymore":
        perm["action"] = "defuse"
    if perm["dist_from_flag"] == "<=10":
        perm["action"] = "move"
    if perm["weather"] == "rainy":
        perm["action"] = "move"
    if perm["time_of_day"] == "night":
        perm["action"] = "defuse"
    if perm["is_barrel_nearby"] == "yes":
        if perm["is_low_temp"] == "yes":
            perm["action"] = "defuse"
        else:
            perm["action"] = "move"
    if perm["sapper_type"] == "rain_defusing":
        if perm["weather"] == "rainy":
            perm["action"] = "defuse"
    if perm["bomb_type"] == "hcb":
        perm["action"] = "move"

with open("input.csv", "w") as f:
    f.write(
        "dist_from_flag,bomb_type,surface_type,weather,time_of_day,is_barrel_nearby,sapper_type,is_low_temp,action\n"
    )
    for perm in perms:
        f.write(
            f'{perm["dist_from_flag"]},{perm["bomb_type"]},{perm["surface_type"]},{perm["weather"]},{perm["time_of_day"]},{perm["is_barrel_nearby"]},{perm["sapper_type"]},{perm["is_low_temp"]},{perm["action"]}\n'
        )
