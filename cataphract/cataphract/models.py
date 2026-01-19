from django.db import models
from faker import Faker
from django.db.models import Sum, Q, Max, Avg
import math, random
from datetime import datetime
faker = Faker('en_GB')


#TODO: add World object, for map editor things (like world width and height)    
#TODO: add Discord object, for channel id and such (THis could also be a generic game object later, but not now)
class World(models.Model):
    discord_guild = models.IntegerField(default=0)
    discord_channel_id = models.IntegerField(default=0)
    discord_channel_name = models.CharField(default="cataphracts")
    world_name = models.CharField(default=faker.last_name)
    world_width = models.IntegerField(default=0) #width in hexes
    world_height = models.IntegerField(default=0) #height in hexes #TODO make hexes automatically when creating world?
    start_time = models.DateTimeField("when did the game start", default=datetime.now)
    last_tick  = models.DateTimeField("last ingame tick", default=datetime.now)
    tick_speed = models.IntegerField(default=4) #Hours between each tick

# class Referee: #todo these should be Django users instead, as they might need to login to do some things
#     name = models.CharField(max_length=200, default=faker.name)
#     discord_id = models.BigIntegerField(default=0)


class Modifier(models.Model): 
    #TODO: This should probably be a longer list but for know it's fine.
    road_speed_bonus = models.IntegerField(default=0)
    forced_march_speed_bonus = models.IntegerField(default=0)
    offroad_speed_bonus = models.IntegerField(default=0) #if _bonus0, no offroading with this unit
    scout_distance_bonus = models.IntegerField(default=0)
    supplies_per_day_bonus = models.IntegerField(default=0)
    harrier_bonus_bonus = models.IntegerField(default=0)
    carry_weight_bonus = models.IntegerField(default=0) #Total carry weight, including Loot and Supplies
    carry_weight_modifier = models.FloatField(default=0.0) #Total carry weight, including Loot and Supplies
    units_per_mile_bonus = models.IntegerField(default=0)
    default_non_combatant_modifier = models.FloatField(default=0.0) #How many non combantants does this detachment has per default?
    pick_up_non_combatant_modifier = models.FloatField(default=0.0) #How many non combantants does this detachment has per default?
    recruitement_rate_bonus = models.FloatField(default=0)
    resting_morale_bonus = models.IntegerField(default=0)
    besiege_bonus = models.IntegerField(default=0)
    defend_stronghold_bonus = models.IntegerField(default=0)
    duelist_bonus = models.IntegerField(default=0.0)
    casualties_modifier = models.FloatField(default=0.0)
    capturechance_bonus = models.IntegerField(default=0)
    pillage_chance_modifier = models.FloatField(default=0)
    revolt_chance_bonus = models.IntegerField(default=0)
    defend_threshold_modifier = models.FloatField(default=0.0)
    cavalry_scout_bonus = models.IntegerField(default=0)
    morale_roll_bonus = models.IntegerField(default=0)
    loot_found_modifier = models.FloatField(default=0.0)
    forage_modifier = models.FloatField(default=0.0)
    siege_engine_build_modifier = models.FloatField(default=0.0)
    morale_loss_battle_modifier = models.FloatField(default=0.0)
    recruitement_rate_good_country_bonus = models.FloatField(default=0) #per settlementscore on hex

# class Weathertypes(models.Model): #TODO: This is a big one, to do weahter in this game?


class Faction(models.Model):
    #TODO: Add a banner image
    name = models.CharField(max_length=200, default=faker.first_name)
    bio = models.TextField(help_text = "A little bio for the faction, who are they, what drives them etc.")
    def __str__(self):
        return self.name


