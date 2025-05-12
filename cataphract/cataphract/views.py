from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from .serializers import CommanderSerializer
from .models import *


def index(request):
    return HttpResponse("Hello, world. You're at the cataphract index.")


class CommanderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commanders to be viewed or edited.
    """
    queryset = Commander.objects.all().order_by('-faction')
    serializer_class = CommanderSerializer
    permission_classes = [permissions.IsAuthenticated] 


class Commandersheet(APIView):
    """
    View to list all users in the system.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    # authentication_classes = [authentication.TokenAuthentication] #This might be something cool to look into
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, discordid, format=None):
        """
        Return a Army Sheet.
        """

#         Commander: Knyazina Kvetoslava “the Whisperer”
# Ivanovna Vronskaya (33, Siege Engineer)
# Infantry 4,600 Cavalry 600 Wagons 25 NC 1,300 // 2 miles

# Morale 9/9,

# Supplies 105,000/146,000,

# Supplies/day 12,150
# Detachments:

# 1st Vortoszol Heavy Infantry “The Terror of Amara” 800, 10 wagons
# 2nd Vortoszol Infantry 800, 10 wagons
# 3rd Vortoszol Infantry 800, 5 wagons
# 1st Zllatar Heavy Infantry 800
# 1st Baranovo Infantry 800
# 1st Mirsk Skirmishers 600
# 1st Vortoszol Heavy Cavalry “The Ironshod” 200
# 2nd Vortoszol Cavalry 200
# 1st Zllatar Cavalry 200
        
        print(discordid)
        response = {}
        commander = Commander.objects.get(pk=1) #TODO connect this to Discord user in query
        response['commander'] = commander.name
        response['age'] = commander.age
        response['faction'] = commander.faction.name
        army = commander.army_set.first()
        response['army'] = army.name
        
        detachment_set = army.detachment_set.all()
        response['detachments'] = []
        response['army_length'] = 0
        
        morale = 0
        response['capacity'] = 0
        response['supplies'] = 0
        response['loot'] = 0
        response['supplies_per_day'] = 0
        for detachment in detachment_set:
            response['detachments'].append(detachment.__str__())
            morale += detachment.morale
            response['supplies'] += detachment.supplies
            response['loot'] += detachment.loot
            response['supplies_per_day'] += detachment.units * detachment.unittype.supplies_per_day
            response['capacity'] += detachment.unittype.carry_weight
            response['capacity'] += detachment.wagons * 500 #TODO: don't hardcode carry capacity wagons
            response['capacity'] += detachment.non_combantants * 15 #TODO: don't hardcode carry capacity non combatants
            
            response['army_length'] += detachment.units/detachment.unittype.units_per_mile
            response['army_length'] += detachment.wagons/50 #TODO: don't hardcode amount of wagons per mile
            response['army_length'] += detachment.non_combantants/5000 #TODO: don't hardcode amount of non combatents per mile
        
        response['morale'] = morale/len(response['detachments'])

        print(response)
        
        return Response(response)