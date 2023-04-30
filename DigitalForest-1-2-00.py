# DIGITAL FOREST 
# Text Based Adventure Game
# By Zach White
# Player must install Python and Pandas to play

import time
import os
from tracemalloc import start
import pandas as pd

class Player:
    health = 100
    unlimited_health = False
    unlimited_ammo = False
    inventory = pd.DataFrame([["phone", 0, 1, 0.0, 0.0, 0]], columns = ["item", "charge", "amount", "damage", "bonus_damage", "health"])
    inventory_lst = []
    agility = 10
    equipped_item = "none"


class Aquire:
    def item(add_item, item_name):
        update_inventory_lst()
        if Player.inventory[Player.inventory.item.isin([item_name])]:
            add_item_index = Player.inventory.index[Player.inventory["item"] == item_name]
            Player.inventory.loc[add_item_index[0], "amount"] += 1
            print("        "+ item_name + " ITEM AQUIRED")
        else:
            Player.inventory = Player.inventory.append(add_item, ignore_index = True)
            print("        "+ item_name + " ITEM AQUIRED")


class HealthBoost:
    health_25_index = Player.inventory.index[Player.inventory["item"] == "health_boost_25"]
    health_full_index = Player.inventory.index[Player.inventory["item"] == "health_boost_full"]

    def use_health_boost(boost_by):
        Player.equipped_item = "none"
        update_inventory_lst()

        if boost_by == "health_boost_25":
            if Player.health >= 75:
                Player.health = 100
                Player.inventory.loc[HealthBoost.health_25_index[0], "amount"] -= 1
                if Player.inventory.loc[HealthBoost.health_25_index[0], "amount"] == 0:
                    Player.inventory.drop([HealthBoost.health_25_index[0]], axis = 0, inplace = True)
            else:
                Player.health += 25
                Player.inventory.loc[HealthBoost.health_25_index[0], "amount"] -= 1
                if Player.inventory.loc[HealthBoost.health_25_index[0], "amount"] == 0:
                    Player.inventory.drop([HealthBoost.health_25_index[0]], axis = 0, inplace = True)
        else:
            Player.health = 100
            Player.inventory.loc[HealthBoost.health_full_index[0], "amount"] -= 1
            if Player.inventory.loc[HealthBoost.health_full_index[0], "amount"] == 0:
                Player.inventory.drop([HealthBoost.health_full_index[0]], axis = 0, inplace = True)


