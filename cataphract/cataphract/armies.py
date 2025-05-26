#TODO: Add all the order logic in here please.
import random
from .models import *
from django.db.models import Q
from faker import Faker
faker = Faker('en_GB')

def moraleCheck(commander, army):
    """
       Do a morale check
    """

    response = {'outcome':''}
    
    morale = 0

    detachments = army.detachment_set.all()
    for detachment in detachments:
        morale += detachment.morale
    
    response['starting_morale'] = int(morale/len(detachments))
    response['morale_roll'] = random.randint(1,6) + random.randint(1,6)
    if response['morale_roll'] <= response['starting_morale']:
        response['outcome'] = f'Rolled {response['morale_roll']} against {response['starting_morale']} starting morale.\n Morale held, nothing happens'
    else:
        response['outcome'] = 'Morale check failed, outcome based on: \n'
        
        if response['morale_roll'] == 2:
            response['outcome'] += '2. Mutiny. 19-in-20 chance each detachment joins a new commander.\n'
            new_army = None
            for detachment in detachments:
                mutiny_roll = random.randint(1,20)
                if mutiny_roll == 20:
                    response['outcome'] += 'Mutiny Roll for {detachment.name} was 20, they remain in your army.\n'
                else:
                    response['outcome'] += f'Mutiny Roll for {detachment.name} was {mutiny_roll}, they joined a new army.\n'
                    if new_army == None:
                        new_army = Army.objects.create(name=f'new {commander.faction} army', bio=f'formed after mutiny in {army.name} lead by {commander.name}', owner=commander.faction, location=commander.location)
                    
                    detachment.army = new_army
                    detachment.save()

        elif response['morale_roll'] == 3:
            response['outcome'] += '3.	Mass desertion. Reduce the army\'s size and supplies by 30%. \n'
            for detachment in detachments:
                detachment.units = detachment.units*0.7
                detachment.non_combantants = detachment.non_combantants*0.7
                detachment.supplies = detachment.supplies*0.7
                detachment.save()
            
        if response['morale_roll'] == 4:
            response['outcome'] += '4. 1d6 random detachments defect to another army. \n'
            new_army = Army.objects.create(name=f'new {commander.faction} army', bio=f'formed after mutiny in {army.name} lead by {commander.name}', owner=commander.faction, location=commander.location)
            army_roll = random.randint(1,6)
            response['outcome'] += f'{army_roll} detachments leave your army \n'

            detachment_list = list(detachments.objects.all())
            leaving_detachments = random.sample(detachment_list, 3)
            for detachment in leaving_detachments:
                    response['outcome'] += f'{detachment.name} joined a new army.\n'
                    detachment.army = new_army
                    detachment.save()
            

        elif response['morale_roll'] == 5:
            response['outcome'] += '5. 	Major desertion. Reduce the army’s size and supplies by 20%. \n'
            for detachment in detachments:
                detachment.units = detachment.units*0.8
                detachment.non_combantants = detachment.non_combantants*0.8
                detachment.supplies = detachment.supplies*0.8
                detachment.save()


        elif response['morale_roll'] == 6:
            response['outcome'] += '6. Army splits in half. 3-in-6 chance each detachment joins a new commander.\n'
            new_army = None
            for detachment in detachments:
                mutiny_roll = random.randint(1,6)
                if mutiny_roll >= 4:
                    response['outcome'] += 'Mutiny Roll for {detachment.name} was {mutiny_roll}, they remain in your army.\n'
                else:
                    response['outcome'] += f'Mutiny Roll for {detachment.name} was {mutiny_roll}, they joined a new army.\n'
                    if new_army == None:
                        new_army = Army.objects.create(name=f'new {commander.faction} army', bio=f'formed after mutiny in {army.name} lead by {commander.name}', owner=commander.faction, location=commander.location)

                    detachment.army = new_army
                    detachment.save()

        elif response['morale_roll'] == 7:
            response['outcome'] += '7. Random detachment defects to another army.\n'
            new_army = Army.objects.create(name=f'new {commander.faction} army', bio=f'formed after mutiny in {army.name} lead by {commander.name}', owner=commander.faction, location=commander.location)
            detachment_list = list(detachments.objects.all())
            leaving_detachment = random.choice(detachment_list)
            response['outcome'] += f'{leaving_detachment.name} joined a new army.\n'
            leaving_detachment.army = new_army
            leaving_detachment.save()


        elif response['morale_roll'] == 8:
            response['outcome'] += '8. 	Desertion. Reduce the army’s size and supplies by 10%. \n'
            for detachment in detachments:
                detachment.units = detachment.units*0.9
                detachment.non_combantants = detachment.non_combantants*0.9
                detachment.supplies = detachment.supplies*0.9
                detachment.save()


        elif response['morale_roll'] == 9:
            response['outcome'] += '9. 1d6 random detachments depart from the main column for 2d6 days, then return.\n' #TODO: how to simulate this?
            


        elif response['morale_roll'] == 10:
            response['outcome'] += '10.	Camp followers. Army picks up an extra 5% noncombatants. \n' #TODO: how to simulate this?
            for detachment in detachments:
                detachment.non_combantants = detachment.non_combantants * 1.05
                detachment.save()

        elif response['morale_roll'] == 11:
            response['outcome'] += '11.	Random detachment departs from the main column for 2d6 days, then returns. \n' #TODO: how to simulate this?

        elif response['morale_roll'] == 12:   
            response['outcome'] += '12.	No consequences.\n'
            # 12.	No consequences. 

