hextypes = {
    0: "grassland",
    1: "forest",
    2: "woodlands",
    3: "hills",
    4: "hillforest",
    5: "mountain",
    6: "sea",
    7: "ocean",
    8: "town",
    9: "city",
    10: "castle",
    11: "fields",
    12: "swamp",
    13: "bog",
    14: "floodplane",
    15: "marsh",
    16: "snow",
    17: "snowforest",
    18: "snowwoodlands",
    19: "snowhills",
    20: "snowhillforest",
    21: "snowsea",
    22: "snowtown",
    23: "snowcastle",
    24: "desert",
    25: "deserthill",
    26: "desertdunes",
    27: "desertmesa",
    28: "desertoasis",
    29: "deserttribe",
    30: "deserttown",
    31: "desertcastle",
    32: "rainforest",
    36: "coasttowneast",
    37: "coasttownwest",
    38: "lighthouse",
    39: "lair",
    40: "farm",
}

city_types = [9]
town_types = [8, 22, 30, 36, 37]
castle_types = [10, 23, 31]
fort_types = []
fort_types.extend(city_types)
fort_types.extend(town_types)
fort_types.extend(castle_types)

def is_fort(hex):
    return hex.type in fort_types

def hextype_to_name(Hex):
    r = hextypes.get(Hex.type, None)
    if not r:
        raise ValueError(f"Unknown hex type: {Hex.type} for hex {Hex.x}, {Hex.y}: {Hex.type}")

    return r
