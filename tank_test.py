# import pandas as pd
import os
import pytest
import pypickle as pkl
from main import saveHandler

def test_saves():

    #data for wrong data type
    with pytest.raises(Exception) as excinfo:
        realSave = pkl.load("saves.pkl")
        pkl.save("saves.pkl", "bad data example", True)
        saveHandler(True)

    #reset save data
    if realSave == None:
        # os.remove("saves.pkl")
        print("removed bad save")
    else:
        pkl.save("saves.pkl", realSave, True)
        print("replaced bad save")
    
    #test for loading wrong data type
    assert "non-tank data" in str(excinfo.value)

    
    #test for loading non number values

    #test for saving no data
    # with pytest.raises(Exception) as excinfo:
    #     saveHandler(False, {})
    # assert "corrupted game" in str(excinfo.value)


