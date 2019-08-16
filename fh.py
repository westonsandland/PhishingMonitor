#Weston Sandland, Procore Technologies 2019

def createIfAbsent(fn):
    newf = open(fn, "a+")
    newf.close()
    newf = open(fn, "r")
    retv = len(newf.read()) == 0
    newf.close()
    return retv #returns true if the file is empty
