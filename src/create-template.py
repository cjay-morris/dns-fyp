import os
import json
import yaml
from jinja2 import Environment, FileSystemLoader
from helpers.getZoneMapping import getZoneMapping

env = Environment(loader=FileSystemLoader("templates/"))
dnsTemplate = env.get_template("dns-zone.txt")
cnameTemplate = env.get_template("cname.txt")
aTemplate = env.get_template("a.txt")
jsonTemplate = env.get_template("template.txt")
templateString = []

def createZone(zoneName):
    zoneTemplate = dnsTemplate.render(
        domainName=zoneName
    )
    return zoneTemplate

def recordsToArray(recordValues):
    recordArray = []
    for value in recordValues.split(" "):
        recordArray.append({
            "ivp4Address": value
        })
    return json.dumps(recordArray)
        

def createRecord(zoneName, recordName, recordValue, recordType, ttl=300):
    if recordType == "A":
        recordTemplate = aTemplate.render(
            recordName=zoneName+"/"+recordName,
            ipvFourArray=ARecordToIPV4Array(recordValue),
            ttl=ttl,
            zoneName=zoneName,
            recordType=recordType
        )
    elif recordType == "CNAME":
        recordTemplate = cnameTemplate.render(
            recordName=zoneName+"/"+recordName,
            recordValue=recordValue,
            ttl=ttl,
            zoneName=zoneName,
            recordType=recordType
        )
    elif recordType == "NS":
        recordTemplate = nsTemplate.render(
            recordName=zoneName+"/"+recordName,
            recordValue=recordValue,
            ttl=ttl,
            zoneName=zoneName,
            recordType=recordType
        )
    return recordTemplate

def makeTemplate(zoneMapping):
    templateString = []
    for zoneName in zoneMapping:
        zoneTemplate = createZone(zoneName)
        templateString.append(zoneTemplate)
        for recordName in zoneMapping[zoneName]:
            recordValue = zoneMapping[zoneName][recordName]
            recordType = recordValue["Type"]
            if recordType == "A":
                recordTemplate = createRecord(zoneName, recordName, recordValue["Value"], recordType)
                templateString.append(recordTemplate)
            elif recordType == "CNAME":
                recordTemplate = createRecord(zoneName, recordName, recordValue["Value"], recordType)
                templateString.append(recordTemplate)
    return templateString

if __name__ == "__main__":
    mapping = getZoneMapping()
    template = makeTemplate(mapping)
    template = ",".join(template)
    with open("template.json", "w") as f:
        renderedTemplate = jsonTemplate.render(resources=template)
        json.dump(json.loads(renderedTemplate), f, indent=4)