#Check the wiki for the models
class Unittype(models.Model): #Should Wagon, Non combatant be included?
    list_display = ("name", "road_speed", "scout_distance",)
    name = models.CharField(max_length=200, default=faker.first_name)
    description = models.TextField(help_text = "A little description of the unit")
    road_speed = models.IntegerField(default=0)
    forced_march_speed = models.IntegerField(default=0)
    offroad_speed = models.IntegerField(default=0) #if 0, no offroading with this unit
    scout_distance = models.IntegerField(default=0)
    supplies_per_day = models.IntegerField(default=0)
    harrier_bonus = models.IntegerField(default=0)
    carry_weight = models.IntegerField(default=0) #Total carry weight, including Loot and Supplies
    units_per_mile = models.IntegerField(default=0)
    default_non_combatant = models.FloatField(default=0.25) #How many non combantants does this detachment has per default?
    recruitement_rate = models.FloatField(default=0.0) #per settlementscore on hex
    recruitement_rate_good_country = models.FloatField(default=1.0) #per settlementscore on hex
    unique_type = models.BooleanField(default=False)
    unique_type_faction = models.ForeignKey(Faction, on_delete=models.PROTECT, null=True, blank=True) #TODO: This could be a generic foreign key?
    base_unit_template = models.ForeignKey('self', on_delete=models.PROTECT, null=True, blank=True)
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

class Region(models.Model): #TODO: Regions no longer exsist in rulesset
    list_display = ("name", "faction", "last_recruitement")
    name = models.CharField(max_length=200, default=faker.name)
    bio = models.TextField()
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    last_recruitement = models.DateTimeField("last recruitment")
    def __str__(self):
        return self.name

    @property
    def recruit_infantry(self):
        "Returns infantry recruit total"
        hexes = self.hex_set.all()
        return round(hexes.aggregate(Sum('settlement_score'))['settlement_score__sum'],-2)
    
class Hex(models.Model):
    list_display = ("region", "x", "y", "settlement_score")
    x = models.IntegerField(default=0)
    y = models.IntegerField(default=0)
    ##Type of landscape
    type = models.IntegerField(default=0)

    region = models.ForeignKey(Region, on_delete=models.PROTECT, blank=True, null=True) #TODO: Should be change to stronghold
    settlement_score = models.IntegerField(default=20) #TODO: create algorithm to calculate this automatically
    ## All roads start in the middle 1 top and than clockwise
    road = models.BooleanField(default=True)
    
    #Based on ribs 1 is the top rib and then clockwise.
    river = models.IntegerField(default=0) #probably a 123456, with every side being a number so a river of 234 has river on sides 2 and 3 and 4
    last_foraged = models.DateTimeField("last foraging")
    foraged_amount_season = models.IntegerField(default=0) #Should reset every season TODO: Add season trigger
    def __str__(self):
        return f'{self.x}, {self.y}'

    @property
    def get_neighbours(self):
        "Returns Neighbouring hexes and the travel costs."
#Please add a description of this to the wiki!
        #Check if x position is even or uneven.
        # in case over even, hex left is, left Down 
        # In case of odd, hex left is left up

#Getting neighbors
#Get all surrounding hexes, so x same and Y one above and one below.
# If odd neighbour are x of the same y-coordinate and one y coordinate down
# If even neighbour are x of the same y-coordinate and one y coordinate up
        hexes = self.hex_set.filter()

#Then check if:
    #Do we have a road from this hex to that hex, than score +1
    #Does this hex, or the target hex have a river on the rib, then score -1
    #is the target hex A uncrossable terrain type? the score -100
    #return dict with scores
        return round(hexes.aggregate(Sum('settlement_score'))['settlement_score__sum'],-2)

class Player(models.Model):
    name = models.CharField(max_length=200, default=faker.name)
    discord_id = models.BigIntegerField(default=0)
    notes = models.TextField()
    def __str__(self):
        return self.name

