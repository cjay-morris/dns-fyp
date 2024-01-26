def 

if __name__ == "__main__":
    mapping = getZoneMapping()
    template = makeTemplate(mapping)
    template = ",".join(template)
    print(template)