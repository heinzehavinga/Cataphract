from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from .serializers import CommanderSerializer
from django.db.models import Q
from .models import *
from .armies import *
from .orders import order_tick
from .mapimage import *
from .helpers import *
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
     
    """
    Sends back the currect Commandeer back.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, discordid, format=None):
        player = Player.objects.get(discord_id=discordid) #TODO: make sure the Discordbots already gets the Commander instead 
        commander = player.commander_set.first()
        army = commander.army_set.first() #TODO: Make this capable of not picking the wrong army if a commander has more armies (which shouldn't be a thing, but it probably will happen)
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
        
        
        #Updates the status of all the ongoing orders.
        order_tick()

        response = {}

        #Add all mapimage URL's and army sheets
        response['armies'] = []
        for army in Army.all():
            armystatus = {}
            armystatus['imageurl'] = "placeholder.jpg"
            response['armies'].append(armystatus)
        
        #Add all commander that reside on the same space
        response['channelsopen'] = []


        ##Construct a giant response object that the bot uses to keep user up to date about what's happening,
        #Recieve their maps image
        #Recieve messages
        #Recieve news 
        # also, open up channels with player that are on the same hex 
        return Response(response)
    
 
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
        response['relation'] = ""
        if commander.relation_name is not None:
            response['relation'] = f"{commander.relation_name} of {commander.relation_commander}"
        
        response['traits'] = ""
        for trait in Trait.objects.filter(owners=commander):
                response['traits'] += trait.__str__()

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
    
class SendMessage(APIView):
    """
    Sends a message to another player
    
    * Requires token authentication.
    """
    # authentication_classes = [authentication.TokenAuthentication] #This might be something cool to look into
    
    def post(self, request, format=None):
        # transfer_data = request.data
        # #Is this a legal transfer, as in are both commanders in the same hex?
        # transfer_data.recieving_commander
        message = playerMessage()
        return True
        



class TransferSupplies(APIView):
    def post(self, request, format=None):
        #Is this a legal transfer, as in are both commanders in the same hex?
        #TODO: How to 
        return True

class TransferWagons(APIView):
    def post(self, request, format=None):
        #Is this a legal transfer, as in are both commanders in the same hex?
        return True

class  TransferDetachments(APIView):
    def post(self, request, format=None):
        
        # transfer_data = request.data
        # #Is this a legal transfer, as in are both commanders in the same hex?
        # transfer_data.recieving_commander
        # new_army = Commander.filter(__name__=transfer_data.recieving_commander)
        # detachment.army = new_army
        # detachment.save()
        
        return True
    
