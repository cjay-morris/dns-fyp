import os
import yaml
from jinja2 import Environment, FileSystemLoader


for recordFile in os.listdir():
    if recordFile.endswith(".yml"):
        record = (yaml.safe_load_all(open(recordFile)))
        for att in record:
            print(att['Value'])
            print(att['Type'])
            print(att['TTL'])