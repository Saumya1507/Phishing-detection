'''
URL based features
1. URL Contains IP Address
2. URL Length
3. Uses a URL Shortening Service
4. URL Contains '@' Symbol
5. URL Contains '//' Symbol for Redirection
6. URL Contains '-' Symbol as a Prefix/Suffix
7. Subdomain or  Multi level subdomain
8. Domain Registration Length
9. URL Contains "HTTPS"
'''

import re
import ipaddress as ip
from urllib.parse import urlparse
import whois  # python-whois
from datetime import datetime as dt


def fetchURLFeatures(url):
    functionList = [isIPinURL, classifyURLLength, usesShorteningService,
                    containsAtSymbol, redirectSymbol, containsDashSymbol,
                    domainLevel, domainRegistrationLen, containsHTTPS]
    outputList = []
    for function in functionList:
        outputList.append(function(url))
    return outputList

# IP Address in URL


def isIPinURL(url):
    domain = urlparse(url).netloc
    try:
        ip.ip_address(domain)
        ipFlag = -1
    except:
        ipFlag = 1
    return ipFlag

# Long URL to hide the suspicious part


def classifyURLLength(url):
    if len(url) < 54:
        return 1
    elif len(url) >= 54 and len(url) <= 75:
        return 0
    else:
        return -1

# Use of URL shortening services


def usesShorteningService(url):
    shortServiceList = r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
        r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
        r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
        r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|" \
        r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|" \
        r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|" \
        r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|" \
        r"tr\.im|link\.zip\.net"
    foundFlag = re.search(shortServiceList, url)
    if foundFlag:
        return -1
    else:
        return 1

# URL contains an '@' symbol


def containsAtSymbol(url):
    if '@' in url:
        return -1
    else:
        return 1

# Redirects using the '//' symbol


def redirectSymbol(url):
    position = url.rfind("//")
    if position <= 7:
        return 1
    else:
        return -1

# Use of the '-' symbol as a suffix/prefix


def containsDashSymbol(url):
    domainName = urlparse(url).netloc
    if '-' in domainName:
        return -1
    else:
        return 1

# Subdomain or Multi level subdomain


def domainLevel(url):
    url = url.replace("www.", "")
    dotCount = url.count('.')
    if dotCount == 1:
        return 1
    elif dotCount == 2:
        return 0
    else:
        return -1

# Domain Registration Length


def domainRegistrationLen(url):
    domainName = ""
    legitimate = -1
    try:
        domainName = whois.whois(urlparse(url).netloc)
    except:
        return -1
    expiryDate = domainName.expiration_date
    if isinstance(expiryDate, str):
        try:
            expiryDate = dt.strptime(expiryDate, "%Y-%m-%d")
        except:
            return 1
    if (expiryDate is None):
        return -1
    elif (type(expiryDate) is list):
        return -1
    else:
        today = dt.now()
        end = abs((expiryDate - today).days)
        if ((end/30) < 6):
            legitimate = -1
        else:
            legitimate = 1
    return legitimate

# Use of HTTPS in the domain name


def containsHTTPS(url):
    domainName = urlparse(url).netloc
    if "https" in domainName:
        return -1
    else:
        return 1
