# import pandas as pd
# if input() == "1":
#     test = pd.DataFrame({
#         "a":pd.Series(["a1", "a2", "a3"]),
#         "b":pd.Series(["b1", "b2", "b3"]),
#         "c":pd.Series(["c1", "c2", "c3"])
#     }, index=[0,1,2])
#     print(test)
#     test.to_csv("test.csv")
# else:
#     test = pd.read_csv("test.csv")
#     print(test)
import pypickle as pic
import random
import math
from main import tank
filepath = "test.pkl"

# if (input() == "1"):
#     tempObj = tank()
#     status = pic.save(filepath, tempObj)
#     print(tempObj)
# else:
#     data = pic.load(filepath)
#     if data == None:
#         raise Exception("need data to load")
#     print(data)

tempObj = tank()
print(type(tempObj))
print(type(type(tempObj)))
if type(tempObj) == tank:
    print("yay")
else:
    print("fail")