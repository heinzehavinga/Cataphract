from django import forms


#TODO: disconnect battle logic to battles.py, it is probably a good idea to play out battle in the backend instead of api?
class CombatForm(forms.Form):
    battle_name = forms.CharField(label="Your name", max_length=100)
    # Positive: Numerical advantage: +1 per 100% more total soldiers. Cavalry count double. 
    # Morale: +1 per morale above resting. -1 per morale below resting.
    # Chosen battlefield: +1 
    # Surprise: +1 
    # Advantageous terrain: +1 Rough terrain: -1
    # Tactics: +0–3 Tactics: -0–3 (How do we make a decision about this?)
    # Undersupplied: -1 
    # Sick or exhausted: -1 #WHERE ARE THE RULES FOR THIS?
    #Bad weather: -1 
    # Out of formation (foraging, resting, etc.): -2

    
    #X forces, which can consist of Y commanders
    #Everybody rolls dice, highest roll wins the battle, but then you check against the next dice roll of opponent
    #Maybe write out and example
    
