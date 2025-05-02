from django.db import models


#Check the wiki for the models
class Unittype(models.Model): #Could this be a sub child of landmark?
    name = models.CharField(max_length=200)
    road_speed = models.IntegerField(default=0)
    offroad_speed = models.IntegerField(default=0)
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
    last_foraged = models.DateTimeField("last foraging")
    def __str__(self):
        return f'{self.x}, {self.y}'
    #Should add road, and rivers

class Commander(models.Model):
    name = models.CharField(max_length=200)
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
    bio = models.TextField()
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
    order = models.TextField()
    commander = models.ForeignKey(Commander, on_delete=models.PROTECT)
    date_start = models.DateTimeField("start of order")
    date_end = models.DateTimeField("end of order")
    def __str__(self):
        return self.name