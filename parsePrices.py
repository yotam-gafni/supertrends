#-------------------------------------------------------------------------------
# Name:        parsePrices
# Purpose:
#
# Author:      nirmo
#
# Created:     25/06/2015
# Copyright:   (c) nirmo 2015
#-------------------------------------------------------------------------------

import gzip
import sys, time, os
import xml.etree.ElementTree as ET

def getStoreId(gzfile):
    b = os.path.basename(gzfile)
    return int(b.split("-")[1])

def generateItemDict(item, storeID, supermarket):
    fields = {
        'ItemCode' : int,
        'ItemPrice' : float,
        'ItemName' : None
    }
    ret = {
        'StoreId' : storeID,
        'Time' : time.time(),
        "Supermarket" : supermarket
    }

    for i in item.iter():
        if i.tag in fields:
            ret[i.tag] = fields[i.tag](i.text) if fields[i.tag] else i.text
    return ret

def parseFile(gzfile, supermarket):
    storeID = getStoreId(gzfile)
    with gzip.open(gzfile) as gz:
        tree = ET.parse(gz)
        root = tree.getroot()
        return (generateItemDict(item, storeID, supermarket)
            for item in root.iter('Item'))


def usage():
    print "%s usage:" % (__file__)
    print "\t%s <PriceFull*.gz> <supermarket name>" % (__file__)

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)

    c = 0
    for i in parseFile(sys.argv[1], sys.argv[2]):
        print i
        c += 1
        if c == 100:
            exit(1)


if __name__ == '__main__':
    main()