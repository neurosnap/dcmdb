import dicom
import numpy
import matplotlib as mpl
mpl.use('Agg')
import pylab

class processDicom(object):
	""" A class of processing DICOM image files"""
	def __init__(self, filepath):
		self.dicom = dicom.read_file(filepath)
	
	def display(self):
		pylab.imshow(self.dicom.pixel_array, cmap=pylab.cm.bone)
		pylab.savefig('C:\\foo.tif')

mydicom = processDicom("C:\\Users\\716211\\Desktop\\kaze\\git\\dicom\\upload\\dicoms\\eric\\brain_images\\001.dcm")
mydicom.display()
