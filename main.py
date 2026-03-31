import random
import pandas as pd
import curses

class tank:
    def __init__(self):
        self.hp = 10
        self.damage = 5
        self.damage_range = 1
        self.hit_rate = 0.8

tankA = tank()
tankB = tank()
turn = random.randint(0,1)
while (tankA.hp > 0 or tankB.hp > 0):
    print("temp")
    break