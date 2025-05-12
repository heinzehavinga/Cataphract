from django.db import models

#Check the wiki for the models
class Unittype(models.Model): #Should Wagon, Non combatant be included.
    list_display = ("name", "road_speed", "scout_distance",)
    name = models.CharField(max_length=200)
    road_speed = models.IntegerField(default=0)
    forced_march_speed = models.IntegerField(default=0)
    offroad_speed = models.IntegerField(default=0) #if 0, no offroading with this unit
    scout_distance = models.IntegerField(default=0)
    supplies_per_day = models.IntegerField(default=0)
    carry_weight = models.IntegerField(default=0) #Total carry weight, including Loot and Supplies
    units_per_mile = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Strongholdtype(models.Model): #Could this be a sub child of landmark?
    list_display = ("name", "defense_bonus", "starting_infantry","starting_cavalry")
    name = models.CharField(max_length=200)
    defense_bonus = models.IntegerField(default=0)
    loot_multiplier = models.IntegerField(default=0)
    starting_infantry = models.IntegerField(default=0)
    starting_cavalry = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Faction(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField(help_text = "A little bio for the faction, who are they, what drives them etc.")
    def __str__(self):
        return self.name

class Region(models.Model):
    list_display = ("name", "faction", "last_recruitement")
    name = models.CharField(max_length=200)
    bio = models.TextField()
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    last_recruitement = models.DateTimeField("last recruitment")
    def __str__(self):
        return self.name

class Hex(models.Model):
    list_display = ("region", "x", "y", "settlement_score")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    settlement_score = models.IntegerField(default=0)
    road = models.BooleanField(default=True)
    river = models.IntegerField(default=0) #probably a 123456, with every side being a number so a river of 234 has river on sides 2 and 3 and 4
    last_foraged = models.DateTimeField("last foraging")
    def __str__(self):
        return f'{self.x}, {self.y}'


class Player(models.Model):
    name = models.CharField(max_length=200)
    discord_id = models.BigIntegerField(default=0)
    notes = models.TextField()
    def __str__(self):
        return self.name

class Commander(models.Model): #Need to add perks and feats! How will we program those in?
    list_display = ("name", "faction")
    name = models.CharField(max_length=200)
    player_id = models.ForeignKey(Player, on_delete=models.PROTECT, blank=True, null=True)
    age = models.IntegerField(default=18) #This should probably be a DateField
    bio = models.TextField()
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
    #Add attributes, items etc.


class ObservedHex(Hex): #Can we inheret
    Commander = models.ForeignKey(Commander, on_delete=models.PROTECT, blank=True, null=True) #These should be deleted if Commander dies?
    Date_Observed = models.DateTimeField("last observed")
    def __str__(self):
        return f'{self.x}, {self.y} observer by f{self.commander} on DATE'
    #Should add road, and rivers

class Strongholds(models.Model): #Could this be a sub child of landmark?
    list_display = ("name", "faction","region")
    name = models.CharField(max_length=200)
    bio = models.TextField()
    stronghold_type = ( #We need to find a complete order list
        (1, "Fortress"),
        (2, "City"),
        (3, "Fortified town"),
    )
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    gate = models.BooleanField(default=True)
    sieged = models.BooleanField(default=False)
    loot = models.IntegerField(default=0) #Default is based on type some sort on save field.
    #Can we generate a city garrison when creating a city?
    def __str__(self):
        return self.name

class Army(models.Model): 
    list_display = ("name", "commander")
    name = models.CharField(max_length=200)
    bio = models.TextField()
    commander = models.ForeignKey(Commander, on_delete=models.PROTECT, blank=True)
    owner = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT) # Only need army has no commander, These will be a single detachment
    def __str__(self):
        return self.name

class Detachment(models.Model):
    list_display = ("name", "commander")
    name = models.CharField(max_length=200)
    bio = models.TextField(blank=True)
    unittype = models.ForeignKey(Unittype, on_delete=models.PROTECT)
    units = models.IntegerField(default=0)
    non_combantants = models.IntegerField(default=0)
    wagons = models.IntegerField(default=0)
    supplies = models.IntegerField(default=0)
    loot = models.IntegerField(default=0)
    personal_loot = models.IntegerField(default=0)
    morale = models.IntegerField(default=9)
    army = models.ForeignKey(Army, on_delete=models.PROTECT, null=True, blank=True)
    def __str__(self):
        wagon_string = ""
        if self.wagons > 0:
            wagon_string = f', {self.wagons} wagons'
        return f'{self.name}: {self.units} {self.unittype}{wagon_string}'
    #Make property: total carrying weight.


class Order(models.Model):
    list_display = ("order_types", "commander", "date_start", "date_end")
    order_types = ( #We need to create a complete order list
        (1, "Move"),
        (2, "Rest"),
        (3, "Build"),
        (4, "Recruit"), #takes a month, commander is free to move on, should that be a Boolean field
        (5, "Forage"), #how long does foraging take?
        (6, "Siege"),
        (7, "Unique")
    )
    order = models.IntegerField(choices=order_types, default=1)
    unique_description = models.TextField(blank=True)
    commander = models.ForeignKey(Commander, on_delete=models.PROTECT)
    date_start = models.DateTimeField("start of order")
    date_end = models.DateTimeField("end of order")
    completed = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.commender}: {self.order_types} DATE START DATE END'