class Menus:
    def item(current_location):
        update_inventory_lst()
        done = False
        print(Player.inventory)
        print("\ncurrently equipped:", Player.equipped_item)
        print("\n        would you like to equip an item? y or n or help\n")

        answer = input(">").lower()

        while done == False:
            if answer == "y":
                Menus.item_select(current_location)
            elif answer == "n":
                done = True
                current_location()
            elif answer == "help":
                Menus.help_warning(current_location)
            else:
                done = False
                print("\n        That isn't an option.\n")
                answer = input(">").lower()
    
    def item_select(current_location):
        done = False
        print("\nType the name of the item you would like to equip as it is displayed...\n")

        answer = input("ITEM MENU >").lower()

        while done == False:
            if answer in Player.inventory_lst:
                Player.equipped_item = answer
                print("\n          ", answer, "equipped")
                if (answer == "health_boost_25") or (answer == "health_boost_full"): 
                    print("\n          USING HEALTH BOOST")
                    HealthBoost.use_health_boost(answer)
                    time.sleep(1)
                    print("\n\n          EXITING MENU\n")
                    current_location()
                else:
                    time.sleep(1)
                    print("\n\n           EXITING MENU\n")
                    answer = True
                    time.sleep(2)
                    current_location()
            else:
                print("\n        That isn't an option.\n")
                answer = input("ITEM MENU >").lower()

    def help_warning(current_location):
        print("""
    The following will take away some of the games difficulty. 
    Type CONTINUE and press enter to view the help text. 
    Type END and press enter to exit.
    """)

        answer = input(">").lower()

        if answer == "end":
            current_location()
        elif answer == "continue":
            Menus.help(current_location)
        else:
            print("\n        This is not an option.\n")
            answer = input(">").lower()

    def help(current_location):
        print("""
    WELCOME THIS SECTION WILL TEACH YOU SOME TRICKS ABOUT THE GAME:

    Most answers should be one lower case word unless they're directions then you can just use the direction letter like l for Left or n for North.
    Sometimes you can use a word and a letter or two letters. 
    When your are fighting an enemy, you can type SHOOT HN and your equiped weapon will fire a Head shot North.
    If an enemy is to the North and you have a weapon equipped this will shoot the enemy.
    You can check if you have an equipped item by typing ITEMS this will show your items and tell you what is equipped. 
    There is a chance you will miss, it depends on the enemies agility and your agility. 
    To shoot an enemy in a more general direction type something like SHOOT E.
    This will shoot towards the East and will, usually, deal damage to an enemy.

    The game will only accept input when you see this
    >

    A players stats can be accessed by typing one of two commands health or agility.
    A players agility will go up as you progress through the game, however if you die it will start back at 10.

    Most weapons need to be charged, when items are displayed, they will be in a table. 
    The table will give you information about items and the number of each item you are carrying.    
    There is one place to charge items in the Digital Forest but be careful you will need a sepcial item to control the charging area.
    If you dont have that item your health will drain as your items charge.
    If you are not careful this will kill you.

    To equip an item type ITEMS, the item menu will be displayed and will ask if you would like to equip an item. 
    From here you can type Y to equip an item or N to go back to the game.
    If you type Y, to equip an item you will need to type the item as it is displayed, for example if the item is called 
    
    health_boost_25 
    
    you will need to type it just like that, underscores and all.
    When you equip a health item the item will be used right away even if your health is full. 
    Your max health can only be 100.

    The phone in the hospital is your friend. Using extentions you can load checkpoints, see maps and even get items.

    To exit this section type anything and press enter and you will go back to the location you were in before you opened the items menu.
    """)
        answer = input(">").lower()

        if answer == "end":
            current_location()
        else:
            current_location()
            


class Enemey:
    pass

# Play Again Text
def play_again():
    print("\nDo you wnat to play again (y or n)")

    answer = input(">").lower()

    if "y" in answer:
        start()
    else:
        exit()

# Variables and Game Functions

trifoliate = False

def update_inventory_lst():
    Player.inventory_lst = []

    for i in Player.inventory["item"]:
        if i not in Player.inventory_lst:
            Player.inventory_lst.append(i)
    #print(Player.inventory_lst)
            

# Items

#NGHT PSTL
#nght_gun = Item("NGHT PSTL", 0)
nght_gun_count = 0
nght_gun_damage_head = 50
nght_gun_damage_body = 35

# HEALTH BOOSTERS
# health_boost_25_count = 0
# health_boost_heal_25 = 25
health_boost_25 = {"item": "health_boost_full", "charge": 0, "amount": 1, "damage": 0.0, "bonus_damage": 0.0, "health": 25}
# health_boost_full_count = 0
# health_boost_heal_full = 100
health_boost_full = {"item": "health_boost_full", "charge": 0, "amount": 1, "damage": 0.0, "bonus_damage": 0.0, "health": 100}

# DIGITAL 22
#digital_22 = Item("Digital 22", 0)
digital_22_count = 0
digital_22_damage_head = 50
digital_22_damage_body = 25

# SMRT PSTL
#smrt_pstl = Item("SMRT PSTL", 0)
smrt_pstl_count = 0
smrt_pstl_damage_head = 20
smrt_pstl_damage_body = 15

# Puzzles
# Puzzle 1
holding_ball1 = False
ball1_status = False
holding_ball2 = False
ball2_status = False
holding_ball3 = False
ball3_status = False
puzzle1_balls = 0


