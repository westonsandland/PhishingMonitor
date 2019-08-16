#Weston Sandland, Procore Technologies 2019
import fh
import smtp
import time

timename = "time.txt"
week = 604800
halfminute = 30

debrecipients = ["DEBUGRECIPIENT@gmail.com","DEBUGRECIPIENT@gmail.com"] #MORE ADDRESSES CAN BE ENTERED INTO THESE ARRAYS: ADDRESS@DOMAIN.COM
recipients = ["RECIPIENT@gmail.com","RECIPIENT@gmail.com","RECIPIENT@gmail.com"]

def isItTime(debug):
    fh.createIfAbsent(timename)
    timef = open(timename, "r+")
    contents = timef.read()
    timef.close()
    if len(contents) == 0:
        timef = open(timename, "a+")
        timef.write(str(time.time()))
        timef.close()
        savedTime = time.time()
    else:
        savedTime = int(float(contents))
    if debug:
        interval = halfminute
    else:
        interval = week
    if savedTime + interval <= time.time():
        timef = open(timename, "w+")
        timef.write(str(time.time()))
        timef.close()
        return True
    return False

def sitesFound():
    return len(open("recents.txt", "r").read()) > 0

def sendEmail(debug):
    bodyf = open("recents.txt", "r+")
    body = []
    nextl = bodyf.readline()
    body.append(nextl)
    while len(nextl) > 0:
        print(nextl)
        nextl = bodyf.readline()
        body.append(nextl)
    bodyf.close()
    bodyf = open("recents.txt", "w+")
    bodyf.write("")
    bodyf.close()
    if debug:
        for r in debrecipients:
            smtp.send(body, r)
    else:
        for r in recipients:
            smtp.send(body, r)
    return 0

def check(deb):
    tBool = isItTime(deb)
    print(str(tBool))
    tFound = sitesFound()
    print(str(tFound))
    if tBool & tFound:
        sendEmail(deb)
    return 0

def main():
    check(True)
    return 0

if __name__ == "__main__":
    main()
