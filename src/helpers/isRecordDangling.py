import dns
from dns import resolver

# array of domains that are vulnerable to dangling DNS records
vulnerableDomains = ["azurewebsites.net"]

# only good for checking CNAME records
def is_cname_record_dangling(url, type="CNAME"):
    try:
        res = resolver.resolve(url, "A")
        # site is live - A record was resolved
        return False
    except Exception as e:
        try:
            res = resolver.resolve(url, type)
            # recursively try to resolve if CNAME points to another CNAME
            return (is_cname_record_dangling(res[0].target.to_text()[:-1]))
        except Exception as es:
            for vulnerableDomain in vulnerableDomains:
                if url.endswith(vulnerableDomain):
                    return True
            if Exception == dns.resolver.NXDOMAIN:
                print("NXDOMAIN - domain does not exist")
                return False
            print("Unknown domain, possibly dangling???")
            return True

def is_ns_record_dangling(url, type="NS"):
    try:
        print("Resolving", url)
        res = resolver.resolve(url, "NS")
        # site is live - A record was resolved
        return False
    except Exception as e:
        print(e)
        return True
