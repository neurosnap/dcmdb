import dicom
import os
import gdcm
import numpy
import matplotlib as mpl
mpl.use('Agg')
from pylab import cm 
import matplotlib.pyplot as plt
from PIL import Image

class processdicom(object):
	""" A class of processing DICOM image files"""
	
	def __init__(self, dcm = False, filename = False):
		#self.dicom = dicom.read_file(filepath)
		if dcm:
			self.dicom = dcm
		elif filename:
			self.dicom = dicom.read_file(filename)

		self.img_process = None

	def writeFiles(self, filename):

		png_filename = filename.replace(' ', '')[:-4]

		self.img_process = gdcm.ImageReader()
		self.img_process.SetFileName(filename.encode('utf-8'))

		if not self.img_process.Read():
			return { "success": False, "msg": "Could not read DCM." }

		self.pxl_arr = None

		try:
			self.pxl_arr = self.gdcm_to_numpy(self.img_process.GetImage())
		except:
			return { "success": False, "msg": "Unsuppported transfer syntax " + self.transferSyntax(self.dicom.file_meta.TransferSyntaxUID) }

		try:
			# save normal resolution image
			self.imsave(fname = png_filename + ".png", arr = self.pxl_arr, cmap = cm.bone)
			
			# save thumbnail via PIL
			try:
				pil = Image.open(png_filename + ".png")
			except:
				return { "success": False, "msg": "Image could not be loaded into PIL." }

			try:
				thumb_size = 150, 150
				pil.thumbnail(thumb_size, Image.ANTIALIAS)
			except:
				return { "success": False, "msg": "Image could not be resized using PIL." }
			
			try:
				pil.save(png_filename + "_thumb.png", "PNG")
			except:
				return { "success": False, "msg": "Thumbnail could not be saved." }

		except:
			return { "success": False, "msg": "Could not save image." }

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

	def getDCM(self):
		return self.dicom

	def getdict(self):

		ddict = {}

		for key in self.dicom.dir():
			ddict[key] = self.dicom.get(key) 

		return ddict

	def get_gdcm_to_numpy_typemap(self):
		"""Returns the GDCM Pixel Format to numpy array type mapping."""
		_gdcm_np = {gdcm.PixelFormat.UINT8  :numpy.int8,
					gdcm.PixelFormat.INT8   :numpy.uint8,
					gdcm.PixelFormat.UINT16 :numpy.uint16,
					gdcm.PixelFormat.INT16  :numpy.int16,
					gdcm.PixelFormat.UINT32 :numpy.uint32,
					gdcm.PixelFormat.INT32  :numpy.int32,
					gdcm.PixelFormat.FLOAT32:numpy.float32,
					gdcm.PixelFormat.FLOAT64:numpy.float64 }
		return _gdcm_np

	def get_numpy_array_type(self, gdcm_pixel_format):
		"""Returns a numpy array typecode given a GDCM Pixel Format."""
		return self.get_gdcm_to_numpy_typemap()[gdcm_pixel_format]

	def gdcm_to_numpy(self, image):
		"""Converts a GDCM image to a numpy array.
		"""
		pf = image.GetPixelFormat().GetScalarType()

		assert pf in self.get_gdcm_to_numpy_typemap().keys(), \
			"Unsupported array type %s"%pf

		d = image.GetDimension(0), image.GetDimension(1)

		dtype = self.get_numpy_array_type(pf)
		gdcm_array = image.GetBuffer()
		## use float for accurate scaling
		result = numpy.frombuffer(gdcm_array, dtype=dtype).astype(float)
		## optional gamma scaling
		maxV = float(result[result.argmax()])
		result = result + .5*(maxV-result)
		result = numpy.log(result+50) ## apprx background level
		result.shape = d
		
		return result

	def imsave(self, fname, arr, vmin=None, vmax=None, cmap=None, format=None, origin=None):

		from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
		from matplotlib.figure import Figure

		fig = Figure(figsize=arr.shape[::-1], dpi=1, frameon=False)
		canvas = FigureCanvas(fig)
		fig.figimage(arr, cmap=cmap, vmin=vmin, vmax=vmax, origin=origin)
		fig.savefig(fname, dpi=1, format=format)