class Commander(models.Model): #Need to add perks and feats! How will we program those in?
    list_display = ("name", "faction")
    name = models.CharField(max_length=200, default=faker.name)
    player_id = models.ForeignKey(Player, on_delete=models.PROTECT, blank=True, null=True) #TODO: would this be better to make this relation the other way around?
    age = models.IntegerField(default=18) #This should probably be a DateField
    bio = models.TextField()
    # portrait = models.ImageField(upload_to='portraits/', blank=True, null=True) #TODO: does this allow to look at already uploaded files
    # map_sprite = models.ImageField(upload_to='units/', blank=True, null=True)
    relation_commander = models.ForeignKey("self", on_delete=models.PROTECT, blank=True, null=True) 
    relation_name = models.CharField(max_length=200, blank=True, null=True)
    faction = models.ForeignKey(Faction, on_delete=models.PROTECT)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT)
    def __str__(self):
        return self.name
    #Add attributes, items etc.

    def save(self, *args, **kwargs):
        if not self.pk:
            # This code only happens if the objects is
            # not in the database yet. Otherwise it would
            # have pk
            if self.relation_commander is not None:
                relation = random.randint(1,17)
                if relation == 1:
                    self.relation_name = "Child"
                    self.age = 14+ random.randint(1,6)+random.randint(1,6)+random.randint(1,6)
                elif relation == 2:
                    self.relation_name = "Sibling"
                    self.age = 20+ random.randint(1,20)+random.randint(1,20)
                elif relation == 3:
                    self.relation_name = "Parent"
                    self.age = 30+ random.randint(1,20)+random.randint(1,20)+random.randint(1,20)
                elif relation == 4:
                    self.relation_name = "Niece/Nephew"
                    self.age = 16+ random.randint(1,20)
                elif relation == 5:
                    self.relation_name = "Uncle/Aunt"
                    self.age = 30+ random.randint(1,20)+random.randint(1,20)+random.randint(1,20)
                elif relation == 6:
                    self.relation_name = "Cousin"
                    self.age = 20+ random.randint(1,20)+ random.randint(1,20)
                #Original 7 and 8 result are skipped for now
                elif relation == 7:
                    self.relation_name = "Spouse"
                    self.age = 20+ random.randint(1,20)+ random.randint(1,20)
                elif relation == 8:
                    self.relation_name = "Friend"
                    self.age = 20+ random.randint(1,20)+ random.randint(1,20)
                elif relation == 9:
                    self.relation_name = "Rival"
                    self.age = 20+ random.randint(1,20)+ random.randint(1,20)
                elif relation == 10:
                    self.relation_name = "Student"
                    self.age = 16+ random.randint(1,20)
                elif relation == 11:
                    self.relation_name = "Teacher"
                    self.age = 30+ random.randint(1,20)+random.randint(1,20)+random.randint(1,20)
                elif relation == 12:
                    self.relation_name = "Priest"
                    self.age = 30+ random.randint(1,20)+random.randint(1,20)+random.randint(1,20)
                elif relation == 13:
                    self.relation_name = "Councilor"
                    self.age = 20+ random.randint(1,20)+random.randint(1,20)+random.randint(1,20)
                elif relation == 14:
                    self.relation_name = "Bodyguard"
                    self.age = 20+ random.randint(1,20)+random.randint(1,20)
                elif relation == 15:
                    self.relation_name = "Quartermaster"
                    self.age = 20+ random.randint(1,20)+random.randint(1,20)
                elif relation == 16:
                    self.relation_name = "Creditor"
                    self.age = 20+ random.randint(1,20)+random.randint(1,20)
                elif relation == 17:
                    self.relation_name = "Favorite"
                    self.age = 16+ random.randint(1,20)+random.randint(1,20)
                
        super(Commander, self).save(*args, **kwargs)        
        #Generate X random traits based on 
        if self.age > 20:
            trait_amount = 1 + math.floor((self.age-20)/10)
            
            traits = Trait.objects.order_by('?').all()[:trait_amount]
            for trait in traits:
                trait.owners.add(self)
                trait.save()
        

class Item(Modifier):
    name = models.CharField(max_length=200, default=faker.first_name)
    desc = models.TextField() #Description of item, also include any roleplaying qualities of the item (owner of this sword is seen as the king of XY, etc.)
    owner = models.ForeignKey(Commander, on_delete=models.PROTECT, blank=True, null=True) #What happens if Commander dies?

class Trait(Modifier): 
    name = models.CharField(max_length=200, default=faker.first_name)
    desc = models.TextField() #Description of item, also include any roleplaying qualities of the item (owner of this sword is seen as the king of XY, etc.)
    owners = models.ManyToManyField(Commander, blank=True, null=True) #TODO: Is this the right way of doing this?
    def __str__(self):
        return self.name

