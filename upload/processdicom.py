import dicom
import os
import numpy
import matplotlib as mpl
mpl.use('Agg')
import pylab

class processdicom(object):
	""" A class of processing DICOM image files"""
	
	def __init__(self, filepath):
		self.dicom = dicom.read_file(filepath)
		pylab.imshow(self.dicom.pixel_array, cmap=pylab.cm.bone)
		pylab.gca().xaxis.set_visible(False)
		pylab.gca().yaxis.set_visible(False)

	def writeFiles(self, directory, filename):
		if not os.path.exists(directory):
			os.makedirs(directory)
		pylab.savefig(directory + "/" + filename + ".tif", bbox_inches='tight')
		pylab.savefig(directory + "/" + filename + ".png", bbox_inches='tight')
		self.dicom.save_as(directory + "/" + filename + ".dcm")

	def getdict(self):
		ddict = {}
		for key in self.dicom.dir():
			ddict[key] = self.dicom.get(key) 
		return ddict
