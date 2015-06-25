# --------------------------------------------------------------------------
# FTPCrawler.py
#
# Download all the supermarket information.
#
# Author: Nir Moshe (nirmo)
# Date: 19 - Jun - 2015
#
# --------------------------------------------------------------------------

import time
import Queue
from ftplib import  FTP_TLS

class SuperMarketID:
	def __init__(self, user, passwd, desc):
		self.user = user
		self.passwd = passwd
		self.desc = desc

class FTPFile:
	def __init__(self, permissions, num, user, goup, size, month, day, _time, filename):
		self.permissions = permissions
		self.size = size
		self.month = month
		self.day = day
		self._time = time
		self.filename = filename


FTP_DB = {
	'url.retail.publishedprices.co.il' : [
		SuperMarketID("TivTaam", "", ""),
		SuperMarketID("doralon", "", ""),
		SuperMarketID("osherad", "", ""),
		SuperMarketID("HaziHinam", "", ""),
		SuperMarketID("Keshet", "", ""),
		SuperMarketID("RamiLevi", "", ""),
		SuperMarketID("SuperDosh", "", ""),
		SuperMarketID("yohananof", "", ""),
		SuperMarketID("freshmarket_sn", "f_efrd", ""),
	]
}

class Log:
	def __init__(self, logfile):
		self.buffer = Queue.Queue()
		self.logfile = logfile

	def log(self, line):
		self.buffer.put("%s : %s" % (time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()), line))
		print self.buffer.get()

	def error(self, line):
		self.log("[ERROR]: %s" % line)

class FTPCrawler:
	def __init__(self, db, output_directory, logfile=None, number_of_threads=0):
		self.nthreads = number_of_threads
		self.db = db
		self.output = output_directory
		self.log = Log(logfile)

	def parseFiles(self, files):
		allfiles = []
		for res in files.split("\n"):
			try:
				allfiles.append(FTPFile(*[word for word in res.split(" ") if word]))
			except:
				self.log.error("Invalid line : %s!" % res)

		for f in allfiles:
			self.log.log("Download %s..." % (f.filename))

	def start(self):
		# create connection
		for ftpserver, users in self.db.iteritems():
			for s_user in users:
				self.log.log("Connecting to %s: user: %s pass: %s" % (ftpserver, s_user.user, s_user.passwd))
				ftp = FTP_TLS(ftpserver)     # connect to host, default port
				ftp.login(user=s_user.user, passwd=s_user.passwd) 
				ftp.prot_p()          # switch to secure data connection
				ftp.retrlines('LIST', self.parseFiles)
				self.log.log("Done! now quit...")
				ftp.quit()


def main():
	ftc = FTPCrawler(FTP_DB, None)
	ftc.start()

if  __name__ == "__main__":
	main()