class ObservedHex(Hex): #Can we inheret
    Commander = models.ForeignKey(Commander, on_delete=models.PROTECT, blank=True, null=True) #These should be deleted if Commander dies?
    Date_Observed = models.DateTimeField("last observed")
    def __str__(self):
        return f'{self.x}, {self.y} observer by f{self.commander} on DATE'
    #Should add road, and rivers

class Strongholds(models.Model): #Could this be a sub child of landmark?
    list_display = ("name", "faction","region")
    name = models.CharField(max_length=200, default=faker.city)
    bio = models.TextField()
    stronghold_type = models.ForeignKey(Strongholdtype, on_delete=models.PROTECT, blank=True, null=True)
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
    commander = models.ForeignKey(Commander, on_delete=models.PROTECT, blank=True, null=True)
    owner = models.ForeignKey(Faction, on_delete=models.PROTECT, blank=True)
    location = models.ForeignKey(Hex, on_delete=models.PROTECT, blank=True, null=True) # Only needed when army has no commander, These will be a single detachment (special unit types like messenger?)
    harried = models.BooleanField(default=False) 
    def __str__(self):
        return self.name
    
    @property
    def morale(self):
        "Returns morale for army"
        detachements = self.detachment_set.all()
        return math.floor(detachements.aggregate(Avg('morale'))['morale__avg'])

    @property
    def scout_distance(self):
        "Returns scouting range based on unit with biggest scouting randge"
        return self.detachment_set.all().aggregate(Max('scout_distance'))['scout_distance__max']
    @property
    def supplies(self):
        "Returns supplies army carry"
        return self.detachment_set.all().aggregate(Sum('supplies'))['supplies__sum']
    
    @property
    def loot(self):
        "Returns loot army carries"
        return self.detachment_set.all().aggregate(Sum('loot'))['loot__sum']

    @property
    def carrying_weight(self):
        "Returns maximum carrying weight for complete army"
        return round(sum(d.carrying_weight for d in self.detachment_set.all()),0)
    
    @property
    def carrying_weight_left(self):
        "Returns maximum carrying weight for complete army"
        return round(sum(d.carrying_weight_left for d in self.detachment_set.all()),0)

    @property
    def travel_length(self):
        "Returns Total travel length of army"
        return round(sum(d.travel_length for d in self.detachment_set.all()),2)
    
    @property
    def supplies_per_day(self):
        "Returns the required supplies per day"
        return sum(d.supplies_per_day for d in self.detachment_set.all())
    
    @property
    def supplies_days_left(self):
        "Returns the required supplies per day"
        supplies_per_day = sum(d.supplies_per_day for d in self.detachment_set.all())
        supplies = sum(d.supplies for d in self.detachment_set.all())
        return round(supplies_per_day/supplies, 2)
    
    @property
    def non_combantants(self):
        "Returns the required supplies per day"
        return round(self.detachment_set.all().aggregate(Sum('non_combantants'))['non_combantants__sum'],0)

class Detachment(models.Model):
    list_display = ("name", "commander")
    name = models.CharField(max_length=200, default=faker.company)
    bio = models.TextField(blank=True, default=faker.catch_phrase)
    unittype = models.ForeignKey(Unittype, on_delete=models.PROTECT)
    units = models.IntegerField(default=0)
    non_combantants = models.IntegerField(default=0)
    wagons = models.IntegerField(default=0)
    supplies = models.IntegerField(default=0)
    loot = models.IntegerField(default=0)
    siege_tower = models.IntegerField(default=0) #We assume one siege tower is 1 wagon to keep the math simple
    personal_loot = models.IntegerField(default=0)
    morale = models.IntegerField(default=9)
    army = models.ForeignKey(Army, on_delete=models.PROTECT, null=True, blank=True)    
    
    def __str__(self):
        wagon_string = ""
        if self.wagons > 0:
            wagon_string = f', {self.wagons} wagons'
        return f'{self.name}: {self.units} {self.unittype}{wagon_string}'
    #Make property: total carrying weight.

    @property
    def carrying_weight(self):
        "Returns detachment carrying limit"
        weight = self.unittype.carry_weight*self.units
        weight += self.wagons * 1000 #TODO: don't hardcode carry capacity wagons
        weight += self.non_combantants * 15 #TODO: don't hardcode carry capacity non combatants
        return round(weight,0)
    
    @property
    def carrying_weight_left(self):
        return self.carrying_weight - (self.supplies+self.loot+self.personal_loot+(self.siege_tower*1000)) #TODO: Uses hardcoded wagons capacity.

    @property
    def travel_length(self):
        "Returns detachment length (in miles) while traveling"
        length = self.units/self.unittype.units_per_mile
        length += self.wagons/50 #TODO: don't hardcode amount of wagons per mile
        length += self.non_combantants/5000 #TODO: don't hardcode amount of non combatents per mile
        return round(length,2)
    
    @property
    def scout_distance(self):
        "Returns the required supplies per day"
        return self.unittype.scout_distance
    
    @property
    def supplies_per_day(self):
        "Returns the required supplies per day"
        return self.units * self.unittype.supplies_per_day

    @property
    def supplies_days_left(self):
        "Returns the required supplies per day"
        return round(self.supplies_per_day/self.supplies, 2)

