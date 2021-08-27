'''
Domain based features
1. Existence of DNS Record
2. Age of Domain
3. Alexa Rank
4. Google Index
'''

import whois  # python-whois
import requests
from datetime import datetime as dt
from urllib.parse import urlparse, quote, urlencode
import urllib.parse
from bs4 import BeautifulSoup


def fetchDomainFeatures(url):
    outputList = []
    domainName = ""
    # Existence of DNS record !
    dnsRecordExists = 1
    ageOfDomain = -1
    try:
        domainName = whois.whois(urlparse(url).netloc)
        ageOfDomain = domainAge(domainName)
    except:
        dnsRecordExists = -1
    outputList.append(ageOfDomain)
    outputList.append(dnsRecordExists)
    outputList.append(alexaRank(url))
    outputList.append(checkGoogleIndex(url))

    return outputList

# Age of domain


def domainAge(domainName):
    creationDate = domainName.creation_date
    expiryDate = domainName.expiration_date

    if isinstance(creationDate, str) or isinstance(expiryDate, str):
        try:
            creationDate = dt.strptime(creationDate, "%Y-%m-%d")
            expiryDate = dt.strptime(expiryDate, "%Y-%m-%d")
        except:
            return -1
    if ((expiryDate is None) or (creationDate is None)):
        return -1
    else:
        if type(expiryDate) is list:
            expiryDate = expiryDate[0]
        if type(creationDate) is list:
            creationDate = creationDate[0]
        ageOfDomain = abs((expiryDate - creationDate).days)
    if ((ageOfDomain/30) < 6):
        age = -1
    else:
        age = 1
    return age

# Website's Alexa Rank


def alexaRank(url):
    try:
        url = urllib.parse.quote(url)
        rank = BeautifulSoup(urllib.request.urlopen(
            "http://data.alexa.com/data?cli=10&dat=s&url=" + url).read(), "xml").find("REACH")['RANK']
        rank = int(rank)
    except TypeError:
        return -1
    if rank < 100000:
        return 1
    else:
        return 0

# Google Index


def checkGoogleIndex(url):
    user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'
    headers = {'User-Agent': user_agent}

    query = {'q': 'info:' + url}
    google = "https://www.google.com/search?" + urlencode(query)
    data = requests.get(google, headers=headers)
    data.encoding = 'ISO-8859-1'
    soup = BeautifulSoup(str(data.content), "html.parser")
    try:
        check = soup.find(id="rso").find(
            "div").find("div").find("h3").find("a")
        href = check['href']
        return 1
    except AttributeError:
        return -1
