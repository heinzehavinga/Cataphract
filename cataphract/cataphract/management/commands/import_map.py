from django.core.management.base import BaseCommand, CommandError
from cataphract.models import World, Map, Region, Hex, Faction
import json
from django.utils import timezone


import random
from collections import defaultdict

def hex_distance(a, b):
    return (abs(a.x - b.x) + abs(a.y - b.y)) / 2

def find_closest_fort(hexes, forts):
    result = {}

    for hex in hexes:
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

class Command(BaseCommand):
    help = "Import a hexmap JSON map to a world"

    def add_arguments(self, parser):
        parser.add_argument("mappath", nargs="+", type=str)

    def handle(self, *args, **options):
        map_path = options["mappath"][0]
        print("Importing map:", map_path)
        with open(map_path, 'r') as f:
            data = json.load(f)
        print(f"Opening map with width: {data['width']}, height: {data['height']}")
        
        world = World.objects.get_or_create(world_name="New World")[0]
        world.save()
        map = Map.objects.get_or_create(name="Our Land", world=world)[0]
        map.width = data['width']
        map.height = data['height']
        map.save()
        print(map)

        hexes = []
        map.hexes.all().delete()  # We empty the map first
        map.regions.all().delete()  # We empty the map first
        for tile in data['map']:
            r = tile.get('rivers', '0')
            if len(r) < 1:
                r = 0
            else:
                r = int(r)
            h = Hex(
                map=map, x=tile['x'], y=tile['y'],
                type=int(tile['type']),
                road=bool(tile.get('roads', False)),
                river=r,
                last_foraged=timezone.now()
            )
            hexes.append(h)
        Hex.objects.bulk_create(hexes)
        print("Added", map.hexes.count(), "hexes")

        faction = Faction.objects.first()
        forts = [h for h in hexes if h.is_fort]
        for h in forts:
            r = Region.objects.create(map=map, faction=faction)
            h.region = r
            h.save()
        print("Discovered", len(forts), "regions")

        result = find_closest_fort(hexes, forts)
        for hex, closest in result.items():
            # print(f"Hex {hex} is closest to fort {closest} with region {closest.region}")
            hex.region = closest.region
        
        Hex.objects.bulk_update(hexes, fields=['region'])
        print("Calculated", len(hexes), "hexes to their regions")
        print("Done 🗺️⤵️⬡⬢⬡")