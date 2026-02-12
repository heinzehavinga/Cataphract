from django.core.management.base import BaseCommand, CommandError

from cataphract.mapimage import make_map

class Command(BaseCommand):
    help = "Generate an image of a map"

    def add_arguments(self, parser):
        parser.add_argument("map", nargs="+", type=int)

    def handle(self, *args, **options):
        make_map(options["map"][0])
        print("Done 🗺️✍️⬡⬢⬡")