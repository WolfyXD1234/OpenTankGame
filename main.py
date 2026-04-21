import random
import pandas as pd # pyright: ignore[reportMissingModuleSource]
import curses
import math
import time
from curses import wrapper

peiceStack = {}
for i in range(32):
    peiceStack[i] = []

def stackHandler(remove=False, location=0, peice="", y=1, x=1, color=4, movement="r", reverse=False):
    """
    remove - add peice if false, else remove
    location - location in stack (32 spots, -1 & remove to clear stack)
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
            "pips" : 2
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
        self.reStat()
        
    def genPart(self,dif,part):
        if (part == "body"):
            hpm = round(((random.random()*20)-10)*((dif+1)**0.5))
            armor = round(((random.random()*0.14)-0.01)*((dif+1)**0.5),3)
            travel = round(((random.random()*20)-10)*((dif+1)**0.5))
            pips = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"hpm":hpm,"armor":armor,"travel":travel,"pips":pips}
        elif (part == "engine"):
            travel = round(((random.random()*0)-0)*((dif+1)**0.5))
            hit_rate = ((random.random()*0)-0)*((dif+1)**0.5)
            pips = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"travel":travel,"hit_rate":hit_rate,"pips":pips}
        elif (part == "cannon"):
            damage = round(((random.random()*0)-0)*((dif+1)**0.5))
            damage_range = round(((random.random()*0)-0)*((dif+1)**0.5))
            hit_rate = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"damage":damage,"damage_range":damage_range,"hit_rate":hit_rate}
        elif (part == "ai"):
            prefered_range = round(((random.random()*0)-0)*((dif+1)**0.5))
            ok_range = round(((random.random()*0)-0)*((dif+1)**0.5))
            fire_pref = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"prefered_range":prefered_range,"ok_range":ok_range, "fire_pref":fire_pref}
        elif (part == "extra"):
            return{}
        else:
            print("what")
    
    def reStat(self):
        self.hpm = 100
        self.damage = 20
        self.damage_range = 8
        self.prefered_range = 120
        self.ok_range = 10
        self.fire_pref = 5
        self.hit_rate = 0.7
        self.armor = 0
        self.travel = 20
        self.pips = 2
        for part in self.parts:
            for effect in self.parts[part]:
                exec(f"self.{effect}+=self.parts[part][effect]")
        if self.hp > self.hpm:
            self.hp = self.hpm
    
    def repair(self):
        self.hp = self.hpm
    
    def __str__(self):
        print(self.parts)
        return(f" hp:{self.hpm}\n damage:{self.damage}\n damage_range:{self.damage_range}\n prefered_range:{self.prefered_range}\n ok_range:{self.ok_range}\n hit_rate:{self.hit_rate}\n armor:{self.armor}\n travel:{self.travel}\n pips:{self.pips}")

def attack (attacker, defender, distance):
    roll = random.random()
    armor = defender.armor
    if (armor < -0.5): armor = -0.5
    hit_chance = (attacker.hit_rate*10)/((distance**0.5)*(armor+1))
    if roll <= hit_chance:
        defender.hp -= attacker.damage + random.randrange(-attacker.damage_range, attacker.damage_range)
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

        if (tankP.hp <= 0):
            stackHandler(False, 0, "#", 1, 1, 4)
            win = True
            break
        elif(tankE.hp <= 0):
            stackHandler(False, 1, "#", 1, 21, 4)
            win = False
            break
    stackHandler(True, 31)
    renderStack(stdscr)
    time.sleep(3)
    return win

def saveHandler():
    pass

def main(stdscr):
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
        curser_pos = 0
        while True:
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
            if True:
                stackHandler(False, 10, "#", 2, 9, 4)
            if True:
                stackHandler(False, 11, "#", 2, 18, 4)
            if True:
                stackHandler(False, 12, "#", 4, 9, 4)
            #battle(stdscr,tankA,tankB)
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
                if curser_pos < 0:
                    curser_pos += 4
                else:
                    curser_pos = curser_pos%4
            if choice == 3:
                break
            if choice == 0:
                battle(stdscr, tank(), tank())
            if choice == 1:
                battle(stdscr, tank(), tank())
            if choice == 2:
                battle(stdscr, tank(), tank())
            else:
                time.sleep(2)

wrapper(main)

# for i in range(10):
#     print(i%4)