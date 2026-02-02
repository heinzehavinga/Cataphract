from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r'commanders', views.CommanderViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("calculaterecruit/<int:discordid>", views.CalculateRecruit.as_view()),
    path("commandersheet/<int:discordid>", views.Commandersheet.as_view()),
    path("actions/sendMessage/", views.SendMessage.as_view()),
    path("actions/transferSupplies/", views.TransferSupplies.as_view()),
    path("actions/transferWagons/", views.TransferWagons.as_view()),
    path("actions/transferDetachment/", views.TransferDetachments.as_view()),
    path("mapimage/<int:discordid>", views.CommanderMap.as_view()), #TODO: this shouldn't be connected to discord id but to player id (how do we do this?), ALSO THIS SHOULD BE AN AUTHED CALL!
    path("moralecheck/<int:discordid>", views.MoraleCheck.as_view()), #TODO: Referee should only be able to make this call about an army
    path("tick/", views.Tick.as_view()),
    path("api/", include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]