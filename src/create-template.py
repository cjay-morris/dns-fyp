import os
import json
import yaml
from helpers.record import DNSRecord
from jinja2 import Environment, FileSystemLoader
from helpers.getZoneMapping import getZoneMapping

env = Environment(loader=FileSystemLoader("templates/"))
# run get_template on all files in the templates directory

templateString = []

# dynamically get templates when needed
def getTemplate(recordType):
    return env.get_template(recordType + ".txt")

dnsTemplate = env.get_template("dns-zone.txt")
jsonTemplate = env.get_template("template.txt")

def createZone(zoneName):
    zoneTemplate = dnsTemplate.render(
        domainName=zoneName
    )
    return zoneTemplate

def recordsToArray(recordValues, attributeNames):
    recordArray = []
    if (len(attributeNames) == 1) | (type(attributeNames) == str):
        if type(recordValues) == str:
            recordArray.append({attributeNames: recordValues})
        else:
            for recordValue in recordValues:
                recordArray.append({attributeNames: recordValue})
    else:
        for recordValue in recordValues:
            for attribute in attributeNames:
                recordArray.append({attribute: recordValue[attribute]})
    print(recordArray)
    return recordArray
        

def createRecord(record):
    if record.type == "A":
        recordTemplate = getTemplate(record.type.lower()).render(
            recordName=record.name,
            ipvFourArray=recordsToArray(record.value if record.value else record.values, "ipv4Address"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "CNAME":
        recordTemplate = getTemplate(record.type.lower()).render(
            recordName=record.name,
            recordValue=record.value,
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "NS":
        recordTemplate = getTemplate(record.type.lower()).render(
            recordName=record.name,
            nsRecordArray=recordsToArray(record.value if record.value else record.values, "nsdname"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "MX":
        recordTemplate = getTemplate(record.type.lower()).render(
            recordName=record.name,
            mxRecordArray=recordsToArray(record.mxRecords, ["preference", "exchange"]),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "TXT":
        recordTemplate = getTemplate(record.type.lower()).render(
            recordName=record.name,
            txtRecordArray=recordsToArray(record.value, "txtData"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    print(recordTemplate)
    return recordTemplate

def makeTemplate(zoneMapping):
    templateString = []
    for zoneName in zoneMapping:
        zoneTemplate = createZone(zoneName)
        templateString.append(zoneTemplate)
        for recordName in zoneMapping[zoneName]:
            record = DNSRecord(zoneMapping[zoneName][recordName], zoneName, recordName)
            templateString.append(createRecord(record))
    return templateString

if __name__ == "__main__":
    mapping = getZoneMapping()
    template = makeTemplate(mapping)
    template = ",".join(template)
    with open("template.json", "w") as f:
        with open("dump.json", "w") as d:
            d.write(template)
        renderedTemplate = jsonTemplate.render(resources=template)
        json.dump(json.loads(renderedTemplate), f, indent=4)
