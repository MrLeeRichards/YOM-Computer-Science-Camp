import random

class Character:
    def __init__(self, name, health, level):
        self.name = name
        self.health = health
        self.max_health = health
        self.level = level

        self.reliable_chance = 90
        self.reliable_crit = 2
        self.reliable_damage = 5

        self.heavy_chance = 60
        self.heavy_crit = 20
        self.heavy_damage = 10

        self.heal_min = 5
        self.heal_max = 50


class Monster:
    def __init__(self, name, damage, hit_chance, health):
        self.name = name
        self.damage = damage
        self.hit_chance = hit_chance
        self.health = health

def battle(character, monsters):
    while len(monsters) > 0 and character.health > 0:
        print("\n{} is at {} hp.".format(character.name, character.health))
        print("\nCurrently fighting:")

        index = 0
        for monster in monsters:
            print("   {}. {} {} hp".format(index, monster.name.ljust(20), monster.health))
            index += 1

        monster_number = int(input("\nWhich monster should {} attack? ".format(character.name)))

        print("""
{}'s Moves:
    1. Reliable Swing      {}% hit    {}% crit   {} damage
    2. Heavy Swing         {}% hit    {}% crit   {} damage
    3. Heal                {} to {} hp healed
    4. Dodge               half chance of being hit this turn
""".format(character.name, 
        character.reliable_chance, character.reliable_crit, character.reliable_damage,
        character.heavy_chance, character.heavy_crit, character.heavy_damage,
        character.heal_min, character.heal_max))

        move_number = int(input("Which move should {} make? ".format(character.name)))

        if move_number == 1:
            swing = random.randint(1, 100)

            if swing <= character.reliable_crit:
                monsters[monster_number].health -= 3 * character.reliable_damage
                print("{} critically hit {} for {} damage".format(character.name, monsters[monster_number].name, 3 * character.reliable_damage))
            elif swing <= character.reliable_chance:
                monsters[monster_number].health -= character.reliable_damage
                print("{} hit {} for {} damage".format(character.name, monsters[monster_number].name, character.reliable_damage))
            else:
                print("{} missed {}".format(character.name, monsters[monster_number].name))

        elif move_number == 2:
            swing = random.randint(1, 100)

            if swing <= character.heavy_crit:
                monsters[monster_number].health -= 3 * character.heavy_damage
                print("{} critically hit {} for {} damage".format(character.name, monsters[monster_number].name, 3 * character.heavy_damage))
            elif swing <= character.heavy_chance:
                monsters[monster_number].health -= character.heavy_damage
                print("{} hit {} for {} damage".format(character.name, monsters[monster_number].name, character.heavy_damage))
            else:
                print("{} missed {}".format(character.name, monsters[monster_number].name))

        elif move_number == 3:
            heal = random.randint(character.heal_min, character.heal_max)

            character.health = min(character.health + heal, character.max_health)

            print("{} healed for {} hp.".format(character.name, heal))

        dodging = move_number == 4

        if monsters[monster_number].health <= 0:
            print("{} defeated {}.".format(character.name, monsters[monster_number].name))
            del monsters[monster_number]

        if character.health > 0:
            for monster in monsters:
                swing = random.randint(1, 100)

                if swing <= monster.hit_chance / (2 if dodging else 1):
                    character.health -= monster.damage
                    print("{} hit {} for {} damage".format(monster.name, character.name, monster.damage))
                else:
                    print("{} missed {}".format(monster.name, character.name))

        else:
            print("{} has been defeated.".format(character.name))
            print("\nGame Over")
            exit()


print("""
Welcome to TextQuest. You, like so many before you,
have set out to rescue the beautiful dragon from the
terrible princess. Armed (somewhat short-sightedly), with a wooden sword
and nothing else, you have made your way to the entrance
of the dreaded Castle More-dread. No, the writing does not
get better from here.
""")


name = input("So, what's your hero's name? ")
character = Character(name, 100, 1)

print(character.name + """? That's what you're going with?
Well, it's your character.

Anyway, you enter the Castle, and are immediately accosted by
by three slimes.
====================
""")

battle(character, [Monster("Green Slime", 2, 75, 10), Monster("Blue Slime", 2, 75, 10), Monster("Red Slime", 2, 75, 10)])

print("""
====================
You defeated the slimes. You proceed further into the dungeons of
Castle More-dread. You note the suspiciously large cobwebs on the
walls, thinking to yourself, "Mmm... Don't like that."

Not long after, you are attacked by a slightly too big spider.
====================
""")

battle(character, [Monster("Slightly Too Big Spider", 10, 80, 30)])

print("""
====================
Having disposed of the spider, you procede deeper still, and come upon
a small yellow and black sign.

"Under construction"

You can't procede further until someone adds more to the dungeon.
""")