def ArmyOverview(commander=None, army= None): #One of these two can't be Null
    overview = {}
    if commander:
        army = commander.army_set.first()
    elif army:
        army = army
    else:
        return False

    overview['army'] = army.name

    detachment_set = army.detachment_set.all()
    overview['detachments'] = []        
    overview['capacity'] = army.carrying_weight
    overview['supplies'] = army.supplies
    overview['morale'] = army.morale
    overview['loot'] = army.loot
    overview['supplies_per_day'] = army.supplies_per_day

    army_comp = {}

    for detachment in detachment_set:
        overview['detachments'].append(detachment.__str__())
        
        if detachment.unittype in army_comp:
            army_comp[detachment.unittype] += detachment.units
        else:
            army_comp[detachment.unittype] = detachment.units
        
    overview['army_overview'] = ''
    {k: v for k, v in sorted(army_comp.items(), key=lambda item: item[1], reverse=True)}
    for regiment in army_comp:
            overview['army_overview'] += f' {regiment} {army_comp[regiment]}'

    overview['army_overview'] += f' NC {army.non_combantants} // {army.travel_length} miles \n' 
    return overview

def caculateRecruitment(faction, region, createArmy = False):
    """
       Used to calculate recruitement number in a region, if createArmy is set to True, instantly save the army to the database.
    """
    #  each hex in a region raises infantry equal to its settlement score. 
    #  In good country, a hex also raises cavalry equal to 25% its settlement score and constructs wagons equal to 5%. 
    #  Thus, a thickly-settled hex (80 settlement) could raise 80 soldiers, 20 cavalry, and 4 wagons. 
    #  After adding up the total infantry from all hexes in the region, round to the nearest 100 and use that to calculate the rest.

    hexes = region.hex_set.all()

    unit_types = Unittype.objects.filter(Q(unique_type=False) | Q(unique_type_faction_isnull=faction))
    
    new_army = Army(name=f"{Region} {faker.color_name()} new army", owner=faction)
    army = { k: Detachment(unittype=k, army=new_army, owner=faction) for k in unit_types }
    total_units = 0
    wagons = 0
    total_non_combatants = 0
    
    for hex in hexes:
        hex.settlement_score
        good_country = True #TODO: When is country not good?
        
        for detachtment in army:
                unit_type = detachtment.unittype_set.first()
                if good_country:
                    units = hex.settlement_score * unit_type.recruitement_rate_good_country
                else: 
                    units = hex.settlement_score * unit_type.recruitement_rate

                non_combatants = units * unit_type.default_non_combatant
                detachtment.units += units
                detachtment.non_combantants += non_combatants
                total_non_combatants += non_combatants
                total_units += units

        if good_country:
            wagons += hex.settlement_score*0.05 #Todo This should not be hard coded.
        
    #Spread wagons amongst detachtments 
    wagons_per_detachment = round(wagons/len(army))
    
    for detachment in army:
        detachment.units = round(detachment.units/100,0)*100 #Round unit amounts to nearest 100 units
        detachment.wagons = wagons_per_detachment
        detachment.supplies = detachment.carrying_weight

    #TODO: If a unique unit type present, substract the amount of unique units from their basic version recruitment numbers    
    # .delete() original detachment if 0 is present
    
    if createArmy:
        new_army.save()
        for detachment in army:
            detachment.save()
     
    else:
        return ArmyOverview(army=new_army)