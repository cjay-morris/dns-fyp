import os, json
from src.helpers.getZoneMapping import getZoneMapping
from azure.mgmt.dns import DnsManagementClient
from azure.identity import ClientSecretCredential

credentials = os.environ['AZURE_CREDENTIALS']
credentials = json.loads(credentials)
credentials = ClientSecretCredential(
    client_id=credentials['clientId'],
    client_secret=credentials['clientSecret'],
    tenant_id=credentials['tenantId']
)
subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
resourceGroup = os.environ['AZURE_RESOURCE_GROUP']

def getAllRecords(zoneName):
    client = DnsManagementClient(credentials, subscription_id)
    records = client.record_sets.list_by_dns_zone(resourceGroup, zoneName)
    return records

def deleteAllRecordsNotInMapping():
    zoneMapping = getZoneMapping()
    for zoneName in zoneMapping:
        records = getAllRecords(zoneName)
        for record in records:
            if record.name not in zoneMapping[zoneName]:
                print("Deleting", record.name, record.type.split("/")[2])
                try:
                    deleteRecord(zoneName, record.name, record.type.split("/")[2])
                    print("Deleted record", record.name, "of type", record.type.split("/")[1])
                except Exception as e:
                    print(e)

def deleteRecord(zoneName, recordName, recordType):
    client = DnsManagementClient(credentials, subscription_id)
    client.record_sets.delete(resourceGroup, zoneName, recordName, recordType)

deleteAllRecordsNotInMapping()
