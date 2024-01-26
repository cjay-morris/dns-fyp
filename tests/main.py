import yaml
import os

currentAttributes = {"Type", "TTL", "Value"}

# helpers

def hasAttribute(obj, attribute):
    for key in obj:
        if key == attribute:
            return True
    return False

def getMapping():
    mapping = {}
    for zoneName in os.listdir("../zones"):
        for record in os.listdir("../zones/" + zoneName):
            recordObj = yaml.safe_load(open("../zones/" + zoneName + "/" + record))
            mapping[zoneName] = recordObj
    return mapping

# tests

def test_hasAttribute():
    mapping = getMapping()
    for zoneName in mapping:
        recordObj = mapping[zoneName]
        for attribute in currentAttributes:
            try:
                assert hasAttribute(recordObj, attribute)
            except AssertionError:
                print("Record " + zoneName + " has no attribute '" + attribute + "'")

def printHelloWorld():
    print("Hello World")
