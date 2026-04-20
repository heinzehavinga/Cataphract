#Make this generate the maps for Commander (+world map)

#Drawn all hexes in scout range using current hex information.
# All know hexes outside scout range through ObservedHex.
# Make more transparant/grey based on time since last seen?

from cataphract.models import Commander, Map
from django.conf import settings
from .utils import hex_distance, hextypes
from PIL import Image, ImageDraw
import math
import random
from pathlib import Path

def get_tileset(tileset_name="wesnoth"):
    tileset = {}
    tileset_path = Path(settings.MEDIA_ROOT)/'tilesets'/tileset_name

    for key, name in hextypes.items():
        try:
            # print(key, name)
            files = list(tileset_path.glob(f'{name}*.png'))
            for p in files:
                tileset[f"tilesets/{tileset_name}/{p.name}"] = Image.open(p).convert("RGBA")
                # print("  ", p.name)
        except Exception as e:
            # print("  ", name, "missing")
            # print(e)
            pass
    return tileset

def create_hexagon(size=72, color=(128, 0, 128)):
    # Create a blank image with transparent background
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Calculate hexagon points (flat top)
    half = size // 2
    quarter = size // 4
    points = [
        (quarter, 0),
        (quarter + half, 0),
        (size, half),
        (quarter + half, size),
        (quarter, size), 
        (0, half),
    ]

    # Draw the hexagon
    draw.polygon(points, fill=color)
    return img

def render_map(map: Map) -> Image:
    size = 72
    tileset = get_tileset()

    # Make bitmap at correct size
    target = Image.new("RGB", (math.ceil(map.width*(size*.75)+size*.25), math.ceil((map.height+.5)*size)), (255, 255, 255))
    for hex in map.hexes.all():
        x = hex.x * (size*.75)
        y = hex.y * size
        if hex.x%2==1:
            y += size/2
        if hex.tile in tileset.keys():
            img = tileset[hex.tile]
            y -= math.floor((img.size[1] - size)/2)
            x -= math.floor((img.size[0] - size)/2)
            target.paste(img, (math.ceil(x), math.ceil(y)), img)
    return target

def render_region_layer(map: Map) -> Image:
    size = 72

    # Make bitmap at correct size
    target = Image.new("RGB", (math.ceil(map.width*(size*.75)+size*.25), math.ceil((map.height+.5)*size)), (255, 255, 255))
    for hex in map.hexes.all():
        x = hex.x * (size*.75)
        y = hex.y * size
        if hex.x%2==1:
            y += size/2
        
        # print(hex, hex.region)
        img = create_hexagon(size=size, color=(random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
        y -= math.floor((img.size[1] - size)/2)
        x -= math.floor((img.size[0] - size)/2)
        target.paste(img, (math.ceil(x), math.ceil(y)), img)
    return target

def make_map(mapid: Map, commander:Commander = None) -> None:
    map = Map.objects.get(id=mapid)
    
    if commander:
        print("generating map of:,", map, ",for Commander:", commander)
    else:
        print("generating map of:", map)

    target = render_map(map)

    print("saving to:", f"{settings.MEDIA_ROOT}/maps/{map.name}.png")
    target.save(f"{settings.MEDIA_ROOT}/maps/{map.name}.png")

def find_closest_fort(map, forts):
    result = {}

    for hex in map.hexes.all():
        if hex.is_fort:
            result[hex] = hex  # Important hexes are closest to themselves
            continue

        distances = []
        for fort in forts:
            dist = hex_distance(hex, fort)
            distances.append((dist, fort))

        min_dist = min(distances, key=lambda x: x[0])[0]
        candidates = [h for dist, h in distances if dist == min_dist]
        result[hex] = random.choice(candidates)

    return result

def calculate_regions(map: Map) -> None:
    #TODO:
    # make forts as found on map
    # make neutral faction
    # assign all forts to neutral faction
    # assign all hexes to closest fort
    # result = find_closest_fort(map, forts)
    # for hex, closest in result.items():
    #     # print(f"Hex {hex} is closest to fort {closest} with region {closest.region}")
    #     hex.region = closest.region
    pass

def calculate_polulation(map: Map) -> None:
    #TODO:
    # for each hex:
    # distance to fort is base pop
    # field/farmsland adds 20
    # road adds 20
    # river adds 20
    # town adds 20
    # city sets to 100
    pass