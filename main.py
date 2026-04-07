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
    def __init__(self, difficulty):
        self.hp = 100
        self.damage = 20
        self.damage_range = 8
        self.prefered_range = 120
        self.ok_range = 10
        self.hit_rate = 0.7
        self.armor = 0
        self.travel = 20
        self.pips = 2
        self.parts = {"body":{"hp":0,"armor":0,"travel":0,"pips":0}, 
                      "engine":{"travel":0,"pips":0}, 
                      "cannon":{"damage":0,"damage_range":0,"hit_rate":0}, 
                      "ai":{"prefered_range":0,"ok_range":0}, 
                      "extra":{}}
        for part in self.parts:
            print(part)
            print(type(part))
            print("---")
    def genPart(self,dif,part):
        if (part == "body"):
            hp = ((random.random()*20)-10)*((dif+1)**0.5)
            armor = ((random.random()*0.14)-0.01)*((dif+1)**0.5)
            travel = ((random.random()*20)-10)*((dif+1)**0.5)
            pips = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"hp":hp,"armor":armor,"travel":travel,"pips":pips}
        elif (part == "engine"):
            travel = ((random.random()*0)-0)*((dif+1)**0.5)
            pips = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"travel":travel,"pips":pips}
        elif (part == "cannon"):
            damage = ((random.random()*0)-0)*((dif+1)**0.5)
            damage_range = ((random.random()*0)-0)*((dif+1)**0.5)
            hit_rate = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"damage":damage,"damage_range":damage_range,"hit_rate":hit_rate}
        elif (part == "ai"):
            prefered_range = ((random.random()*0)-0)*((dif+1)**0.5)
            ok_range = ((random.random()*0)-0)*((dif+1)**0.5)
            return {"prefered_range":prefered_range,"ok_range":ok_range}
        elif (part == "extra"):
            pass
        else:
            print("what")

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
    distance = random.randint (100, 200)
    turn = random.randint(0,1)
    while (tankP.hp > 0 or tankP.hp > 0):
        stackHandler(True, 31)
        stackHandler(False, 0, "=", 1, 1, 1)
        stackHandler(False, 1, "=", 1, 21, 1)
        stackHandler(False, 2, str(tankP.hp), 3, 1, 1)
        stackHandler(False, 3, str(tankE.hp), 3, 21, 2, "l", True)
        stackHandler(False, 4, str(distance), 4, 1, 1)
        renderStack(stdscr)
        curses.napms(500)
        if turn == 0:
            if (attack(tankP, tankE, distance) == "hit"):
                stackHandler(False, 31, "@", 1, 21, 3)
                stackHandler(False, 3, str(tankE.hp), 3, 21, 2, "l", True)
            else:
                stackHandler(False, 31, "@", 1, 20, 3)
            turn = 1
        elif turn == 1:
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
            break
        elif(tankE.hp <= 0):
            stackHandler(False, 1, "#", 1, 21, 4)
            break
    stackHandler(True, 31)
    renderStack(stdscr)
    time.sleep(5)

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

    tankA = tank()
    tankB = tank()
    playerIn = stdscr.getch()
    stdscr.clear()

    if (playerIn == 112):
        # curses.init_color(5, 300, 300, 300)
        for i in range(8):
            curses.init_pair(i, i, 0)
            stdscr.addch(1,i+1, str(i)[-1:], (curses.color_pair(i)))
        if (curses.can_change_color() == True):
            stdscr.addch(2,1, "T", (curses.color_pair(7)))
        else:
            stdscr.addch(2,1, "F", (curses.color_pair(7)))
        stdscr.refresh()
        stdscr.getch()
    else:
        battle(stdscr,tankA,tankB)

# wrapper(main)
tanky = tank()
