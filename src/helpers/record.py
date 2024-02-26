class DNSRecord:
    """
    A dynamic class to represent a DNS record of any type.

    Attributes:
        name (str): The hostname of the DNS record.
        type (str): The type of DNS record (e.g., "A", "CNAME", "MX").
        value (str or dict): The value of the DNS record, which can be a string or a list of strings depending on the type.
        ttl (int, optional): The time to live of the DNS record in seconds. Defaults to 3600 (1 hour).
    """

    def __init__(self, recordObject, zoneName, recordName):
        """
        The constructor for the DNSRecord class.

        Args:
            recordObject (dict): A dictionary representing a DNS record.
            zoneName (str): The name of the DNS zone.
            recordName (str): The name of the DNS record.
        """
        self.name = recordName
        self.type = recordObject["Type"]
        self.value = recordObject["Value"]
        self.ttl = recordObject.get("TTL", 3600)
        self.zoneName = zoneName

    def name(self):
        return self.name
    
    def type(self):
        return self.type
    
    def value(self):
        return self.value
    
    def ttl(self):
        return self.ttl

    def zoneName(self):
        return self.zoneName
