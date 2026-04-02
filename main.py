import random
import pandas as pd
import curses
import math
import time
from curses import wrapper

class tank:
    def __init__(self):
        self.hp = 100
        self.damage = 25
        self.damage_range = 10
        self.hit_rate = 0.5

def attack (attacker, defender):
    roll = random.random()
    if roll <= attacker.hit_rate:
        defender.hp -= attacker.damage + random.randrange(-attacker.damage_range, attacker.damage_range)
        return("hit")
    else:
        return("miss")

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
    turn = random.randint(0,1)
    hit = ""
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
        while (tankA.hp > 0 or tankB.hp > 0):
            stdscr.clear()
            peicePrint(stdscr, str(tankA.hp), 3, 1, 1)
            peicePrint(stdscr, str(tankB.hp), 3, 21, 2, "l", True)
            stdscr.addch(1,1,"=",(curses.color_pair(1)))
            stdscr.addch(1,2," ",(curses.color_pair(1)))
            stdscr.addch(1,21,"=",(curses.color_pair(2)))
            stdscr.addch(1,20," ",(curses.color_pair(2)))
            stdscr.refresh()
            curses.napms(500)
            if turn == 0:
                if (attack(tankA, tankB) == "hit"):
                    stdscr.addch(1,21, "@", (curses.color_pair(3)))
                    peicePrint(stdscr, str(tankB.hp), 3, 21, 2, "l", True)
                else:
                    stdscr.addch(1,20, "@", (curses.color_pair(3)))
                turn = 1
            elif turn == 1:
                if (attack(tankB, tankA) == "hit"):
                    stdscr.addch(1,1, "@", (curses.color_pair(3)))
                    peicePrint(stdscr, str(tankA.hp), 3, 1, 1)
                else:
                    stdscr.addch(1,2, "@", (curses.color_pair(3)))
                turn = 0
            stdscr.refresh()
            curses.napms(300)

            if (tankA.hp < 0):
                stdscr.addch(1,1, "#", (curses.color_pair(4)))
                stdscr.refresh()
                break
            elif(tankB.hp < 0):
                stdscr.addch(1,21, "#", (curses.color_pair(4)))
                stdscr.refresh()
                break

        time.sleep(5)

wrapper(main)