class playerMessage(models.Model):
    sending_commander = models.ForeignKey(Commander, on_delete=models.PROTECT, related_name='sending_commander')
    recieving_commander = models.ForeignKey(Commander, on_delete=models.PROTECT, related_name='recieving_commander')
    contents = models.TextField(help_text = "Message content")
    sent = models.DateTimeField("start of order")
    recieved = models.BooleanField(default=True)
    completed = models.BooleanField(default=True)

# class News(models.Model): #TODO: How do you check if News has been delivered to every player?

class RefMessage(models.Model):
    #TODO: make it possible to link to relevant Commanders (for setting position or states)
    message = models.TextField(blank=True, default=faker.catch_phrase)
    discord_url = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=True)
    completed_by = models.TextField(blank=True, default="ref") #TODO: This should be based on referee user object

class Order(models.Model):
    #TODO: I would like to be able have one order in the queue, so pleople can do "When I complete rest, move to X. Or when move to X is complete, Forage."
    list_display = ("order_types", "commander", "date_start", "date_end")
    order_types = ( #TODO: make this a seperate table with standard durations etc.
        (1, "Move"),
        (2, "Rest"),
        (3, "Build"),
        (4, "Recruit"), #takes a month, commander is free to move on, should that be a Boolean field? TODO: Is this an area order? What prevents commanders to recruit in every stronghold?
        (5, "Forage"), #Takes a day
        (6, "Siege"),
        (7, "Harrying - killing soldiers"), #Takes a day
        (8, "Harrying - torching supplies"), #Takes a day
        (9, "Harrying - stealing loot"), #Takes a day
        (10, "Operations")
    )
    order = models.IntegerField(choices=order_types, default=1)
    unique_description = models.TextField(blank=True)
    commander = models.ForeignKey(Commander, on_delete=models.PROTECT)
    date_start = models.DateTimeField("start of order")
    date_end = models.DateTimeField("end of order", null=True, blank=True)
    completed = models.BooleanField(default=True)
    week_counter = models.IntegerField(default=0) #Number to tell how many week bonuses have been giving (morale, siege threshold)
    start_hex = models.ForeignKey(Hex, on_delete=models.PROTECT, null=True,  blank=True, related_name='starting_hex') #TODO: This should be the current location of the commander
    end_hex = models.ForeignKey(Hex, on_delete=models.PROTECT, null=True,  blank=True, related_name='end_hex')
    selected_detachment =  models.ForeignKey(Detachment, on_delete=models.PROTECT, null=True,  blank=True, related_name='end_hex') #Only to be used with Harried commands
    target_army = models.ForeignKey(Army, on_delete=models.PROTECT, null=True,  blank=True, related_name='target_army') #Only to be used with Harried commands
    
    def save(self):
        #TODO: Make an order always start and end at a tick?
        # self.date_start = 
        # self.date_end =
        #TODO: How does this work for a move order?!
        for order in self.commander.order_set.filter(~Q(order=4)):
            if self.date_start < order.date_end:
                self.date_start = order.date_end
        super(Order, self)

    def __str__(self):
        return f'{self.commender}: {self.order_types} DATE START DATE END'