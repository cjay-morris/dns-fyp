import os
import sys
import unittest

# TODO: Figure out why imports need . prefix to work in GitHub Actions
from .helpers.getZoneMapping import *
from .helpers.isRecordDangling import *

requiredAttributes = ["Type", "TTL", "Value"]

def hasRequiredAttributes(obj):
    for attribute in requiredAttributes:
        if attribute not in obj:
            return False
    return True

class TestGetZoneMapping(unittest.TestCase):
    def test_hasAttribute(self):
        global failures
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                self.assertTrue(hasRequiredAttributes(recordObj), domain + " is missing required attributes")

    def test_noDanglingRecords(self):
        global failures
        mapping = getZoneMapping()
        for domain in mapping:
            for record in mapping[domain]:
                recordObj = mapping[domain][record]
                if recordObj["Type"] == "CNAME":
                    self.assertFalse(is_cname_record_dangling(recordObj["Value"]), domain + " is dangling. Record value is " + recordObj["Value"])

if __name__ == "__main__":
    unittest.main()
