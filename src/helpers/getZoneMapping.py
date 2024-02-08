import os
import yaml

def getZoneMapping():
    zoneMapping = {}
    for zoneName in os.listdir("zones"):
        zoneMapping[zoneName] = {}
        for record in os.listdir("zones/" + zoneName):                
            with open("zones/" + zoneName + "/" + record, "r") as file:
                recordValue = file.read()
                yamlObj = yaml.safe_load(recordValue)
                zoneMapping[zoneName][record.replace(".yml", "")] = yamlObj
    return zoneMapping

def getDomainNames():
    domainNames = []
    for zoneName in os.listdir("zones"):
        domainNames.append(zoneName)
    return domainNames
