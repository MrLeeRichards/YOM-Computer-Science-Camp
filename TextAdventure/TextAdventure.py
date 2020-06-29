import random

class Monster:
    def __init__(self, name, damage, hit_chance, xp):
        self.name = name
        self.damage = damage
        self.hit_chance = hit_chance
        self.xp = xp

print("""
Welcome to TextQuest. You, like so many before you,
have set out to rescue the beautiful dragon from the
terrible princess. Armed (somewhat short-sidedly), with a wooden sword
and nothing else, you have made your way to the entrance
of the dreaded Castle More-dread. No, the writing does not
get better from here.
""")

character = object()
character.name = input("So, what's your hero's name? ")
character.gold = 100
character.inventory = [Weapon("Wooden Sword", 5)]
character.equipped = 0 #Number of the inventory slot for the currently equipped weapon

print(character.name + """? That's what you're going with?
Well, it's your character.
""")

