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

# set required templates
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
        recordArray = recordValues
    # return json dump to ensure double quotes
    return json.dumps(recordArray)

def createRecord(record):
    if record.type == "A":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            ipvFourArray=recordsToArray(record.value, "ipv4Address"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "CNAME":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            recordValue=record.value,
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "NS":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            nsRecordArray=recordsToArray(record.value, "nsdname"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "MX":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            mxRecordArray=recordsToArray(record.value, ["preference", "exchange"]),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "TXT":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            txtRecordArray=recordsToArray([record.value], "value"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "AAAA":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            ipvSixArray=recordsToArray(record.value, "ipv6Address"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "SRV":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            srvArray=recordsToArray(record.value, ["priority", "weight", "port", "target"]),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "CAA":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            caaArray=recordsToArray(record.value, ["flags", "tag", "value"]),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )
    elif record.type == "PTR":
        return getTemplate(record.type.lower()).render(
            recordName=record.zoneName+"/"+record.name,
            ptrArray=recordsToArray(record.value, "ptrdname"),
            ttl=record.ttl,
            zoneName=record.zoneName,
            recordType=record.type
        )

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
        renderedTemplate = jsonTemplate.render(resources=template)
        json.dump(json.loads(renderedTemplate), f, indent=4)
