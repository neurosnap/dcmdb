import dicom
import os
import numpy
import matplotlib as mpl
mpl.use('Agg')
import pylab

class processdicom(object):
	""" A class of processing DICOM image files"""
	
	def __init__(self, dicom):
		#self.dicom = dicom.read_file(filepath)
		self.dicom = dicom

	def writeFiles(self, directory, filename):

		try:
			pxl_arr = self.dicom.pixel_array
		except:
			return { "success": False, "error": "Unsuppported transfer syntax " + self.transferSyntax(self.dicom.file_meta.TransferSyntaxUID) }

		pylab.imshow(pxl_arr, cmap = pylab.cm.bone)

		pylab.gca().xaxis.set_visible(False)
		pylab.gca().yaxis.set_visible(False)

		if not os.path.exists(directory):
			os.makedirs(directory)

		#pylab.savefig(directory + "/" + filename + ".tif", bbox_inches='tight')
		pylab.savefig(directory + "/" + filename + ".png", bbox_inches = 'tight')
		self.dicom.save_as(directory + "/" + filename + ".dcm")

		return { "success": True, "dicom": self.dicom }

	def transferSyntax(self, transferSyntaxUID):

		transfer_syntax = {
			"1.2.840.10008.1.2": "Implicit VR Endian: Default Transfer Syntax for DICOM",
			"1.2.840.10008.1.2.1": "Explicit VR Little Endian",
			"1.2.840.10008.1.2.1.99": "Deflated Explicit VR Big Endian",	
			"1.2.840.10008.1.2.2": "Explicit VR Big Endian",
			"1.2.840.10008.1.2.4.50": "JPEG Baseline (Process 1): Default Transfer Syntax for Lossy JPEG 8-bit Image Compression",
			"1.2.840.10008.1.2.4.51": "JPEG Baseline (Processes 2 & 4): Default Transfer Syntax for Lossy JPEG 12-bit Image Compression (Process 4 only)",
			"1.2.840.10008.1.2.4.57": "JPEG Lossless, Nonhierarchical (Processes 14)",
			"1.2.840.10008.1.2.4.70": "JPEG Lossless, Nonhierarchical, First- Order Prediction (Processes 14 [Selection Value 1]): Default Transfer Syntax for Lossless JPEG Image Compression",
			"1.2.840.10008.1.2.4.80": "JPEG-LS Lossless Image Compression",
			"1.2.840.10008.1.2.4.81": "JPEG-LS Lossy (Near- Lossless) Image Compression",
			"1.2.840.10008.1.2.4.90": "JPEG 2000 Image Compression (Lossless Only)",
			"1.2.840.10008.1.2.4.91": "JPEG 2000 Image Compression",
			"1.2.840.10008.1.2.4.92": "JPEG 2000 Part 2 Multicomponent Image Compression (Lossless Only)",
			"1.2.840.10008.1.2.4.93": "JPEG 2000 Part 2 Multicomponent Image Compression",
			"1.2.840.10008.1.2.4.94": "JPIP Referenced",
			"1.2.840.10008.1.2.4.95": "JPIP Referenced Deflate",
			"1.2.840.10008.1.2.5": "RLE Lossless",
			"1.2.840.10008.1.2.6.1": "RFC 2557 MIME Encapsulation",
			"1.2.840.10008.1.2.4.100": "MPEG2 Main Profile Main Level",
			"1.2.840.10008.1.2.4.102": "MPEG-4 AVC/H.264 High Profile / Level 4.1",
			"1.2.840.10008.1.2.4.103": "MPEG-4 AVC/H.264 BD-compatible High Profile / Level 4.1"
		}

		if transferSyntaxUID in transfer_syntax:
			return transfer_syntax[transferSyntaxUID]
		else:
			return transferSyntaxUID

	def getdict(self):

		ddict = {}

		for key in self.dicom.dir():
			ddict[key] = self.dicom.get(key) 

		return ddict
