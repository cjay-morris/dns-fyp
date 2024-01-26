import os
import json
import yaml
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))
dnsTemplate = env.get_template("dns-zone.txt")
cnameTemplate = env.get_template("cname.txt")
aTemplate = env.get_template("a.txt")
jsonTemplate = env.get_template("template.txt")
templateString = []

def makeZoneMapping():
    zoneMapping = {}
    for zoneName in os.listdir("zones"):
        zoneMapping[zoneName] = {}
        for record in os.listdir("zones/" + zoneName):
            recordValue = open("zones/" + zoneName + "/" + record, "r").read()
            yamlObj = yaml.safe_load(recordValue)
            zoneMapping[zoneName][record.replace(".yml", "")] = yamlObj
    return zoneMapping

def createZone(zoneName):
    zoneTemplate = dnsTemplate.render(
        domainName=zoneName
    )
    return zoneTemplate

def ARecordToIPV4Array(recordValues):
    if type(recordValues) == str:
        recordValues = [{"ipv4Address": recordValues}]
    else:
        recordValue = []
        for recordValue in recordValues:
            recordValue.append({"ipv4Address": recordValue})
    print(json.dumps(recordValues))
    return json.dumps(recordValues)

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
    mapping = makeZoneMapping()
    template = makeTemplate(mapping)
    template = ",".join(template)
    with open("template.json", "w") as f:
        renderedTemplate = jsonTemplate.render(resources=template)
        # print(renderedTemplate)
        json.dump(json.loads(renderedTemplate), f, indent=4)
