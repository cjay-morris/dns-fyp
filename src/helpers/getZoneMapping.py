import os
import yaml
from .record import DNSRecord

def getArrayOfDNSRecords():
    zoneMapping = getZoneMapping()
    arrayOfDNSRecords = []
    for zoneName in zoneMapping:
        for recordName in zoneMapping[zoneName]:
            record = DNSRecord(zoneMapping[zoneName][recordName], zoneName, recordName)
            arrayOfDNSRecords.append(record)
    return arrayOfDNSRecords

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

def getZoneNames():
    zoneNames = []
    for zoneName in os.listdir("zones"):
        zoneNames.append(zoneName)
    return zoneNames

def getDomainNames():
    domainNames = []
    for zoneName in os.listdir("zones"):
        domainNames.append(zoneName)
    return domainNames
