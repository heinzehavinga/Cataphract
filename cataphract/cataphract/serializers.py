from rest_framework import serializers
from .models import Commander

# Serializers define the API representation. 
class CommanderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Commander
        fields = ['name']

