import os
import json
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates/"))
dnsTemplate = env.get_template("dns-zone.txt")
recordTemplate = env.get_template("record.txt")
jsonTemplate = env.get_template("template.txt")
templateString = []

for zoneName in os.listdir("zones"):
    templateString.append(dnsTemplate.render(
        domainName=zoneName
    ))
    for record in os.listdir("zones/" + zoneName):
        recordValue = open("zones/" + zoneName + "/" + record, "r").read()
        record = recordTemplate.render(
            recordName=record,
            recordValue=recordValue,
            ttl=300,
            zoneName=zoneName,
            recordType="CNAME"
        )
        templateString.append("\n" + record)

with open ("template.json", "w") as f:
    templateString = ",".join(templateString)
    print(templateString)
    json.dump(json.loads(jsonTemplate.render(resources=templateString)), f, indent=4)