from django.db import models

#Check the wiki for the models
class Unittype(models.Model): #Could this be a sub child of landmark?
    name = models.CharField(max_length=200)
    road_speed = models.IntegerField(default=0)
    offroad_speed = models.IntegerField(default=0) #if 0, no offroading with this unit
    scout_distance = models.IntegerField(default=0)
    supplies_per_day = models.IntegerField(default=0)
    carry_weight = models.IntegerField(default=0) #Loot and Supplies
    units_per_mile = models.IntegerField(default=0)
    def __str__(self):
        return self.name

class Strongholdtype(models.Model): #Could this be a sub child of landmark?
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
    name = models.CharField(max_length=200)
    bio = models.TextField()
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    last_recruitement = models.DateTimeField("last recruitment")
    def __str__(self):
        return self.name

class Hex(models.Model):
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    settlement_score = models.IntegerField(default=0)
    settlement_score = models.IntegerField(default=20)
    road = models.BooleanField(default=True)
    river = models.IntegerField(default=0) #probably a 123456, with every side being a number so a river of 234 has river on sides 2 and 3 and 4
    last_foraged = models.DateTimeField("last foraging")
    def __str__(self):
        return f'{self.x}, {self.y}'
    #Should add road, and rivers


class Player(models.Model):
    name = models.CharField(max_length=200)
    discord_id = models.IntegerField(default=0)
    notes = models.TextField()
    def __str__(self):
        return self.name
    #Add attributes, items etc.

class Commander(models.Model): #Need to add perks and feats! How will we program those in?
    name = models.CharField(max_length=200)
    player_id = models.ForeignKey(Player, on_delete=models.PROTECT, blank=True, null=True)
    age = models.IntegerField(default=18)
    bio = models.TextField()
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
    #Add attributes, items etc.

class Strongholds(models.Model): #Could this be a sub child of landmark?
    name = models.CharField(max_length=200)
    bio = models.TextField()
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT, blank=True)
    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True)
    gate = models.BooleanField(default=True)
    sieged = models.BooleanField(default=False)
    loot = models.IntegerField(default=0) #Default is based on type... 
    def __str__(self):
        return self.name

class Army(models.Model): #Could this be a sub child of landmark?
    name = models.CharField(max_length=200)
    bio = models.TextField()
    commander = models.ForeignKey(Commander, on_delete=models.PROTECT, blank=True)
    owner = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT) # Only need if no commander, Detachtment becomes 
    def __str__(self):
        return self.name

class Detachment(models.Model): #Could this be a sub child of landmark?
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
    def __str__(self):
        return self.name


class Order(models.Model):
    order_types = ( #We need to find a complete order list
        (1, "Move"),
        (2, "Rest"),
        (3, "Build"),
        (4, "Unique"),
    )
    order = models.IntegerField(choices=order_types, default=1)
    unique_description = models.TextField(blank=True)
    commander = models.ForeignKey(Commander, on_delete=models.PROTECT)
    date_start = models.DateTimeField("start of order")
    date_end = models.DateTimeField("end of order")
    def __str__(self):
        return self.name