# Game Over Text
def game_over(reason):
    print("\n" + reason)
    print("Game Over!")
    play_again()


# Right Door -----------------------------------------------------------------------------------------------------------------------------------------------------------

# Puzzle 1
def maze_one_structure():
    print("""

       ___           ___           ___                    ___           ___           ___           ___           ___           ___           ___           ___           ___     
      /\  \         /\__\         /\  \                  /\  \         /\  \         /\  \         /\__\         /\  \         /\  \         /\__\         /\  \         /\  \    
      \:\  \       /:/  /        /::\  \                /::\  \        \:\  \       /::\  \       /:/  /        /::\  \        \:\  \       /:/  /        /::\  \       /::\  \   
       \:\  \     /:/__/        /:/\:\  \              /:/\ \  \        \:\  \     /:/\:\  \     /:/  /        /:/\:\  \        \:\  \     /:/  /        /:/\:\  \     /:/\:\  \  
       /::\  \   /::\  \ ___   /::\~\:\  \            _\:\~\ \  \       /::\  \   /::\~\:\  \   /:/  /  ___   /:/  \:\  \       /::\  \   /:/  /  ___   /::\~\:\  \   /::\~\:\  \ 
      /:/\:\__\ /:/\:\  /\__\ /:/\:\ \:\__\          /\ \:\ \ \__\     /:/\:\__\ /:/\:\ \:\__\ /:/__/  /\__\ /:/__/ \:\__\     /:/\:\__\ /:/__/  /\__\ /:/\:\ \:\__\ /:/\:\ \:\__:
     /:/  \/__/ \/__\:\/:/  / \:\~\:\ \/__/          \:\ \:\ \/__/    /:/  \/__/ \/_|::\/:/  / \:\  \ /:/  / \:\  \  \/__/    /:/  \/__/ \:\  \ /:/  / \/_|::\/:/  / \:\~\:\ \/__/
    /:/  /           \::/  /   \:\ \:\__\             \:\ \:\__\     /:/  /         |:|::/  /   \:\  /:/  /   \:\  \         /:/  /       \:\  /:/  /     |:|::/  /   \:\ \:\__\  
    \/__/            /:/  /     \:\ \/__/              \:\/:/  /     \/__/          |:|\/__/     \:\/:/  /     \:\  \        \/__/         \:\/:/  /      |:|\/__/     \:\ \/__/  
                    /:/  /       \:\__\                 \::/  /                     |:|  |        \::/  /       \:\__\                      \::/  /       |:|  |        \:\__\    
                    \/__/         \/__/                  \/__/                       \|__|         \/__/         \/__/                       \/__/         \|__|         \/__/    

    """)
    time.sleep(2)
    print("\nYou've entered THE STRUCTURE the opening that was once behind you instantly closed off.\nThe only direction you can go here is West. So you head West.")
    puzzle1_intersection1()

def puzzle1_start():
    print("\n\nYou are back at the start of the structure.")
    time.sleep(2)
    print("\n\n    What would you like to do?")

    answer = input(">").lower()

    while answer != "w":
        if answer == "w":
            puzzle1_intersection1()
        else:
            print("That is not an option.")

def puzzle1_north1():
    pass

def puzzle1_intersection1():
    print("\n\nYou approch an intersection you can go West, head back East, or you can go North.")
    time.sleep(2)
    print("    What would you like to do?")

    answer = input(">").lower()

    while (answer != "w") or (answer != "e") or (answer != "n"):
        if answer == "hint":
            print("Look at the capatalized Letters.")
            answer = input(">").lower()
        elif answer == "items":
            print(Player.inventory)
            answer = input(">").lower()
        elif answer == "look":
            print("You are at an intersection you can go West, head back East, or go North.")
        elif answer == "health":
            print("health:", Player.health)
            answer = input(">").lower()
        elif answer == "e":
            puzzle1_start()
        elif answer == "n":
            puzzle1_north1()
        elif answer == "w":
            puzzle1_west1_ball1()
        else:
            print("That is not an option.\n")
            answer = input(">").lower()

