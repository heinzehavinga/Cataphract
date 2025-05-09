from django.http import HttpResponse
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CommanderSerializer
from .models import Commander


def index(request):
    return HttpResponse("Hello, world. You're at the cataphract index.")


class CommanderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows commanders to be viewed or edited.
    """
    queryset = Commander.objects.all().order_by('-faction')
    serializer_class = CommanderSerializer
    permission_classes = [permissions.IsAuthenticated] 
