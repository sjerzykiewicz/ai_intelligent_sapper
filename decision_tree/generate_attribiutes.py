from itertools import product
from random import shuffle

posibilities = {
    "dist_from_flag": ["<=3", ">3"],
    "bomb_type": ["landmine", "claymore", "hcb"],
    "surface_type": ["unpaved_road", "grass", "sand"],
    "weather": ["sunny", "rainy"],
    "time_of_day": ["day", "night"],
    "is_barrel_nearby": ["yes", "no"],
    "sapper_type": ["standard", "rain_defusing"],
    "is_low_temp": ["yes", "no"],
    "answer": ["defuse"],
}

keys, values = zip(*posibilities.items())
perms = [dict(zip(keys, v)) for v in product(*values)]
for perm in perms:
    if perm["surface_type"] == "sand":
        perm["answer"] = "defuse"
    if perm["surface_type"] == "unpaved_road":
        perm["answer"] = "move"
    if perm["bomb_type"] == "claymore":
        perm["answer"] = "defuse"
    if perm["dist_from_flag"] == "<=3":
        perm["answer"] = "move"
    if perm["weather"] == "rainy":
        perm["answer"] = "move"
    if perm["time_of_day"] == "night":
        perm["answer"] = "defuse"
    if perm["sapper_type"] == "rain_defusing":
        if perm["weather"] == "rainy":
            perm["answer"] = "defuse"
    if perm["is_barrel_nearby"] == "yes":
        if perm["is_low_temp"] == "yes":
            perm["answer"] = "defuse"
        else:
            perm["answer"] = "move"
    if (
        perm["is_barrel_nearby"] == "yes"
        and perm["sapper_type"] == "standard"
        and perm["is_low_temp"] == "no"
    ):
        perm["answer"] = "move"
    if perm["bomb_type"] == "hcb":
        perm["answer"] = "move"

with open("./input.csv", "w") as f:
    f.write(
        "dist_from_flag,bomb_type,surface_type,weather,time_of_day,is_barrel_nearby,sapper_type,is_low_temp,answer\n"
    )
    cnt = 0
    shuffle(perms)
    for perm in perms:
        if cnt % 2 == 0:
            f.write(
                f'{perm["dist_from_flag"]},{perm["bomb_type"]},{perm["surface_type"]},{perm["weather"]},{perm["time_of_day"]},{perm["is_barrel_nearby"]},{perm["sapper_type"]},{perm["is_low_temp"]},{perm["answer"]}\n'
            )
        cnt += 1
