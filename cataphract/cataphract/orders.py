from .helpers import *
import random, math
from .models import *
from .armies import moraleCheck
from datetime import datetime, timedelta

def order_tick():
    #Set all armies to unharried
    #Check and apply all harried commands (is a harried command still given?)
        world = World.first()
        now =  world.last_tick + timedelta(hours=world.tick_speed)
        Army.all().update(harried=False)
        
        for order in Order.filter(order__gte=7, order__lte=9, date_end__gte=now, completed=False):
            
            # A detachment may harry an army within scouting range. 
            source_army = order.commander.army_set.first()
            target_army = order.target_army_set.first()
            #Check if army is within distance
            
            if order.selected_detachment.scout_distance >= calc_distance_hexes(source_army.location.x,source_army.location.y,target_army.location.x,target_army.location.y):
                order.commander.target_army_set.first().update(harried=True)
                if order.order == 7:
                    h_kill(order)
                    
                elif order.oder == 8:
                    h_torch(order)
                
                elif order.order == 9:
                    h_loot(order)            

        
        Army.all().save()
        
        #Get all other orders 
        #Move orders
        for order in Order.filter(order=1, date_end__gte= now, completed=False):
            move(order)

        for order in Order.filter(order=2, date_end__gte = now, completed=False):
            rest(order)
        
        #Building check (we assume that siege)
        for order in Order.filter(order=3, date_end__gte = now, completed=False):
            build(order)
        
        for order in Order.filter(order=5, date_end__gte = now, completed=False):
            forage(order)

        for order in Order.filter(order=6, date_end__gte = now, completed=False):
            siege(order)
        
        for order in Order.filter(order=10, date_end__gte =now, completed=False):
            operations(order)

def move():
    #is Army same location as other army that is from different faction? Notify referee to see if they are letting each other pass, make the ref move them manually
    #Is end location reached? No, let's travel further
    #Is end location is reached, delete order. Notify Referee and Commander, order is complete
    return True

def build():
    #If end time is reached, add Siege engines
    #Otherwise just pass
    return True

def forage():
    
    #Takes a full day
    #if completed

    return True

def rest(order):
    #If new week is reached add 1 morale to army (or eeach )
    #If rest time is completed
    return True

def siege(order):
    #If new week is reached reduce 1 morale to sieged city
    return True

def h_kill(order):
    return True

def h_torch(order):
    return True

def h_loot(order):
    return True

def operations(order):
    return True
