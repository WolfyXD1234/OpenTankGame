import random
# import pandas as pd # pyright: ignore[reportMissingModuleSource]
import pypickle as pkl # pyright: ignore[reportMissingImports]
import curses
import math
import time
from curses import wrapper

#set up stack for rendering objects
peiceStack = {}
for i in range(32):
    peiceStack[i] = []

#shorthand for rendering strings
shorthand = {
    "hp" : "hpc",
    "hpm" : "hpm",
    "damage" : "dmg",
    "damage_range" : "drg",
    "prefered_range" : "prg",
    "ok_range" : "org",
    "fire_pref" : "frc",
    "hit_rate" : "htr",
    "armor" : "arm",
    "travel" : "spd",
    "pips" : "eng"
}


def stackHandler(remove=False, location=0, peice="", y=1, x=1, color=4, movement="r", reverse=False):
    """
    remove - add peice if false, else remove\n
    location - location in stack (32 spots, -1 & remove to clear stack)\n
    peice - string to add \n
    y - ypos to place peice \n
    x - xpos to place peice \n
    color - color group to use \n
    movement - udlr - direction to print in
    reverse - reverse print order
    """
    if (location == -1 and remove == True):
        for i in range(32):
            peiceStack[i] = []
    elif (location < 0 or location >= 32):
        return
    elif (remove == True):
        peiceStack[location] = []
    else:
        peiceStack[location] = [peice, y, x, color, movement, reverse]

def renderStack(stdscr):
    """
    renders the curent stack
    """
    stdscr.clear()
    for i in range(32):
        obj = peiceStack[i]
        if (len(obj) == 0):
            pass
        else:
            peicePrint(stdscr, obj[0], obj[1], obj[2], obj[3], obj[4], obj[5])
    stdscr.refresh()

def peicePrint (stdscr, peice, y=1, x=1, color=4, movement="r", reverse=False):
    """
    srdscr - screen \n
    peice - string to print \n
    y - ypos to place peice \n
    x - xpos to place peice \n
    color - color group to use \n
    movement - udlr - direction to print in
    reverse - reverse print order
    """
    length = len(peice)
    for i in range(length):
        if (reverse == False):
            stdscr.addch(y, x, peice[i:i+1], (curses.color_pair(color)))
        else:
            stdscr.addch(y, x, peice[length-1-i:length-i], (curses.color_pair(color)))
        if (movement == "u"): y-=1
        elif (movement == "r"): x+=1
        elif (movement == "d"): y+=1
        elif (movement == "l"): x-=1
        if(y < 1 or x < 1): 
            return

