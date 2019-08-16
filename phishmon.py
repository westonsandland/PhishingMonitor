#Weston Sandland, Procore Technologies 2019
import namegen
import fh
import clock

import requests
import time
import json
import threading
import re
import os

recentsName = "recents.txt"
masterName = "masterlist.txt"
debug = False

def makeRequest(website):
   headers = {
       'Authorization': 'Bearer API_KEY', #replace with your API Key as shown in SSLMate API Credentials - Keep "Bearer "
   }
   params = (
       ('domain', website),
       #('expand', 'dns_names'), #uncomment for debugs
       #('expand', 'issuer'),
       #('expand', 'cert'),
   )
   raw = requests.get('https://api.certspotter.com/v1/issuances', headers=headers, params=params).json()
   return raw


def handleRecents(site):
    fh.createIfAbsent(masterName)
    fh.createIfAbsent(recentsName)
    masterFile = open(masterName, "r+")
    allMasters = masterFile.read()
    masterFile.close()
    if site not in str(allMasters):
        recentsFile = open(recentsName, "a+")
        masterFile = open(masterName, "a+")
        recentsFile.write(site + "\n")
        masterFile.write(site + "\n")
        recentsFile.close()
        masterFile.close()
    return 0

def phishProcessing(input, rotfsitelist, output):
    inputfile = open(input, "w+")
    inputfile.write(rotfsitelist[1])
    inputfile.close()
    certs = makeRequest(rotfsitelist[0])
    print(rotfsitelist[0])
    if len(certs) > 0:
        handleRecents(rotfsitelist[0])
        phfile = open(output, "a+")
        phfile.write("The website " + rotfsitelist[0] + " has the following certificates:\n")
        print(certs)
        for cert in certs:
            phfile.write(json.dumps(cert) + "\n")
        phfile.close()
    inputfile = open(input, "r+")
    rotfsitelist[0] = inputfile.readline()[:-1]
    rotfsitelist[1] = inputfile.read()
    inputfile.close()
    return 0

def removeSite(input, rotfsitelist):
    print(rotfsitelist[0])
    inputfile = open(input, "w+")
    inputfile.write(rotfsitelist[1])
    inputfile.close()
    inputfile = open(input, "r+")
    rotfsitelist[0] = inputfile.readline()[:-1]
    rotfsitelist[1] = inputfile.read()
    inputfile.close()
    return 0

def pingSite(website):
    t = time.time()
    try:
        response = requests.get("https://"+website).status_code
        print(response)
    except:
        response = -1
    return response != -1

def stdSleep():
    time.sleep(3.6)
    return 0

def requestAll(input, output):
    inputfile = open(input, "r+")
    rotfsitelist = ["",""]
    rotfsitelist[0] = inputfile.readline()[:-1] #site
    rotfsitelist[1] = inputfile.read() #restofthefile
    inputfile.close()
    while len(rotfsitelist[1]) > 0: #multithreading saves approximately 0.2 seconds per request
        if pingSite(rotfsitelist[0]):
            t = time.time()
            t1 = threading.Thread(target=phishProcessing, args=(input, rotfsitelist, output))
            t2 = threading.Thread(target=stdSleep)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
            if time.time() - t <= 3.6:
                print("Error, time taken less than thread: ",time.time() - t)
        else:
            removeSite(input, rotfsitelist)
    return 0

def populateInput(name, input, replacement):
    isEmpty = fh.createIfAbsent(input)
    if isEmpty:
        sites = namegen.generateNames(name, replacement)
        sitefile = open(input, "a+")
        for site in sites:
            sitefile.write(site+"\n")
        sitefile.write("If this is the only remaining text, all generated phishing sites have been exhausted.")
        sitefile.close()
    return 0

def clearFiles(notThis):
    cwd = os.getcwd()
    files = os.listdir(cwd)
    for f in files:
        if f.endswith(".txt") and f not in notThis:
            os.remove(os.path.join(cwd, f))
    return 0

def certRoutine(valid):
    if debug:
        fh.createIfAbsent(masterName)
        repf = "psdebug.txt"
        master = open("masterlist.txt", "r+")
        rotfsitelist = ["",""]
        rotfsitelist[0] = master.readline()[:-1]
        rotfsitelist[1] = master.read()
        master.close()
        master = open("masterlist.txt", "w+")
        master.write(rotfsitelist[1])
        master.close()
    else:
        repf = "ps.txt"
    clearFiles(["ps.txt", masterName, recentsName, "time.txt", "psdebug.txt"])
    inprefix = "phsites"
    outprefix = "phcerts"
    inf = inprefix + "-" + re.search(".+\.", valid).group() + "txt"
    outf = outprefix + "-" + re.search(".+\.", valid).group() + "txt"
    populateInput(valid, inf, repf)
    requestAll(inf, outf)
    return 0

def main():
    while True:
        if debug:
            certRoutine("red.com")
            certRoutine("okta.com")
        else:
            certRoutine("gmail.com")
            certRoutine("google.com")
        clock.check(debug)

if __name__ == "__main__":
    main()
