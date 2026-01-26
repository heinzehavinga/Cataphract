#Make this generate the maps for Commander (+world map)

#Drawn all hexes in scout range using current hex information.
# All know hexes outside scout range through ObservedHex.
# Make more transparant/grey based on time since last seen?

from .models import Commander


def make_map(commander:Commander) -> None:
    print("generating map for Commander:", commander)