class tank:
    def __init__(self, auto=True, /, *, difficulty=0, parts={}):
        self.baseStats = {
            "hp" : 100,
            "hpm" : 100,
            "damage" : 20,
            "damage_range" : 8,
            "prefered_range" : 120,
            "ok_range" : 10,
            "fire_pref" : 5,
            "hit_rate" : 0.7,
            "armor" : 0,
            "travel" : 20,
            #"pips" : 2
        }
        if (auto == True):
            self.parts = {"body":self.genPart(difficulty,"body"), 
                        "engine":self.genPart(difficulty,"engine"), 
                        "cannon":self.genPart(difficulty,"cannon"), 
                        "ai":self.genPart(difficulty,"ai"), 
                        "extra":self.genPart(difficulty,"extra")}
        else:
            self.parts = parts
        self.inventory = []
        self.hp = 100
        self.combats=0
        self.reStat()
        
    def genPart(self,dif,part):
        #generate chosen part
        #this is probably horrid code
        if (part == "body"):
            hpm = round(((random.random()*20)-10)*((dif+1)**0.5))
            armor = round(((random.random()*0.14)-0.01)*((dif+1)**0.5),3)
            travel = round(((random.random()*15)-7.5)*((dif+1)**0.5))
            #pips = ((random.random()*0)-0)*((dif+1)**0.5)
            #return {"hpm":hpm,"armor":armor,"travel":travel,"pips":pips}
            return {"hpm":hpm,"armor":armor,"travel":travel}
        elif (part == "engine"):
            travel = round(((random.random()*30)-15)*((dif+1)**0.5))
            hit_rate = abs(round(((random.random()*1)-0.5)*((dif+1)**0.5), 3))
            #pips = ((random.random()*0)-0)*((dif+1)**0.5)
            #return {"travel":travel,"hit_rate":hit_rate,"pips":pips}
            return {"travel":travel,"hit_rate":hit_rate}
        elif (part == "cannon"):
            damage = round(((random.random()*5)-2.5)*((dif+1)**0.5))
            damage_range = round(((random.random()*8)-4)*((dif+1)**0.5))
            hit_rate = round(((random.random()*2)-1)*((dif+1)**0.5),3)
            return {"damage":damage,"damage_range":damage_range,"hit_rate":hit_rate}
        elif (part == "ai"):
            prefered_range = round(((random.random()*40)-15)*((dif+1)**0.5))
            ok_range = round(((random.random()*10)-2.5)*((dif+1)**0.5))
            fire_pref = round(((random.random()*6)-3)*((dif+1)**0.5),3)
            return {"prefered_range":prefered_range,"ok_range":ok_range, "fire_pref":fire_pref}
        elif (part == "extra"):
            return{}
        else:
            print("what")
    
    def reStat(self):
        #sets tank stats based on parts
        self.hpm = 100
        self.damage = 20
        self.damage_range = 8
        self.prefered_range = 120
        self.ok_range = 10
        self.fire_pref = 5
        self.hit_rate = 0.7
        self.armor = 0
        self.travel = 20
        #self.pips = 2
        for part in self.parts:
            if type(self.parts[part]) == dict:
                for effect in self.parts[part]:
                    if effect in self.baseStats:
                        exec(f"self.{effect}+=self.parts[part][effect]")
                    else:
                        raise Exception("bad tank data: non stat data")
            else:
                raise Exception("bad tank data: bad part")
        if self.hp > self.hpm:
            self.hp = self.hpm
        if self.ok_range < 1:
            self.ok_range = 1
        if self.prefered_range < 100:
            self.prefered_range = 100
        if self.travel < 0:
            self.travel = 0
        if self.damage_range < 0:
            self.damage_range = 0

    def replacePart(self, inventoryPos):
        #replaces equiped part with chosen part
        partName = self.inventory[inventoryPos][0]
        partObj = self.inventory[inventoryPos][1]
        self.inventory.pop(inventoryPos)
        if partName in self.parts:
            self.inventory.append([partName, self.parts[partName]])
        else:
            raise Exception("Bad Name Error")
        self.parts[partName] = partObj
        self.reStat()
    
    def repair(self):
        self.hp = self.hpm
    
    def __str__(self):
        print(self.parts)
        #return(f" hp:{self.hpm}\n damage:{self.damage}\n damage_range:{self.damage_range}\n prefered_range:{self.prefered_range}\n ok_range:{self.ok_range}\n hit_rate:{self.hit_rate}\n armor:{self.armor}\n travel:{self.travel}\n pips:{self.pips}")
        return(f" hp:{self.hpm}\n damage:{self.damage}\n damage_range:{self.damage_range}\n prefered_range:{self.prefered_range}\n ok_range:{self.ok_range}\n hit_rate:{self.hit_rate}\n armor:{self.armor}\n travel:{self.travel}")

def attack (attacker, defender, distance):
    roll = random.random()
    armor = defender.armor
    if (armor < -0.5): armor = -0.5
    hit_chance = (attacker.hit_rate*10)/((distance**0.5)*(armor+1))
    if roll <= hit_chance:
        damage = attacker.damage + random.randrange(-attacker.damage_range, attacker.damage_range)
        if damage < 0:
            damage = 0
        defender.hp -= damage
        return("hit")
    else:
        return("miss")

