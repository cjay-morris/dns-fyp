import dns
from dns import resolver

def is_cname_record_dangling(cname_record):
    try:
        resolver.query(cname_record, 'A')
        return False
    except dns.resolver.NXDOMAIN:
        return True
