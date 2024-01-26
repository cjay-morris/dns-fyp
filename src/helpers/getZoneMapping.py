import os
import yaml

def getZoneMapping():
    zoneMapping = {}
    for zoneName in os.listdir("zones"):
        zoneMapping[zoneName] = {}
        for record in os.listdir("zones/" + zoneName):
            recordValue = open("zones/" + zoneName + "/" + record, "r").read()
            yamlObj = yaml.safe_load(recordValue)
            zoneMapping[zoneName][record.replace(".yml", "")] = yamlObj
    return zoneMapping