def puzzle1_west1_ball1():
    print("""
    Heading West...
    """)

    if (holding_ball1 == False) and (ball1_status == False):
        print("""
    You've reached a dead end. There is a sphere floating in front of you.    
        """)
        puzzle1_west1()
    elif (holding_ball1 == True) or (ball1_status == True):
        print("""
        You've reached a dead end there is nothing here for you. 
        You turn around.
        """)
        puzzle1_intersection1()
    
        
def puzzle1_west1():
    
    print("""
        What would you like to do?
    """)
    answer = input(">").lower()

    while answer != "collect":
            
        if (answer == "back"):
            print("You head back East...")
            puzzle1_intersection1()
        elif answer == "e":
            print("You head back East...")
            puzzle1_intersection1()
        elif answer == "hint":
            print("""
            The Sphere. 
            """)
            answer = input(">").lower()
        elif answer == "items":
            print(Player.inventory)
            answer = input(">").lower()
        elif answer == "look":
            print("""
    There is a sphere floating in front of you. Above the sphere on the wall is engraved...
        
        dPPPb8  dPPYb  88     88     888888  dPPPb8 888888 
       dP   `` dP   Yb 88     88     88__   dP   ``   88   
       Yb      Yb   dP 88     88     88``   Yb        88   
        YboodP  YbodP  88ood8 88ood8 888888  YboodP   88   
        """)
            answer = input(">").lower()
        elif answer == "health":
            print("health:", Player.health)
            answer = input(">").lower()
        else:
            print("That is not an option.\n")
            answer = input(">").lower()
    if answer == "collect":
        holding_ball1 = True
        print("""
    You take the sphere, it is heavier than expected but can be held in one arm, and made of some sort of cool metal. The sphere has a pattern on it...
        
        dPPPb8  dPPYb
        
        You head back to the intersection with the sphere.
        """)
        puzzle1_intersection1()
        

# Puzzle 1 ^^^^^^^^^^^^^^^^^^^^^^


def path_ahead():
    print("""
After following the path for some time you approach large cylindrical structure.
You walk up to it. Would you like to ENTER or go BACK?
""")

    answer = input(">").lower()

    if answer == "enter":
        maze_one_structure()
    elif answer == "back":
        digital_forest()
    elif answer == "hint":
        print("        Look at the capatalized words.\n")
        answer = input(">").lower()
    elif answer == "items":
        print(Player.inventory)
        answer = input(">").lower()
    elif answer == "look":
        print("Theres a large cylindrical structure in front of you.")
    elif answer == "health":
        print("health:", Player.health)
        answer = input(">").lower()
    else:
        print("That is not an option.\n")
        answer = input(">").lower()


def left_side_of_the_forest():
    print("\n    Your are in the left side of the forest walking...")

def right_side_of_the_forest():
    print("\n    your are in the right side of the forest walking the ground feels damp")

def trees1():
    print("\n\nWould you like to go Left or Right through the trees?\n")

    answer = input(">").lower()

    while answer.lower() != "l" or "r":
        if answer == "l":
            left_side_of_the_forest()
        elif answer == "r":
            right_side_of_the_forest()
        elif answer == "back":
            digital_forest()
        else:
            print("        That isn't an option.")
            answer = input(">").lower()


# Right Door Room 1
def digital_forest():
    print("\n    You are in a dark forest...")
    time.sleep(2)
    print("\n\n      There are gigantic TREES all around you and there is a PATH ahead.") 
    time.sleep(2)
    print("\n\n        What do you do?\n")

    answer = input(">").lower()
    
    while answer.lower() != "path":
        if answer == "trees":
            trees1()
        elif answer == "look": 
            print("\nThere are gigantic TREES all around you and there is a PATH ahead.")
            answer = input(">").lower()
        elif answer == "items":
            print(Player.inventory)
            answer = input(">").lower()
        elif answer == "hint":
            print("Take a LOOK at the capitalized words, pick one, they wont always be here to help you.")
            answer = input(">").lower()
        elif answer == "health":
            print("health: ", Player.health)
            answer = input(">").lower()
        else: 
            print("\n\nThat isn't an option.")
            answer = input(">")
    
    if answer == "path":
        print("\nYou take the path ahead.")
        path_ahead()

