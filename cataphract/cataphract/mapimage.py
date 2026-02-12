#Make this generate the maps for Commander (+world map)

#Drawn all hexes in scout range using current hex information.
# All know hexes outside scout range through ObservedHex.
# Make more transparant/grey based on time since last seen?

from cataphract.models import Commander, Map
from django.conf import settings
from .utils import hextypes
from PIL import Image
import math
from pathlib import Path

def get_tileset(tileset_name="wesnoth"):
    tileset = {}
    tileset_path = Path(settings.MEDIA_ROOT)/'tilesets'/tileset_name

    for key, name in hextypes.items():
        try:
            print(key, name)
            files = list(tileset_path.glob(f'{name}*.png'))
            for p in files:
                tileset[f"tilesets/{tileset_name}/{p.name}"] = Image.open(p).convert("RGBA")
                print("  ", p.name)
        except Exception as e:
            print("  ", name, "missing")
            print(e)
    return tileset

def make_map(mapid: Map, commander:Commander = None) -> None:
    map = Map.objects.get(id=mapid)
    size = 72
    
    if commander:
        print("generating map of:,", map, ",for Commander:", commander)
    else:
        print("generating map of:", map)

    tileset = get_tileset()

    # Make bitmap at correct size
    target = Image.new("RGBA", (math.ceil(map.width*(size*.75)+size*.25), math.ceil((map.height+.5)*size)), (255, 255, 255, 255))
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
        print(hex)

    print("saving to:", f"{settings.MEDIA_ROOT}/maps/{map.name}.png")
    target.save(f"{settings.MEDIA_ROOT}/maps/{map.name}.png")
