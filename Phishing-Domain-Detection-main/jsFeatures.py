'''
JavaScript based features
1. Website Forwarding
2. Status Bar Customization
3. Right Click Disabled
4. IFrame Redirection
'''

import requests
import re


def fetchJSFeatures(url):
    try:
        response = requests.get(url)
    except:
        response = ""

    functionList = [redirectsManyTimes, fakeStatusBar,
                    rightClickDisabled, usingIFrame]
    outputList = []
    for function in functionList:
        outputList.append(function(response))
    return outputList

# Website Forwarding


def redirectsManyTimes(response):
    if response == "":
        return 1
    else:
        if len(response.history) <= 2:
            return 0
        else:
            return 1

# Status Bar Customization


def fakeStatusBar(response):
    if response == "":
        return 1
    else:
        if re.findall("<script>.+onmouseover.+</script>", response.text):
            return -1
        else:
            return 1

# Disabling Right Click


def rightClickDisabled(response):
    if response == "":
        return 1
    else:
        if re.findall(r"event.button ?== ?2", response.text):
            return -1
        else:
            return 1

# IFrame Redirection


def usingIFrame(response):
    if response == "":
        return 1
    else:
        if re.findall(r"<iframe|<frameBorder", response.text):
            return -1
        else:
            return 1
