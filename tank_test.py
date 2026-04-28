# import pandas as pd
import os
import pytest
import pypickle as pkl
from main import saveHandler, tank

def test_saves():

    #data for wrong data type
    with pytest.raises(Exception) as non_save_format:
        realSave = pkl.load("saves.pkl")
        pkl.save("saves.pkl", "bad data example", True)
        saveHandler(True)
    #data for no save data in save
    with pytest.raises(Exception) as no_save:
        saveHandler(False, {})

    #reset save data
    if realSave == None:
        os.remove("saves.pkl")
        print("removed bad save")
    else:
        pkl.save("saves.pkl", realSave, True)
        print("replaced bad save")
    
    #test for loading wrong data type
    assert "non-tank data" in str(non_save_format.value)
    #test for saving no data
    assert "non-tank data" in str(no_save.value)
    #test for saving good data
    tempSave = {0:tank(),1:tank(),2:tank()}
    assert saveHandler(False, tempSave) == True
    #test for loading good data
    assert saveHandler()

def test_tank_obj():
    with pytest.raises(Exception) as bad_tank1:
        tank(False, parts={"pynapple":42})
    with pytest.raises(Exception) as bad_tank2:
        tank(False, parts={"pynapple":{"pynapple":42}})
    #test for giving bad tank data
    assert "bad tank data" in str(bad_tank1.value)
    assert "bad tank data" in str(bad_tank2.value)