from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from .serializers import CommanderSerializer
from django.db.models import Q
from .models import *
from .armies import *
from .orders import *
from .mapimage import *
import random, math
from datetime import datetime, timedelta

def index(request):
    return HttpResponse("Hello, world. You're at the cataphract index.")


class CommanderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commanders to be viewed or edited.
    """
    queryset = Commander.objects.all().order_by('-faction')
    serializer_class = CommanderSerializer
    permission_classes = [permissions.IsAuthenticated] 


class CommanderMap(APIView):
    def get(self, request, discordid, format=None):
        player = Player.objects.get(discord_id=discordid)
        commander = player.commander_set.first()
        army = commander.army_set.first() #TODO: Make this capable of not picking the wrong army if player has more armies (which shouldn't be a thing, but it probably will happen)
        #TODO turn this into an image
        response = moraleCheck(commander, army)

        return Response(response)


class MoraleCheck(APIView):
    """
    Make a morale check for the army

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication] #This might be something cool to look into

    def get(self, request, discordid, format=None):
        """
        Makes a morale check, applies the results, reports back the outcome
        """
        player = Player.objects.get(discord_id=discordid)
        commander = player.commander_set.first()
        army = commander.army_set.first() #TODO: Make this capable of not picking the wrong army if player has more armies (which shouldn't be a thing, but it probably will happen)
        response = moraleCheck(commander, army)

        return Response(response)


class Tick(APIView):
    """
    This is the big one, it moves everything forward 1 tick (simulates 4 hours)

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication] #This might be something cool to look into

    def get(self, request, format=None):
        """
        Move the game forward four hours.
        """
        world = World.first()
        now =  world.last_tick + timedelta(hours=world.tick_speed)
        
        world.last_tick = now
        world.save()
        
        #Set all armies to unharried

        #Check and apply all harried commands (is a harried command still given?)
        Army.all().update(harried=False)
        
        for order in Order.filter(order__gte=7, order__lte=9, date_end__gte=now, completed=False):
            
# A detachment may harry an army within scouting range. 

            source_army = order.commander.army_set.first()
            target_army = order.target_army_set.first()
            #Check if army is within distance
            
            source_army_loc = (source_army.location.x,source_army.location.y)
            target_army_loc = (target_army.location.x,target_army.location.y)
            
            if order.selected_detachment.scout_distance >= math.dist(source_army_loc, target_army_loc):
                order.commander.target_army_set.first().update(harried=True)
                order_harried(order)
            else:
                pass
            

            
            #
        
        Army.all().save()

        #Get all other orders 
        #Move orders
        # for order in Order.filter(order=1, date_end__gte= now, completed=False):
            # self.move(order)

        for order in Order.filter(order=2, date_end__gte = now, completed=False):
            self.rest(order)
        
        #Building check (we assume that siege)
        for order in Order.filter(order=3, date_end__gte = now, completed=False):
            self.build(order)
        
        for order in Order.filter(order=5, date_end__gte = now, completed=False):
            self.forage(order)

        for order in Order.filter(order=6, date_end__gte = now, completed=False):
            self.siege(order)
        
        for order in Order.filter(order=10, date_end__gte =now, completed=False):
            self.operations(order)

        #Time threshold order (only check when weeks is completed)
        #Rest, Seige

        #Fully complete orders (only check completed orders)
        #Recruit, 
        
        #If move order
        response = {'done':True}

        ##Construct a giant response object that the bot uses to keep user up to date about what's happening,
        #Recieve their maps image
        #Recieve messages
        #Recieve news 
        # also, open up channels with player that are on the same hex 
        return Response(response)
    
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
    
class Commandersheet(APIView):
    """
    Creates an army overview, format based on the example army shown in the rules.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication] #This might be something cool to look into
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, discordid, format=None):
        """
        Returns a Army Sheet.
        """
        response = {}
        player = Player.objects.get(discord_id=discordid)
        commander = player.commander_set.first()
        response['commander'] = commander.name
        response['relation'] = f"{commander.relation_name} of {commander.relation_commander}"
        response['traits'] = ','.join(Trait.objects.filter(owner__id=commander.id))
        f"{commander.relation_name} of {commander.relation_commander}"
        response['age'] = commander.age
        response['faction'] = commander.faction.name
        army = commander.army_set.first()
        response['army'] = army.name
        
        sheet = ArmyOverview(commander=commander)
        overview = response | sheet
        
        return Response(overview) 
    

class CalculateRecruit(APIView):
    """
    Creates an army overview, format based on the example army shown in the rules. 
    
    #TODO rules have changed! Now is calculated per location?
    #TODO This also changes how regions probably work, they should be mini regions with a strongholds?
    #TODO THis feel like a version that is easier for human calculation, but worse ingame? 

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication] #This might be something cool to look into
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, discordid, format=None):
        """
        Returns a calculation of what sort of army you would recruit.
        """
        response = {}
        player = Player.objects.get(discord_id=discordid)
        commander = player.commander_set.first()
        response['commander'] = commander.name
        response['age'] = commander.age
        response['faction'] = commander.faction.name
        location = commander.location
        region = location.region

        result = caculateRecruitment(commander.faction, region, False)
        print(result)
        return Response(result) 