def battle(stdscr, tankP, tankE):
    stackHandler(True, -1)
    distance = random.randint (100, 200)
    turn = random.randint(0,1)
    while (True):
        stackHandler(True, 31)
        stackHandler(False, 0, "=", 1, 1, 1)
        stackHandler(False, 1, "=", 1, 21, 1)
        stackHandler(False, 2, str(tankP.hp), 3, 1, 1)
        stackHandler(False, 3, str(tankE.hp), 3, 21, 2, "l", True)
        stackHandler(False, 4, str(distance), 4, 1, 1)
        renderStack(stdscr)
        curses.napms(500)
        if turn == 0:
            chance = random.random()
            if chance < ((10**(-(tankP.fire_pref/10)))/((10**(-(tankP.fire_pref/10)))+math.exp(-(abs(tankP.prefered_range-distance))))) and abs(tankP.prefered_range-distance) > tankP.ok_range:
                if abs(distance-tankP.prefered_range) < tankP.travel:
                    distance = tankP.prefered_range
                elif distance > tankP.prefered_range:
                    distance -= tankP.travel
                else:
                    distance += tankP.travel
            else:
                if (attack(tankP, tankE, distance) == "hit"):
                    stackHandler(False, 31, "@", 1, 21, 3)
                    stackHandler(False, 3, str(tankE.hp), 3, 21, 2, "l", True)
                else:
                    stackHandler(False, 31, "@", 1, 20, 3)
            turn = 1
        elif turn == 1:
            chance = random.random()
            if chance < ((10**(-(tankE.fire_pref/10)))/((10**(-(tankE.fire_pref/10)))+math.exp(-(abs(tankE.prefered_range-distance))))) and abs(tankE.prefered_range-distance) > tankE.ok_range:
                if abs(distance-tankE.prefered_range) < tankE.travel:
                    distance = tankE.prefered_range
                elif distance > tankE.prefered_range:
                    distance -= tankE.travel
                else:
                    distance += tankP.travel
            else:
                if (attack(tankE, tankP, distance) == "hit"):
                    stackHandler(False, 31, "@", 1, 1, 3)
                    stackHandler(False, 2, str(tankP.hp), 3, 1, 1)
                else:
                    stackHandler(False, 31, "@", 1, 2, 3)
            turn = 0
        renderStack(stdscr)
        curses.napms(300)

        #if tanks are dead, end battle
        if (tankP.hp <= 0):
            stackHandler(False, 0, "#", 1, 1, 4)
            win = False
            break
        elif(tankE.hp <= 0):
            stackHandler(False, 1, "#", 1, 21, 4)
            win = True
            break
    stackHandler(True, 31)
    renderStack(stdscr)
    time.sleep(3)
    if win == True:
        return tankE
    else:
        return False

def saveHandler(load = True, data = {}):
    #save data
    if load == False:
        if type(data) != dict or len(data) != 3:
            raise Exception("non-tank data: failed save")
        for index in data:
            if type(data[index]) != tank:
                raise Exception("non-tank data: failed save")
        return pkl.save("saves.pkl", data, True)

    #load data
    else:
        save = pkl.load("saves.pkl")
        if save == None:
            save = {0:tank(), 1:tank(), 2:tank()}
            for index in save:
                save[index].hp = 0
            pass
        else:
            if type(save) != dict or len(save) != 3:
                raise Exception("non-tank data: failed load")
            for index in save:
                if type(save[index]) != tank:
                    raise Exception("non-tank data: failed load")
        return save

