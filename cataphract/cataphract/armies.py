#TODO: Add all the order logic in here please.
import random
from .models import *
from django.db.models import Q
from faker import Faker
import heapq
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
    overview['supplies_days_left'] = army.supplies_days_left
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

    unit_types = Unittype.objects.filter(Q(unique_type=False) | Q(unique_type_faction=faction))
    
    new_army = Army(name=f"{region.name} {faker.color_name()} new army", owner=faction)
    army = { k.name: Detachment(unittype=k, army=new_army) for k in unit_types }
    total_units = 0
    wagons = 0
    total_non_combatants = 0
    
    infantry_total = region.recruit_infantry
    
    good_country = True #TODO when is country good?
    
    wagons = 0
    if good_country:
        wagons = infantry_total*0.05 #Todo This should not be hard coded.
    wagons_per_detachment = round(wagons/len(army.values()))
    

    for detachtment in army:
        
        unit_type = army[detachtment].unittype
        
        if good_country:
            units = infantry_total * unit_type.recruitement_rate_good_country
        else: 
            units = infantry_total * unit_type.recruitement_rate

        non_combatants = units * unit_type.default_non_combatant
        army[detachtment].units = units
        army[detachtment].non_combantants += non_combatants
        total_non_combatants = non_combatants
        army[detachtment].wagons = wagons_per_detachment
        army[detachtment].supplies = army[detachtment].carrying_weight #Why do horses get more supplies?
        total_units += units

    #TODO: If a unique unit type present, substract the amount of unique units from their basic version recruitment numbers    
    # .delete() original detachment if 0 is present
    new_army.save()
    Detachment.objects.bulk_create(army.values())
    print(army) 
    
    sheet = ArmyOverview(army=new_army) 
    if createArmy == False:
        for detachment in new_army.detachment_set.all():
            print(detachment, detachment.supplies, detachment.carrying_weight)
            # unit = Detachment.objects.get(name=army[detachtment].name)
            detachment.delete() #TODO: Can we do this without saving and writing the army and detachments to the database?
        new_army.delete()
 
    return sheet


def hex_distance(start, destination):
    """Hex distance for axial coordinates."""
    return int((abs(start.x - destination.x) 
               + abs(start.x + destination.y - destination.y - destination.x) 
               + abs(start.y - start.x)) / 2)


