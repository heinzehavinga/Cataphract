from django.contrib import admin
from .models import Unittype, Strongholdtype, Faction, Region, Hex, Commander, Strongholds, Army, Detachment, Order

admin.site.register(Unittype)
admin.site.register(Strongholdtype)
admin.site.register(Faction)
admin.site.register(Region)
admin.site.register(Hex)
admin.site.register(Commander)
admin.site.register(Strongholds)
admin.site.register(Army)
admin.site.register(Detachment)
admin.site.register(Order)


# Register your models here.
