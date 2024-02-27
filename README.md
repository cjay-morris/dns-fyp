# dns-fyp 🌐

[![Tests](https://github.com/cjay-morris/dns-fyp/actions/workflows/tests.yml/badge.svg)](https://github.com/cjay-morris/dns-fyp/actions/workflows/tests.yml)
[![Azure ARM Deploy](https://github.com/cjay-morris/dns-fyp/actions/workflows/deploy.yml/badge.svg)](https://github.com/cjay-morris/dns-fyp/actions/workflows/deploy.yml)

An Infrastructure-as-Code repository for creating DNS records in Azure. This repository was created for DNS administrators, with the prevention and detection of CNAME-based and NS-based subdomain takeovers in mind.

## Contents 🔗

- [Getting Started](#getting-started-)
- [What is a subdomain takeover?](#what-is-a-subdomain-takeover-)
  - [Example of CNAME-based subdomain takeover](#example-of-cname-based-subdomain-takeover-)
  - [What are Cloud Providers doing to combat subdomain takeovers?](#what-are-cloud-providers-doing-to-combat-subdomain-takeovers-)
- [Why Infrastructure-as-Code?](#why-infrastructure-as-code-)
- [What Best Practices are implemented?](#what-best-practices-are-implemented-)
- [Examples](#examples-)

## Getting Started 🚀

TODO - repo structure, how to use, etc.

Will be completed once project is released as a template.

[🔝 Back to Top](#contents-)

## What is a subdomain takeover? 👨‍💻

A subdomain takeover is where an attacker gains control of a subdomain of a domain that they do not own.

Often, this is done by exploiting a misconfigured DNS record, such as a CNAME record pointing to a service that was deprovisioned.

[🔝 Back to Top](#contents-)

### Example of CNAME-based subdomain takeover 📝

A domain owner creates a CNAME record for their domain, `awesomeapp.cmorris.dev`, that points to a service hosted by a third-party, such as an Azure Web App, `cmorrisawesomeapp.azurewebsites.net`.

A few months down the line, the domain owner decides to stop using the third-party service and removes the Web App. However, they forget to remove the CNAME record.

At any point from the deletion of the Web App, an attacker can register a Web App with the same name and gain control of the subdomain `awesomeapp.cmorris.dev`. In this example, the attacker would have complete control over the subdomain and can host malicious content. Because the domain is pointing to an Azure Web App, they can also create an SSL certificate for the domain, so the takeover would be undetectable, even to the most security-aware users.

This is because many Cloud Providers release domain names back into the pool of available names after they are deleted and users are allowed to choose their app names.

[🔝 Back to Top](#contents-)

### What are Cloud Providers doing to combat subdomain takeovers? 🤔

Recently, Cloud Providers have started to implement measures to prevent subdomain takeovers.

For newer resources, Azure has started using semi-random domain names for their services, such as Azure Static Web Apps, meaning that users cannot choose their domain name.

Other Azure resources have also started to require domain verification, typically adding a TXT record to the domain to prove ownership.

Although these services take a step in the right direction, there are still many widely-used services that do not protect users from subdomain takeovers.

[🔝 Back to Top](#contents-)

## Why Infrastructure-as-Code? ⚙

Infrastructure-as-Code (IaC) is a DevOps practice that involves doing what it says on the tin - writing code to define infrastructure.

IaC has become increasingly popular in recent years, mainy due to the rise of Cloud Computing.

There are many benefits to IaC over traditional, manual infrastructure management:

- **Version Control** - Infrastructure changes can be tracked and swiftly rolled back if needed
- **Automated Testing** - Infrastructure can be tested automatically, reducing the chance of human error
- **Automated Deployment** - Infrastructure code can be deployed automatically, saving time and again reducing the chance of human error
- **Collaboration** - Infrastructure code can be reviewed and collaborated on by multiple people

[🔝 Back to Top](#contents-)

## What Best Practices are implemented? 💡

TODO - what tests are run, how subdomain takeover detection works, etc.

[🔝 Back to Top](#contents-)

## Examples 📚

TODO - will include examples of how to use the repository (record types, yml format)

[🔝 Back to Top](#contents-)
