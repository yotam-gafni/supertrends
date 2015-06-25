# --------------------------------------------------------------------------
# Stores.py
#
# represent a store
#
# Author: Nir Moshe (nirmo)
# Date: 21 - Jun - 2015
#
# --------------------------------------------------------------------------
import sys, os, glob
import xml.etree.ElementTree as ET

class Store:
	def __init__(self, parent, store_id, Bikoret_No, StoreType, StoreName, Address, City, ZipCode):
		self.parent = parent
		self.store_id = store_id
		self.Address = Address
		self.City = City
		self.ZipCode = ZipCode

	def  getAdress(self):
		return u"%s, %s" % (self.City, self.Address)

	def getParent(self):
		return self.parent

	def __hash__(self):
		return hash(self.getAdress())

class StoreContainer:
	def __init__(self, seq, superMarketName, supreid):
		self.seq = set(seq)
		self.superMarketName = superMarketName
		self.supreid = supreid

	def dump(self, output):
		r=''
		for store in self.seq:
			r += "['%s', '%s', %d], \n" % (store.getAdress().encode("utf-8"),
									   	   self.superMarketName.encode("utf-8"),
									   	   self.supreid)
		s = "['Address', 'Name', 'SUPER ID'],\n%s" %  (r)
		with open(output, "a") as out:
			out.write(s)


def StoresFactory(xmlfile, _id):
	"""
	build a list of stores from an xml file
	"""
	tree = ET.parse(xmlfile)
	root = tree.getroot()
	superName = root.iter('ChainName').next().text
	res = []
	for store in root.iter('Store'):
		res.append(Store(_id, *[child.text for child in store]))
	return StoreContainer(res, superName, _id)


if __name__ == "__main__":
	i = 0
	for xm in glob.glob(os.path.join(sys.argv[1], "*.xml")):
		sl = StoresFactory(xm, i)
		i += 1
		sl.dump("stores.txt")
