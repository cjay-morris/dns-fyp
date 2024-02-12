import dns
from dns import resolver
import sys

# array of domains that are vulnerable to dangling DNS records
vulnerableDomains = ["azurewebsites.net"]

# only good for checking CNAME records
def is_cname_record_dangling(url, type="CNAME"):
    try:
        print("Resolving", url)
        res = resolver.resolve(url, "A")
        # site is live - A record was resolved
        return False
    except Exception as e:
        try:
            res = resolver.resolve(url, type)
            return (is_cname_record_dangling(res[0].target.to_text()[:-1]))
        except Exception as es:
            print(es)
            for vulnerableDomain in vulnerableDomains:
                if url.endswith(vulnerableDomain):
                    print("Vulnerable domain - ", url)
                    return True
            print("No CNAME record found for", url)
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

if __name__ == "__main__":
    domainToCheck = sys.argv[1]
    print("Record is dangling: " + str(is_cname_record_dangling(domainToCheck)))