def biased_astar(start, goal, bias = 1.2):
    """
    A* with bias for Hex map.
    bias > 1 increases pull towards goal (aggressive pathfinding).
    """
    open_set = []
    heapq.heappush(open_set, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    f_score = {start: hex_distance(start, goal) * bias}
    
    while open_set:
        _, current = heapq.heappop(open_set)
        
        if current == goal:
            # reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]
        
        for neighbor, move_cost in current.neighbors.items():
            tentative_g = g_score[current] + move_cost
            
            if tentative_g < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score[neighbor] = tentative_g + hex_distance(neighbor, goal) * bias
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
    
    return None  # no path found


#TODO: These result should be added to player message stack.
def gain_loot(army, amount, personal_loot):
    amount_left = amount

    if army.carrying_weight_left < amount:

        for detachtment in army.detachment_set.all():
            if personal_loot:
                if amount >= detachtment.units:
                    detachtment.morale += 1
                detachtment.loot += detachtment.carrying_weight_left
            else:    
                detachtment.personal_loot += detachtment.carrying_weight_left
            
            amount_left -= detachtment.carrying_weight_left
        return  amount_left
    #If not, spread randomly across detachments
    else:
        pass #How do spread randomly in a way that fits all detachments
    #TOOD: Don't forget to put morale bonus here
        return True
    
def lose_loot(army, loot):
    pass

def gain_supplies(army, amount):
    #is supplies to be gained, greater than capacity?
    #if so, just set everything to max.
    amount_left = amount

    if army.carrying_weight_left < amount:
        for detachtment in army.detachment_set.all():
            detachtment.supplies += detachtment.carrying_weight_left
            amount_left -= detachtment.carrying_weight_left
    
        return  amount_left
    #If not, spread randomly across detachments
    else:
        pass #How do spread randomly in a way that fits all detachments
        return True
    


def battle(armies):
    pass
#     When two or more hostile armies meet, the referee provides each commander with their current information and the lay of the land. Commanders draw up a brief plan of battle, then each roll 2d6, adding the follower modifiers:

# Positive:
# Numerical advantage: +1 per 100% more total soldiers. Cavalry count double. 
# Morale advantage: +1 per point of morale difference. 
# Chosen battlefield: +1
# Surprise: +1
# Advantageous terrain: +1
# Tactics: +0–3

# Negative:
# Rough terrain: -1
# Undersupplied: -1
# Sick or exhausted: -1
# Bad weather: -1
# Out of formation (foraging, resting, etc.): -2
# Tactics: -0–3

# The higher of the two rolls is the victor and achieves their objective; the loser does not. Then, compare rolls and apply the difference as result:
# 0.	Defender, if there is one, holds the objective. Attacker, if there is one, loses 1 morale. Both sides suffer 5% casualties.  
# 1.	Both sides suffer 10% casualties. Loser loses 1 morale. 
# 2–3.	Victor suffers 5% casualties, loser suffers 10% casualties. Loser loses 2 morale, victor gains 1.
# 4–5.	Victor suffers 5% casualties; loser suffers 15%. Loser loses 2 morale, victor gains 2. 1-in-6 chance loser commander captured.
# 6+.	Victor suffers 5% casualties; loser suffers 20%. Loser loses 2 morale, victor gains 2. 2-in-6 chance loser commander captured. 

# The losing army retreats 1 hex (or as appropriate), then checks morale. On a failure, it routs: lose 1d6 × 10% of your supplies, the army retreats a further 1d6 hexes away (as much time as that takes) out of control, then regroups. If retreat is impossible, reduce the army’s size and supplies by half, spend 1d6 days out of control, and stay in place. Lost supplies may be acquired by victorious commanders. 

# When more than two armies fight in battle, divide the armies into sides. Calculate each side’s total troop counts as if they were one army for numeric advantage bonuses, but apply separate individual bonuses for each army (including morale, tactics, commander traits, and so on). Each army makes its own battle roll, and the side with the highest single roll wins. 

# The winning side uses its highest single roll to determine morale consequences, but otherwise each army on each side compares its result to the highest result on the enemy side and suffers consequences accordingly. Thus, one side might win the day but suffer heavier casualties than their opponents, including possibly their armies routing or their commanders being captured. 


def lose_supplies(army, amount):
    # if army.supplies:
    # for detachtment in army.detachment_set.all():
    #     detachtment.supplies = detachtment.supplies - (detachtment.supplies *(amount/100))
    #     detachtment.save()
    #is supplies to be lost, greater than capacity?
    #if so, just set everything to 0.
    #If not, spread randomly across detachments
    pass

def lose_supplies_percentage(army, amount):
    for detachtment in army.detachment_set.all():
        detachtment.supplies = detachtment.supplies - (detachtment.supplies *(amount/100))
        detachtment.save()

def gain_units(army, amount):
    #is supplies to be gained, greater than capacity?
    #if so, just set everything to max.
    #If not, spread randomly across detachments
    pass

def lose_units_percentage(army, amount): #in percentage
    for detachtment in army.detachment_set.all():
        detachtment.units = detachtment.units - (detachtment.units *(amount/100))
        detachtment.save()



# ORDER LOGIC FOLLOWS HERE

def order_move(order):
    pass


def order_harrying(order):
    result = {'player':order.Commander.player.discord_id, 'Commander':order.Commander.name, 'order':order.order, 'outcome':'Unknown'}
# def When a detachment spends a day harrying, choose whether to focus on killing soldiers, torching supplies, or stealing loot and supplies. 

# By default, a detachment has a 2-in-6 chance of success: 
# Skirmishers add +1 to their roll (both the initial roll and the results). Cavalry add +2. 
    #TODO: include commander trait bonus
    if random.randint(1,6) + order.selected_detachment.harrier_bonus > 2:
    # Killing soldiers reduces enemy numbers by 20% of the harrying detachment’s numbers. 
        if order.order == 7:
            #TODO calc: way to reduce Army numbers:
            lost_soldiers = round(order.selected_detachment.units * 0.2)
            pass
            
        if order.order == 8:
    # Torching supplies reduces the enemy supplies by an amount equal to 2d6 × the harrying detachment’s numbers.
            #TODO: add way to lose supplies in army
            lost_supplies = (random.randint(1,6) + random.randint(1,6) + order.selected_detachment.harrier_bonus) * order.selected_detachment.units
            pass
        
    # Stealing loot or supplies captures loot or supplies equal to 1d6 × the harrying detachment’s numbers.
        if order.order == 9:
            looted_supplies = random.randint(1,6) + order.selected_detachment.harrier_bonus
            #TODO add way to lose supplies in army
            #TODO add way to gain supplies in army
            pass
        
        order.commander.army.save()
        order.target_army.save()
    
    else:
        order.selected_detachment.units = order.selected_detachment.units*0.8
        order.selected_detachment.save()

# On a failure, the harrying detachment suffers 20% losses and does not accomplish their objective. 
    return result