# End Right Door ----------------------------------------------------------------------------------

# Check Point System
def checkpoint_system():
    print("ENTER CHECKPOINT CODE")
    checkpoint_code = input("CHECKPOINT>").lower()

    if checkpoint_code == "the structure":
        maze_one_structure()
    else:
        begin_game()

# Left Door ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

def white_room():
    print("\n    You are in a white room.")
    time.sleep(2)
    print("""

,---------------------------------------.---------.    
|                                       |         |    
|    ,-----------------------------.    |    .    |    
|    |                             |    |    |    |    
|    |    ,-------------------.    |    |    |    |    
|    |    |                   |    |    |    |    |    
|    |    `----     ,----     |    |    |    |    |    
|    |              | X       |    |    |    |    |    
|    |    ,-------------------:    |    `----'    |    
|    |    |                   |    |              |    
|    `----:    ,---------.    |    `---------.    |    
|         |    |         |    |              |    |    
|    .    |    |    .    |    |     ---------'    |    
|    |    |    |    |    |    |                   |    
:----'    |    |    |    |    |    ,--------------:    
|         |    |    |    |    |    |              |    
|    .    |    `----'    |    |    |     ----.    |    
|    |    |              |    |    |         |    |    
|    `----"---------     |    |    `---------'    |    
|                        |    |                   |    
`------------------------'    `-------------------'
    """)
    time.sleep(1)
    print("\n                  REMEMBER ME?")
    time.sleep(3)
    print("THIS ROOM IS UN$TA8L3")
    time.sleep(1)
    print("THIS ROOM IS UNSTABLE")
    for i in range(1, 60):
        print("TH|S R00M |Z UN$TAB&73  TH|S R00M |Z UN$TAB&73  *$Hdhjfe48$@@9fdshj  TH|S R00M |Z UN$TAB&73 TH3 WH|T3 R000M R0oM R8M RQQM R00W TH|S R00M |Z UN$TAB&73  TH|S R00M |Z UN$TAB&73  *$Hdhjfe48$@@9fdshj  TH|S R00M |Z UN$TAB&73 TH3 WH|T3 R000M R0oM R8M RQQM R00W TH|S R00M |Z UN$TAB&73  TH|S R00M |Z UN$TAB&73  *$Hdhjfe48$@@9fdshj  TH|S R00M |Z UN$TAB&73 TH3 WH|T3 R000M R0oM R8M RQQM R00W ")
        time.sleep(0.3)
        print("01000100 01001001 01000111 01001001 01010100 01000001 01001100 00100000 01000110 01001111 01010010 01000101 01010011 01010100 01000100 01001001 01000111 01001001 01010100 01000001 01001100 00100000 01000110 01001111 01010010 01000101 01010011 01010100 01000100 01001001 01000111 01001001 01010100 01000001 01001100 00100000 01000110 01001111 01010010 01000101 01010011 01010100 ")
        time.sleep(0.1)
    time.sleep(1)
    print("88888888888")
    time.sleep(1)
    print("REBOOTING...")
    time.sleep(4)
    start()


# def weapon_selection_phone_order():
#     print("\n    Enter an item.\n")
#     answer = input(">").lower()
#     global health_boost_25_count
#     global digital_22_count
#     global smrt_pstl_count
#     if (answer == "health boost 25") and (health_boost_25_count <= 3):
#         players_items.update(health_boost_25) 
#         health_boost_25_count += 1
#         hospital_lobby()
#     elif (answer == "digital 22") and (digital_22_count != 1):
#         players_items.update(digital_22)
#         digital_22_count += 1
#         hospital_lobby()
#     elif (answer == "smrt pstl") and (smrt_pstl_count != 1):
#         players_items.update(smrt_pstl)
#         smrt_pstl_count += 1
#         hospital_lobby()
#     else:
#         hospital_lobby()
    
    

