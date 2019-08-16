#Weston Sandland, Procore Technologies 2019
import re
import fh

def populateSubs(replacement): #this method puts all the substitute characters in a list from a txt file
    ps = open(replacement, "r")
    psResult = {}
    if ps.mode == 'r':
        line = ps.readline()
        while line != "-":
            unsplit = re.search("[^\\n:]{2,}", line)
            if unsplit != None:
                elements = re.split("\s", unsplit.group())
                for e in elements:
                    if len(e) == 0:
                        elements.remove(e)
                psResult[re.match(".", line).group()] = elements
            line = ps.readline()
    return psResult

def pluralize(labels): #adds in 's' to all the ends of the labels
    labelss = []
    for label in labels:
        labelss.append(label)
        labelss.append(label + 's')
    return labelss

def phishLabels(label, list, subs): #recursive method that creates a list of all possible phishing site domains
    if len(label) == 0:
        return list
    toSub = label[0]
    newList = []
    for perm in list:
        newList.append(perm + toSub)
        if toSub in subs:
            for subLetter in subs[toSub]:
                newList.append(perm + subLetter)
    return phishLabels(label[1:], newList, subs)

def phishform(domain, subs, TLDs): #adds the domains onto the ends of the phish labels
    phishList = []
    #for these purposes, "label" refers to the name before TLD, and TLD is the ".com" part
    label = re.search("[^\.]+", domain).group()
    pLabels = phishLabels(label, [""], subs)
    if domain[-1:] != 's': #if it doesn't already end in s, add all domains that are plural to the list
        pLabels = pluralize(pLabels)
    for pl in pLabels:
        for t in TLDs:
            phishList.append(pl+t)
    return phishList

def checkWhitelist(phishList, orig):
    whitePrefix = "whitelist"
    whiteName = whitePrefix + "-" + re.search(".+\.", orig).group() + "txt"
    if fh.createIfAbsent(whiteName):
        defaulter = open(whiteName, "w")
        defaulter.write(orig+"\n")
        defaulter.write(re.search(".+\.", orig).group()[:-1]+".org"+"\n")
        defaulter.close()
    inputfile = open(whiteName, "r")
    toWhite = inputfile.readline()[:-1]
    while len(toWhite) > 0:
        if toWhite in phishList:
            phishList.remove(toWhite)
        toWhite = inputfile.readline()[:-1]
    inputfile.close()
    return 0


def generateNames(original, replacement):
    possibleTLDs = [".com", ".net", ".org"]
    phishSubs = populateSubs(replacement)
    phishSites = phishform(original, phishSubs, possibleTLDs)
    checkWhitelist(phishSites, original)
    return phishSites

def main():
    sites = generateNames("WEBSITE.TLD") #enter your website and top level domain, such as "github.com"
    for i in range(len(sites)):
        print(str(i+1) + ": " + sites[i])
    return 0

if __name__ == "__main__":
    main()