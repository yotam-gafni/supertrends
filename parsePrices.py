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
import sys, time, os, glob
import xml.etree.ElementTree as ET
from pymongo import MongoClient
from consts import DBURI

def getStoreId(gzfile):
    b = os.path.basename(gzfile)
    return int(b.split("-")[1])

def getTime(gzfile):
    b = os.path.basename(gzfile)
    p = b.split("-")[2]
    return "%s-%s-%s" % (p[:4], p[4:6], p[6:8])

def generateItemDict(item, storeID, supermarket, _time):
    fields = {
        'ItemCode' : int,
        'ItemPrice' : float,
        'ItemName' : None
    }
    ret = {
        'StoreId' : storeID,
        'Time' : _time,
        "Supermarket" : supermarket
    }

    for i in item.iter():
        if i.tag in fields:
            ret[i.tag] = fields[i.tag](i.text) if fields[i.tag] else i.text
    return ret

def parseFile(gzfile, supermarket):
    storeID = getStoreId(gzfile)
    ti = getTime(gzfile)
    with gzip.open(gzfile) as gz:
        tree = ET.parse(gz)
        root = tree.getroot()
        return (generateItemDict(item, storeID, supermarket, ti)
            for item in root.iter('Item'))


def usage():
    print "%s usage:" % (__file__)
    print "\t%s <PriceFull*.gz> <supermarket name>" % (__file__)

def main():
    if len(sys.argv) != 3:
        usage()
        sys.exit(1)


    coll = MongoClient(DBURI).supertrends.supertrends
    for f in glob.glob(os.path.join(sys.argv[1], "*.gz")):
        print f
        for i in parseFile(f, sys.argv[2]):
            if i['ItemCode'] != 500:
                print i
                coll.insert(i)





if __name__ == '__main__':
    main()