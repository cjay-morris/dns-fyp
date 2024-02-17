import os
import sys
import unittest

# TODO: Figure out why imports need . prefix to work in GitHub Actions
from .helpers.getZoneMapping import *
from .helpers.isRecordDangling import *

requiredAttributes = ["Type", "TTL", "Value"]
supportedRecordTypes = ["A", "CNAME", "MX", "NS", "PTR", "SOA", "SRV", "TXT"]

def hasRequiredAttributes(obj):
    for attribute in requiredAttributes:
        if attribute not in obj:
            return False
    return True

def isAnIPAddress(value):
    return (value.count(".") == 3) & (all(i.isdigit() for i in value.split(".")))

class TestRecords(unittest.TestCase):
    def test_hasAttribute(self):
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                self.assertTrue(hasRequiredAttributes(recordObj), domain + " is missing required attributes")

    def test_noDanglingRecords(self):
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                if recordObj["Type"] == "CNAME":
                    self.assertFalse(is_cname_record_dangling(recordObj["Value"]), domain + " is dangling. Record value is " + recordObj["Value"])

    def test_cnameRecordPointsToIPAddress(self):
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                if recordObj["Type"] == "CNAME":
                    self.assertTrue(not isAnIPAddress(recordObj["Value"]), domain + " has a CNAME record, " + record + ", that points to an IP address")
    
    def test_aRecordPointsToIPAddress(self):
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                if recordObj["Type"] == "A":
                    self.assertTrue(isAnIPAddress(recordObj["Value"]), domain + " has an A record, " + record + ", that does not point to an IP address. Value is " + recordObj["Value"])

    def test_zoneIsEmpty(self):
        mapping = getZoneMapping()
        for domain in mapping:
            self.assertTrue(len(mapping[domain]) > 0, domain + " is empty")

    def test_recordTypeIsSupported(self):
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                self.assertTrue(recordObj["Type"] in supportedRecordTypes, domain + " has an unsupported record type: " + recordObj["Type"])

    def test_ttlIsValid(self):
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                self.assertTrue(recordObj["TTL"] > 0, domain + " has an invalid TTL: " + str(recordObj["TTL"]))

    # TODO: Add test for different IP addresses in A record

if __name__ == "__main__":
    unittest.main()