def reception_phone():
    print("    *type END to hang up*")

    answer = input("EXT: ").lower()

    if answer == "888888888888":
        checkpoint_system()
    #elif answer == "weapons":
    #    weapon_selection_phone_order()
    elif answer == "8b":
        print("        *ring* *ring* *ring*")
        time.sleep(2)
        print("        *click* *click* *click* *click*")
        hospital_lobby()
    elif answer == "hint":
        print("        From the top of the FOREST everything is an extention.")
        answer = input("EXT: ").lower()
    elif answer == "88888888888":
        white_room()
    # elif answer == ",ad8888ba,":
    #     players_items.update(nght_gun)
    #     print("    NGHT PSTL AQUIRED: ")
    #     time.sleep(1)
    #     print("    CHARGE: 0%")
    #     time.sleep(1)
    #     print("    WEAPON TYPE: GUN")
    #     time.sleep(1)
    #     print("    DAMAGE: 25%")
    #     time.sleep(2)
    #     print("    REBOOTING...")
    #     time.sleep(2)
    #     begin_game()
    elif answer == "88888888ba":
        print("""
        5 8 13 3 24 14 20 17 18 4 11 5 
        5 8 13 3 24 14 20 17 18 4 11 5 
        5 8 13 3 24 14 20 17 18 4 11 5 
        5 8 13 3 24 14 20 17 18 4 11 5 
        5 8 13 3 24 14 20 17 18 4 11 5 
        5 8 13 3 24 14 20 17 18 4 11 5 
        5 8 13 3 24 14 20 17 18 4 11 5 
        5 8 13 3 24 14 20 17 18 4 11 5 
         D    E   EC E   O     DE   E
        """)
    elif answer == "ad88888ba":
        print("""
              HOSPITAL FLOOR 1
,---------------------------------------.---------.
|     |                |           |              |
|     |                |           |              |
|     |                |           |              |
|     |                |           |              |    
|    ,-------------  --------  -----              |    
|    |                             |              |    
|    |    ,-------------------.    |              |    
|    |    | E       :         |                   |    
|    |    `----     |         |    |——————————————|    
| ___               | X       |    |              |    
|    |    ,---------"---------:    |              |    
|    |    |                   |                   |    
|    :    |    ,-  ------.    |    |——————————————|    
|    :    |    |         |    |    |              |    
|    :    |    |         |    |    |              |    
|    |    |    |_________|    |                   |    
|——‘__[  ]|____|||||||||||____|    ,--------------|    
|                   0                             |    
|       h h   h h      h h   h        h h   h h   |                                          
|       h h   h h      h h   h        h h   h h   |
|       h h   h h      h h   h        h h   h h   |                                           
|       h h   h h      h h   h        h h   h h   |    
|                                                 |    
`--------------- '    `---------------------------‘
        """)
        answer = input(">").lower()
    elif answer == "end":
        hospital_lobby()
        

def hospital_lobby():
    print("    You are in a hospital lobby waiting room. It seems, no one is here. \n    There is a reception desk straight ahead and chairs all around you...")
    time.sleep(2)
    print("\n        *RING* *RING* *RING*") 
    time.sleep(2)
    print("\n        *RING* *RING* *RING*")  
    time.sleep(2)
    print("\n        *RING* *RING* *RING*")
    time.sleep(1)
    print("""
    There is a phone ringing on the desk.

        What would you like to do?
    """)

    answer = input(">").lower()

    while answer.lower() != "answer" or "hallway":
        if answer == "answer":
            print("        \"If you know your party extention please dial it now\"")
            reception_phone()
        elif answer == "look":
            print("    You are in a hospital lobby. It appears no one is here. There is a hallway to the right of the front desk.")
            answer = input(">").lower()
        elif answer == "hint":
            print("\n        Can some one answer that? There is a hallway to the right of the front desk.")
            answer = input(">").lower()
        elif answer == "hallway":
            print("\n    You take the hallway to the right.")
            time.sleep(2)
            print("\n    You've reached the first room. It is to your right.")
            time.sleep(2)
            print("\n        would you like to CHECK it or CONTINUE on?")
            answer = input(">").lower()
        else:
            game_over("A ___ killed you")

