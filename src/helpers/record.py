class DNSRecord:
    def __init__(self, recordObject, zoneName, recordName):
        # required fields
        self.type = recordObject['Type']
        self.name = recordName
        self.ttl = recordObject['TTL']
        self.zoneName = zoneName

        # optional fields
        self.preference = recordObject.get('preference', None)
        self.exchange = recordObject.get('exchange', None)
        self.value = recordObject.get('Value', None)
        self.mxRecords = recordObject.get('MXRecords', None)
        self.values = recordObject.get('Values', None)
    
    def type(self):
        return self.type
    
    def name(self):
        return self.name
    
    def value(self):
        return self.value
    
    def values(self):
        return self.value
    
    def ttl(self):
        return self.ttl
    
    def zoneName(self):
        return self.zoneName
    
    def mxRecords(self):
        return self.mxRecords