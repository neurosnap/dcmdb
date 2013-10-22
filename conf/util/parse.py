import dicom
import sys
import os

class parsedcms(object):
	def __init__(self, path):
		self.path = path
	def getfiles(self):
		self.files = []
		for files in os.walk(self.path).next()[2]:
			self.files.append(self.path + '/' + files)

	def buildstatistics(self):
		self.statistics = {}
		for fil in self.files:
			try:
				dcm = dicom.read_file(fil)

				for labels in dcm.dir():
					if labels in self.statistics:
						self.statistics[labels] += 1
					else:
						self.statistics[labels] = 1
			except:
				pass	
	# end buldstatistics

	def printstatistics(self):
		print ('key, value')
#		for key, value in iter(sorted(self.statistics.iteritems())):
		for key, value in sorted(self.statistics.items() ,key = lambda x: x[1]):
			print("%s,%s" % (key, value))
	

path = os.path.dirname(os.path.abspath(__file__)) + '/dcms'
pdcms = parsedcms(path)
pdcms.getfiles()
pdcms.buildstatistics()
pdcms.printstatistics()