# End Left Door ----------------------------------------------------------------------------------


# Room Choice Begin
def begin_game():
    print("\n\n    You are standing in a dark room.")
    time.sleep(2)
    print("    There are two doors in front of you.")
    time.sleep(1)
    print("    One to the Left and one to the Right.") 
    time.sleep(1)
    print("\n        Which one do you choose? \n        (you can always type hint if you're unsure what to do.)\n")
    
    answer = input(">").lower()

    while (answer != "l") or (answer != "r"):
        if answer == "hint":
            print("\n        l or r\n")
            answer = input(">").lower()
        elif answer == "items":
            Menus.item(begin_game)
        elif answer == "l":
            hospital_lobby()
        elif answer == "r":
            digital_forest()
        elif answer == "health":
            print("health: ", Player.health)
            print("")
            answer = input(">").lower()
        elif answer == "health_unlimited":
            print("GRANTED")
            Player.unlimited_health = True
            answer = input(">").lower()
        elif answer == "ammo_unlimited":
            print("GRANTED")
            Player.unlimited_ammo = True
            answer = input(">").lower()
        elif answer == "888888888888 CP":
            checkpoint_system()
        else: 
            print("\n        That isn't an option.\n")
            answer = input(">").lower()

# Clear screen function
def screen_clear():
   # for mac and linux(here, os.name is 'posix')
   if os.name == 'posix':
      _ = os.system('clear')
   else:
      # for windows platfrom
      _ = os.system('cls')

# Game start and title
def start():
    screen_clear()
    print("""
                                                                                                                                                                   
88888888ba,    88    ,ad8888ba,   88  888888888888    db         88              88888888888  ,ad8888ba,    88888888ba   88888888888  ad88888ba  888888888888  
88      `"8b   88   d8"'    `"8b  88       88        d88b        88              88          d8"'    `"8b   88      "8b  88          d8"     "8b      88       
88        `8b  88  d8'            88       88       d8'`8b       88              88         d8'        `8b  88      ,8P  88          Y8,              88       
88         88  88  88             88       88      d8'  `8b      88              88aaaaa    88          88  88aaaaaa8P'  88aaaaa     `Y8aaaaa,        88       
88         88  88  88      88888  88       88     d8YaaaaY8b     88              88````     88          88  88````88'    88           ```````8b,      88       
88         8P  88  Y8,        88  88       88    d8````````8b    88              88         Y8,        ,8P  88    `8b    88                  `8b      88       
88      .a8P   88   Y8a.    .a88  88       88   d8'        `8b   88              88          Y8a.    .a8P   88     `8b   88          Y8a     a8P      88       
88888888Y"'    88    `"Y88888P"   88       88  d8'          `8b  88888888888     88           `"Y8888Y"'    88      `8b  88888888888  "Y88888P"       88       

    """)
    time.sleep(2)
    print("\n    Welcome to the DIGITAL FOREST your responses should be one word, one letter for directions, or one word and one letter.")
    time.sleep(1)
    print("    *this game is best experienced in full screen*\n")
    print("        Type \"begin\" and press enter")
    print("")

    answer = input(">").lower()

    while answer != "begin":
        print("        Type \"begin\" and press enter\n")
        answer = input(">").lower()
    if answer == "begin":
        begin_game()


start()

# 4 spaces for non titles
# 8 spaces for player prompt and sounds