def main(stdscr):

    curses.resizeterm(24,175)

    def tankMenu(player):
        """
        player - player tank
        used to load game
        """
        while True:
            curser_pos = 0
            #load menu
            stackHandler(True, -1)
            stackHandler(False, 0, "|||", 2, 1, 1, "d")
            stackHandler(False, 1, "|||", 2, 10, 1, "d")
            stackHandler(False, 2, "|||", 2, 19, 1, "d")
            stackHandler(False, 3, "-------------------", 1, 1, 1)
            stackHandler(False, 4, "-------------------", 3, 1, 1)
            stackHandler(False, 5, "-------------------", 5, 1, 1)
            stackHandler(False, 6, "Battle", 2, 3, 1)
            stackHandler(False, 7, "repair", 2, 12, 1)
            stackHandler(False, 8, "editer", 4, 3, 1)
            stackHandler(False, 9, "title?", 4, 12, 1)

            while True:
                #handle input
                if curser_pos == 0:
                    stackHandler(False, 31, ">", 2, 2, 1)
                elif curser_pos == 1:
                    stackHandler(False, 31, ">", 2, 11, 1)
                elif curser_pos == 2:
                    stackHandler(False, 31, ">", 4, 2, 1)
                elif curser_pos == 3:
                    stackHandler(False, 31, ">", 4, 11, 1)
                renderStack(stdscr)
                playerIn = stdscr.getch()
                if playerIn in [122, 32, 10]:
                    choice = curser_pos
                    break
                elif playerIn in [258, 259]:
                    curser_pos = curser_pos ^ 2
                elif playerIn in [260, 261]:
                    curser_pos = curser_pos ^ 1
            if choice == 3:
                #return to menu
                saveHandler(False, tanks)
                return
            if choice == 0:
                #combat
                fight = battle(stdscr, player, tank(difficulty=player.combats))
                if fight == False:
                    #handle loss
                    saveHandler(False, tanks)
                    return
                else:
                    #handle win
                    #get parts
                    part_list = []
                    for part in fight.parts:
                        part_list.append([part, fight.parts[part]])
                    partChoice = 0
                    #chose part
                    while True:
                        itemName = part_list[partChoice][0]

                        #render
                        stackHandler(True, -1)
                        if partChoice < len(part_list)-1:
                            itemName += " >"
                        if partChoice > 0:
                            stackHandler(False, 0, "<", 1, 1, 1)
                        stackHandler(False, 1, itemName, 1, 3, 1)
                        renderPos = 2
                        for effect in part_list[partChoice][1]:
                            stackHandler(False, renderPos, shorthand[effect]+":"+str(part_list[partChoice][1][effect]), renderPos, 3, 1)
                            renderPos+=1
                        renderStack(stdscr)

                        playerIn = stdscr.getch()
                        if playerIn == 260:
                            #increment part choice
                            if partChoice > 0:
                                partChoice -= 1
                        elif playerIn == 261:
                            #decrement part choice
                            if partChoice < len(part_list)-1:
                                partChoice += 1
                        elif playerIn in [122, 32, 10]:
                            #select part
                            chosen_part = part_list[partChoice]
                            break
                    #add part
                    player.inventory.append(chosen_part)
            if choice == 1:
                #heal & show stats
                stackHandler(True, -1)
                renderPos = 0
                for stat in player.baseStats:
                    exec(f"stackHandler(False, renderPos, shorthand[stat]+\":\"+str(player.{stat}), renderPos+1, 1, 1)")
                    renderPos+=1
                renderStack(stdscr)
                player.hp = player.hpm
                playerIn = stdscr.getch()
            if choice == 2:
                #edit tank
                curser_pos = 0
                partChoice = 0
                while True:
                    #rendering
                    if len(player.inventory) < 1:
                        break
                    stackHandler(True, -1)
                    stackHandler(False, 0, "Exit?", 1, 2, 1)
                    
                    itemName = player.inventory[partChoice][0]
                    if curser_pos == 0:
                        stackHandler(False, 1, ">", 1, 1, 1)
                    if partChoice < len(player.inventory)-1:
                        itemName += " >"
                    if partChoice > 0:
                        stackHandler(False, 2, "<", 3, 1, 1)
                    stackHandler(False, 3, itemName, 3, 3, 1)
                    renderPos = 4
                    for effect in player.inventory[partChoice][1]:
                        stackHandler(False, renderPos, shorthand[effect]+":"+str(player.inventory[partChoice][1][effect]), renderPos, 3, 1)
                        renderPos+=1

                    renderStack(stdscr)

                    #input
                    playerIn = stdscr.getch()
                    if playerIn == 259:
                        #set to quit button
                        curser_pos = 0
                    elif playerIn == 258:
                        #move down to selections
                        if len(player.inventory) > 0:
                            curser_pos = 1
                    elif playerIn == 260:
                        #change part choice -> 1
                        if partChoice > 0 and curser_pos == 1:
                            partChoice -= 1
                    elif playerIn == 261:
                        #change part choice <- 1
                        if partChoice < len(player.inventory)-1 and curser_pos == 1:
                            partChoice += 1
                    elif playerIn in [122, 32, 10]:
                        #select
                        if curser_pos == 0:
                            break
                        else:
                            player.replacePart(partChoice)
                            break


    

    tanks = saveHandler(True)
    global playerIn
    curses.curs_set(0)
    curses.start_color()
    curses.use_default_colors()
    curses.init_color(5, 500, 500, 500)
    #player
    curses.init_pair(1, 7, 0)
    #enemy
    curses.init_pair(2, 3, 0)
    #fire
    curses.init_pair(3, 1, 0)
    #background
    curses.init_pair(4, 5, 0)
    stdscr.bkgdset(" ", (curses.color_pair(4)))

    peicePrint(stdscr, "press start", 1, 1, 1)
    #stdscr.addstr(1,1,"press start", (curses.color_pair(1)))

    stdscr.getch() #for some reason this one reads the enter key press
    playerIn = stdscr.getch()
    stdscr.clear()

    if (playerIn == 112):
        while True:
            for i in range(8):
                curses.init_pair(i, i, 0)
                stdscr.addch(1,i+1, str(i)[-1:], (curses.color_pair(i)))
            if (curses.can_change_color() == True):
                stdscr.addch(2,1, "T", (curses.color_pair(7)))
            else:
                stdscr.addch(2,1, "F", (curses.color_pair(7)))
            stdscr.refresh()
            var = stdscr.getch()
            stdscr.clear()
            if var == 112:
                break
            else:
                peicePrint(stdscr, str(var), 3)
    else:
        while True:
            #load main menu
            curser_pos = 0

            #rendering
            stackHandler(False, 0, "|||", 2, 1, 1, "d")
            stackHandler(False, 1, "|||", 2, 10, 1, "d")
            stackHandler(False, 2, "|||", 2, 19, 1, "d")
            stackHandler(False, 3, "-------------------", 1, 1, 1)
            stackHandler(False, 4, "-------------------", 3, 1, 1)
            stackHandler(False, 5, "-------------------", 5, 1, 1)
            stackHandler(False, 6, "tank1", 2, 3, 1)
            stackHandler(False, 7, "tank2", 2, 12, 1)
            stackHandler(False, 8, "tank3", 4, 3, 1)
            stackHandler(False, 9, "quit?", 4, 12, 1)
            #tank 0 image
            if tanks[0].hp <= 0:
                stackHandler(False, 10, "#", 2, 9, 4)
            else:
                stackHandler(False, 10, "=", 2, 9, 1)
            #tank 1 image
            if tanks[1].hp <= 0:
                stackHandler(False, 11, "#", 2, 18, 4)
            else:
                stackHandler(False, 11, "=", 2, 18, 1)
            #tank 2 image
            if tanks[2].hp <= 0:
                stackHandler(False, 12, "#", 4, 9, 4)
            else:
                stackHandler(False, 12, "=", 4, 9, 1)

            #player input
            while True:
                if curser_pos == 0:
                    stackHandler(False, 31, ">", 2, 2, 1)
                elif curser_pos == 1:
                    stackHandler(False, 31, ">", 2, 11, 1)
                elif curser_pos == 2:
                    stackHandler(False, 31, ">", 4, 2, 1)
                elif curser_pos == 3:
                    stackHandler(False, 31, ">", 4, 11, 1)
                renderStack(stdscr)
                playerIn = stdscr.getch()
                if playerIn in [122, 32, 10]:
                    choice = curser_pos
                    break
                elif playerIn in [258, 259]:
                    curser_pos = curser_pos ^ 2
                elif playerIn in [260, 261]:
                    curser_pos = curser_pos ^ 1
            #quit
            if choice == 3:
                saveHandler(False, tanks)
                break
            #load tank of choice
            else:
                if tanks[choice].hp <= 0:
                    tanks[choice] = tank()
                else:
                    tankMenu(tanks[choice])


if __name__ == "__main__":
    wrapper(main)