from __future__ import division
import subprocess

try:

	import gdcm
	import numpy
	from pylab import cm 
	from PIL import Image

except:

	#import error but I'm handling the error inside extractImage()
	pass

class dcmproc(object):

	""" A class using GDCM to attempt to extract an image and thumbnail from a DICOM file as well as validate it with dciodvfy """

	def __init__(self, filename):

		self.filename = filename
		self.png_filename = self.filename.replace(' ', '')[:-4] + ".png"

		self.gdcm = gdcm

		self.img_read = self.gdcm.ImageReader()
		self.img_read.SetFileName(self.filename.encode('utf-8'))

		self.pxl_arr = None

	def getGDCM(self):

		return self.gdcm

	def validate(self):

		""" Validates DICOM file using dciodvfy """

		cmd = ["dciodvfy", self.filename]

		return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr = subprocess.PIPE).communicate()

	def extractImage(self):

		""" Extracts an image and a thumbnail of that image from a DICOM file and saves it as a PNG """

		if not self.module_exists("gdcm"):
			return { "success": False, "msg": "Image extraction failed: missing GDCM module." }
		elif not self.module_exists("numpy"):
			return { "success": False, "msg": "Image extraction failed: missing numpy module." }
		elif not self.module_exists("pylab"):
			return { "success": False, "msg": "Image extraction failed, missing matplotlib: pylab module." }
		elif not self.module_exists("PIL"):
			return { "success": False, "msg": "Image extraction failed, missing PIL module." }

		if not self.img_read.Read():
			return { "success": False, "msg": "Could not read DICOM file." }

		try:
			self.pxl_arr = self.gdcm_to_numpy(self.img_read.GetImage())
		except:
			return { "success": False, "msg": "Could not convert DICOM pixel array into a numpy array." }

		try:
			# save normal resolution image
			self.imsave(fname = self.png_filename, arr = self.pxl_arr, cmap = cm.bone)
			
			# save thumbnail via PIL
			try:
				pil = Image.open(self.png_filename)
			except:
				return { "success": False, "msg": "Image could not be loaded into PIL." }

			try:
				thumb_size = 150, 150
				pil.thumbnail(thumb_size, Image.ANTIALIAS)
			except:
				return { "success": False, "msg": "Image could not be resized using PIL." }
			
			try:
				pil.save(self.png_filename[:-4] + "_thumb.png", "PNG")
			except:
				return { "success": False, "msg": "Thumbnail could not be saved." }

		except:
			return { "success": False, "msg": "Could not save image." }

		return { "success": True }

	def get_gdcm_to_numpy_typemap(self):
		"""Returns the GDCM Pixel Format to numpy array type mapping."""

		_gdcm_np = {
			gdcm.PixelFormat.UINT8  :numpy.int8,
			gdcm.PixelFormat.INT8   :numpy.uint8,
			gdcm.PixelFormat.UINT16 :numpy.uint16,
			gdcm.PixelFormat.INT16  :numpy.int16,
			gdcm.PixelFormat.UINT32 :numpy.uint32,
			gdcm.PixelFormat.INT32  :numpy.int32,
			gdcm.PixelFormat.FLOAT32:numpy.float32,
			gdcm.PixelFormat.FLOAT64:numpy.float64 
		}

		return _gdcm_np

	def get_numpy_array_type(self, gdcm_pixel_format):
		""" Returns a numpy array typecode given a GDCM Pixel Format. """
		
		return self.get_gdcm_to_numpy_typemap()[gdcm_pixel_format]

	def gdcm_to_numpy(self, image):
		""" Converts a GDCM image to a numpy array. """
		
		pf = image.GetPixelFormat().GetScalarType()

		assert pf in self.get_gdcm_to_numpy_typemap().keys(), \
			"Unsupported array type %s"%pf

		#d = image.GetDimension(0), image.GetDimension(1)
		d = image.GetDimension(1), image.GetDimension(0)

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
		#fig.set_size_inches(5.12, 5.12)
		canvas = FigureCanvas(fig)
		fig.figimage(arr, cmap=cmap, vmin=vmin, vmax=vmax, origin=origin)
		fig.savefig(fname, dpi=1, format=format)

	def module_exists(self, module_name):

		try:
			__import__(module_name)
		except ImportError:
			return False
		else:
			return True