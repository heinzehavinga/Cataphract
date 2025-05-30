from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from .serializers import CommanderSerializer
from .models import *
from .armies import *
import random

def index(request):
    return HttpResponse("Hello, world. You're at the cataphract index.")


class CommanderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commanders to be viewed or edited.
    """
    queryset = Commander.objects.all().order_by('-faction')
    serializer_class = CommanderSerializer
    permission_classes = [permissions.IsAuthenticated] 



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
       
        response = {'done':True}
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