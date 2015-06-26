#-------------------------------------------------------------------------------
# Name:        parseStores
# Purpose:
#
# Author:      nirmo
#
# Created:     26/06/2015
# Copyright:   (c) nirmo 2015
#-------------------------------------------------------------------------------
import sys
import urllib2
from urllib import urlencode
import xml.etree.ElementTree as ET

def getCoordinates(address):
    u = urlencode({'address' : address.encode("utf8")})
    loc = urllib2.urlopen("http://maps.google.com/maps/api/geocode/xml?%s&sensor=false" % u)
    tree = ET.parse(loc)
    root = tree.getroot()
    r = {}
    for item in root.iter('location'):
        for i in item:
            r[i.tag] = float(i.text)
    return r

def generateItemDict(store):
    fields = {
        'StoreId' : int,
        'Address' : None,
        'City' : None,
        'ChainName': None,
        'SubChainName' : None
    }

    ret = {}
    for i in store.iter():
        if i.tag in fields:
            ret[i.tag] = fields[i.tag](i.text) if fields[i.tag] else i.text
    ret.update(getCoordinates(u"%s, %s" % (ret["City"], ret['Address'])))
    return ret

def parseStores(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    return (generateItemDict(item) for item in root.iter('Store'))


def usage():
    print "%s usage:" % (__file__)
    print "\t%s <StoresFull*.xml>" % (__file__)

def main():
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)


    res = u''
    c = 0
    for i in parseStores(sys.argv[1]):
        try:
            print i
            res += u"""[%f, %f, "%s", 'FILL'],\n""" % (i['lat'], i['lng'], i['Address'])
        except:
            pass
        c += 1
        if c == 10:
            break

    with open('tmp.txt', "wb") as f:
        f.write(res.encode("utf8"))

if __name__ == "__main__":
    main()
