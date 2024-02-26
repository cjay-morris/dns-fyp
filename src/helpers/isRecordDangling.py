import dns
from dns import resolver

# array of Azure domains that are vulnerable to dangling DNS records - from https://github.com/EdOverflow/can-i-take-over-xyz
vulnerableDomains = [
  "cloudapp.net",
  "cloudapp.azure.com",
  "azurewebsites.net",
  "blob.core.windows.net",
  "cloudapp.azure.com",
  "azure-api.net",
  "azurehdinsight.net",
  "azureedge.net",
  "azurecontainer.io",
  "database.windows.net",
  "azuredatalakestore.net",
  "search.windows.net",
  "azurecr.io",
  "redis.cache.windows.net",
  "azurehdinsight.net",
  "servicebus.windows.net",
  "visualstudio.com"
]

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
                    # site is vulnerable to dangling DNS records
                    return True
                # site MAY not be vulnerable to dangling DNS records - depends on the subdomain
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
