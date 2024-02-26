import os
import sys
import unittest
from .helpers.getZoneMapping import getArrayOfDNSRecords
from .helpers.isRecordDangling import is_cname_record_dangling

# removes useless traceback output from unittest on failed tests
__unittest = True

requiredAttributes = ["Type", "TTL", "Value"]
supportedRecordTypes = ["A", "AAAA", "CAA", "CNAME", "MX", "NS", "PTR", "SRV", "TXT"]

records = getArrayOfDNSRecords()

aRecords = [record for record in records if record.type == "A"]
aaaaRecords = [record for record in records if record.type == "AAAA"]
caaRecords = [record for record in records if record.type == "CAA"]
cnameRecords = [record for record in records if record.type == "CNAME"]
mxRecords = [record for record in records if record.type == "MX"]
nsRecords = [record for record in records if record.type == "NS"]
ptrRecords = [record for record in records if record.type == "PTR"]
srvRecords = [record for record in records if record.type == "SRV"]
txtRecords = [record for record in records if record.type == "TXT"]

def isAnIPV4Address(value):
    """
    Checks if a string is a valid IPv4 address.

    Args:
        value (str): The string to check.
    
    Returns:
        bool: True if the string is a valid IPv4 address, False otherwise.
    """
    return (value.count(".") == 3) & (all(i.isdigit() for i in value.split(".")))

def isAnIPV6Address(value):
    """
    Checks if a string is a valid IPv6 address.

    Args:
        value (str): The string to check.

    Returns:
        bool: True if the string is a valid IPv6 address, False otherwise.
    """

    if len(value) > 39:
        return False

    groups = value.split(":")

    if len(groups) != 8:
        return False

    for group in groups:
        if not all(char in "0123456789abcdefABCDEF" for char in group):
            return False

    if any(group == "" for group in groups) or "::" in value:
        zero_groups = 0
        for i, group in enumerate(groups):
            if group == "":
                zero_groups += 1
            if zero_groups > 2:
                return False
            else:
                if zero_groups > 0:
                    if i != len(groups) - 1:
                        return False
                    zero_groups = 0
    return True

def isADomainName(domain):
    """
    Checks if a domain name is syntactically valid.

    Args:
        domain (str): The domain name to check.

    Returns:
        bool: True if the domain name is valid, False otherwise.
    """

    if not domain or len(domain) > 253:
        return False

    if domain.startswith("-") or domain.endswith("-"):
        return False

    labels = domain.split(".")

    if len(labels) < 2:
        return False

    for label in labels:
        if len(label) < 1 or len(label) > 63:
            return False
        if label.startswith("-") or label.endswith("-"):
            return False
        if not all(char in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for char in label):
            return False

    return True

def cnameRecordIsDangling(record):
    # if cname record points to another local record, don't try to resolve and instead take that record's value
    if record.value in [r.name + "." + r.zoneName for r in records]:
        return cnameRecordIsDangling([r for r in records if r.name + "." + r.zoneName == record.value][0])
    else:
        if is_cname_record_dangling(record.value):
            return True
        else:
            return False

class GenericTests(unittest.TestCase):
    def test_RecordsDontPointToThemselves(self):
        failed = []
        for record in records:
            if record.name + "." + record.zoneName == record.value:
                failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following records points to itself: " + ", ".join(failed))

    def test_AllRecordsHaveRequiredAttributes(self):
        failed = []
        for record in records:
            for attr in requiredAttributes:
                if not hasattr(record, attr.lower()):
                    failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following records are missing required attributes: " + ", ".join(failed))

    def test_zoneIsEmpty(self):
        failed = []
        for record in records:
            if record.zoneName == "":
                failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following records have an empty zone: " + ", ".join(failed))

    def test_recordTypeIsSupported(self):
        failed = []
        for record in records:
            if record.type not in supportedRecordTypes:
                failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following records have an unsupported type: " + ", ".join(failed))

    def test_ttlIsValid(self):
        failed = []
        for record in records:
            if record.ttl < 0:
                failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following records have an invalid TTL: " + ", ".join(failed))

class ARecordTests(unittest.TestCase):
    def test_aRecordPointsToIPAddress(self):
        failed = []
        for record in aRecords:
            if type(record.value) == list:
                for value in record.value:
                    if not isAnIPV4Address(value):
                        failed.append(record.name + "." + record.zoneName)
                        break
            else:
                if not isAnIPV4Address(record.value):
                    failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following A records do not point to an IP address: " + ", ".join(failed))

    def test_aRecordsAreUnique(self):
        failed = []
        for record in aRecords:
            if type(record.value) == list:
                if len(record.value) != len(set(record.value)):
                    failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following A records have duplicates: " + ", ".join(failed))

class AAAARecordTests(unittest.TestCase):
    def test_aaaaRecordPointsToIPAddress(self):
        failed = []
        for record in aaaaRecords:
            for value in record.value:
                if not isAnIPV6Address(value):
                    failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following AAAA records do not point to an IPV6 address: " + ", ".join(failed))

    def test_aaaaRecordsAreUnique(self):
        failed = []
        for record in aaaaRecords:
            if len(record.value) != len(set(record.value)):
                failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following AAAA records have duplicates: " + ", ".join(failed))

class CNAMERecordTests(unittest.TestCase):
    def test_cnameRecordIsNotDangling(self):
        failed = []
        for record in cnameRecords:
            if cnameRecordIsDangling(record):
                failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following CNAME records are dangling: " + ", ".join(failed))

    def test_cnameRecordPointsToIPAddress(self):
        failed = []
        for record in cnameRecords:
            if isAnIPV4Address(record.value) or isAnIPV6Address(record.value):
                failed.append(record.name + "." + record.zoneName)
        self.assertTrue(len(failed) == 0,  "The following CNAME records point to an IP address: " + ", ".join(failed))

class MXRecordTests(unittest.TestCase):
    def test_mxRecordPointsToValidDomain(self):
        failed = []
        for record in mxRecords:
            for value in record.value:
                if not isADomainName(value['exchange']):
                    failed.append(record.name + "." + record.zoneName)
                    break
        self.assertTrue(len(failed) == 0,  "The following MX records do not point to a valid domain: " + ", ".join(failed))

class NSRecordTests(unittest.TestCase):
    def test_nsRecordPointsToValidDomain(self):
        failed = []
        for record in nsRecords:
            if type(record.value) == list:
                for value in record.value:
                    if not isADomainName(value):
                        failed.append(record.name + "." + record.zoneName)
                        break
            else:
                if not isADomainName(record.value):
                    failed.append(record.name + "." + record.zoneName)
                    break
        self.assertTrue(len(failed) == 0,  "The following NS records do not point to a valid domain: " + ", ".join(failed))

if __name__ == "__main__":
    unittest.main()
