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

for zoneName in os.listdir("zones"):
    templateString.append(dnsTemplate.render(
        domainName=zoneName
    ))
    for record in os.listdir("zones/" + zoneName):
        recordValue = open("zones/" + zoneName + "/" + record, "r").read()
        yamlObj = yaml.safe_load(recordValue)
        if yamlObj["Type"] == "A":
            record = aTemplate.render(
                recordName=zoneName+"/"+yamlObj["Type"],
                recordValue=yamlObj["Value"],
                ttl=300,
                zoneName=zoneName,
                recordType="A"
            )
        elif yamlObj["Type"] == "CNAME":
            record = cnameTemplate.render(
                recordName=zoneName+"/"+yamlObj["Type"],
                recordValue=yamlObj["Value"],
                ttl=300,
                zoneName=zoneName,
                recordType="CNAME"
            )
        templateString.append("\n" + record)

with open ("template.json", "w") as f:
    templateString = ",".join(templateString)
    json.dump(json.loads(jsonTemplate.render(resources=templateString)), f, indent=4)
