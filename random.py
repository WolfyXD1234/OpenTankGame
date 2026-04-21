# import pandas as pd
# test = pd.DataFrame({
#     "a":pd.Series(["a1", "a2", "a3"]),
#     "b":pd.Series(["b1", "b2", "b3"]),
#     "c":pd.Series(["c1", "c2", "c3"])
# }, index=[1,2,3])
# # test = pd.read_csv("test.csv")
# print(test)

import pypickle as pic
import random
import math
from main import tank
filepath = "test.pkl"

if (input() == "1"):
    tempObj = tank()
    status = pypickle.save(filepath, tempObj)
    print(tempObj)
else:
    data = pypickle.load(filepath)
    print(data)