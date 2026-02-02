import math

def calc_distance_hexes(x1, y1, x2, y2): #TODO: this doesn't work for us in the hex system, I think?
    source_army_loc = (x1, y1)
    target_army_loc = (x2, y2)
    return math.dist(source_army_loc, target_army_loc)

# def hex_distance(start, destination):
#     """Hex distance for axial coordinates."""
#     return int((abs(start.x - destination.x) 
#                + abs(start.x + destination.y - destination.y - destination.x) 
#                + abs(start.y - start.x)) / 2)