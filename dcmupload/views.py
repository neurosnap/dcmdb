# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpRequest
from django.template import RequestContext
#ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
#Force CSRF Cookie
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from dcmupload.models import Study, Series, Image
from dcmupload.processdicom import processdicom

import json as simplejson
import random
import string
import re
import dicom
import os

BASE_DIR = settings.BASE_DIR
MEDIA_DIR = settings.MEDIA_ROOT

@ensure_csrf_cookie
def dcmupload(request):

	context = {}

	return render_to_response('dcmupload.html', context, context_instance = RequestContext(request))

@csrf_exempt
def blank(request):

	context = {}

	return render_to_response('blank.html', context, context_instance = RequestContext(request))

@csrf_exempt
def handle_upload(request):

     # used to generate random unique id
    import uuid

    # settings for the file upload
    #   you can define other parameters here
    #   and check validity late in the code
    options = {
        # the maximum file size (must be in bytes)
        "maxfilesize": 3 * 2 ** 20, # 15 Mb
        # the minimum file size (must be in bytes)
        "minfilesize": 1 * 2 ** 10, # 1 Kb
        # the file types which are going to be allowed for upload
        #   must be a mimetype
        "acceptedformats": (
            "application/dicom",
            "image/dicom",
            "image/x-dicom",
            "application/octet-stream",
            "application/x-rar-compressed",
            "application/zip",
        )
    }


    # POST request
    #   meaning user has triggered an upload action
    if request.method == 'POST':
        # figure out the path where files will be uploaded to
        temp_path = MEDIA_DIR

        # if 'f' query parameter is not specified
        # file is being uploaded
        if not ("f" in request.GET.keys()): # upload file

            # QUIRK HERE
            # in jQuey uploader, when it falls back to uploading using iFrames
            # the response content type has to be text/html
            # if json will be send, error will occur
            # if iframe is sending the request, it's headers are a little different compared
            # to the jQuery ajax request
            # they have different set of HTTP_ACCEPT values
            # so if the text/html is present, file was uploaded using jFrame because
            # that value is not in the set when uploaded by XHR
            if "text/html" in request.META['HTTP_ACCEPT']:
                response_type = "text/html"
            else:
                response_type = "application/json"

            print response_type

            # make sure some files have been uploaded
            if not request.FILES:
                return HttpResponseBadRequest('Must upload a file')

            # get the uploaded file
            file = request.FILES[u'files[]']

            # initialize the error
            # If error occurs, this will have the string error message so
            # uploader can display the appropriate message
            error = False

            # check against options for errors

            # file size
            if file.size > options["maxfilesize"]:
                error = "maxFileSize"
            if file.size < options["minfilesize"]:
                error = "minFileSize"
                # allowed file type
            if file.content_type not in options["acceptedformats"]:
                error = "acceptFileTypes"

            # the response data which will be returned to the uploader as json
            response_data = {
                "name": file.name,
                "size": file.size,
                "type": file.content_type
            }

            # if there was an error, add error message to response_data and return
            if error:
                # append error message
                response_data["error"] = error
                # generate json
                response_data = simplejson.dumps([response_data])
                # return response to uploader with error
                # so it can display error message
                return HttpResponse(response_data, mimetype=response_type)


            # make temporary dir if not exists already
            if not os.path.exists(temp_path):
                os.makedirs(temp_path)

            # get the absolute path of where the uploaded file will be saved
            # all add some random data to the filename in order to avoid conflicts
            # when user tries to upload two files with same filename
            file_name = str(uuid.uuid4())

            if not file_name.endswith(".dcm"):
                file_name = file_name + '.dcm'

            filename = os.path.join(temp_path, file_name)

            # open the file handler with write binary mode
            destination = open(filename, "wb+")
            # save file data into the disk
            # use the chunk method in case the file is too big
            # in order not to clutter the system memory
            for chunk in file.chunks():
                destination.write(chunk)
                # close the file

            destination.close()

            # strip patient data
            try:
                anonymize(filename, filename)
            except:
                #delete the file
                os.remove(filename)
                #throw an error to client
                return HttpResponse(simplejson.dumps([{ 
                    "success": False, 
                    "msg": "Missing required DICM marker, are you sure this is a DICOM file?", 
                    "name": file.name
                }]), mimetype=response_type)

            dcm = processdicom(filename = filename)

            #Save 
            args = {
                "dcm": dcm.getDCM(),
                "filename": file_name[:-4],
                "request": request,
            }

            new_series = add_dcm_record(**args)

            if not new_series['success']:
                #remove recently uploaded dcm file
                os.remove(filename)

                return HttpResponse(simplejson.dumps([{ 
                    "success": False, 
                    "msg": "DCM already found in database. <a href='/dcmview/series/" + new_series['series'].UID + "'>View DCM</a>", 
                    "name": file.name, 
                    "image_uid": new_series['image'].UID,
                    "series_uid": new_series['series'].UID, 
                    "study_uid": new_series['study'].UID 
                }]), mimetype=response_type)

            #save image and thumbnail
            save_image = dcm.extractImage(filename)
            
            if save_image['success']:
                # set image generated flag to true in series record
                new_series['image'].image_gen = True
                new_series['image'].save()

            #not able to save images?  return an error with the saved DCM file
            else:

                save_image['image_uid'] = new_series['image'].UID
                save_image['series_uid'] = new_series['series'].UID
                save_image['study_uid'] = new_series['study'].UID 
                save_image['msg'] += " <a href='/dcmview/series/" + new_series['series'].UID + "'>View DCM</a>" 
                save_image['name'] = file.name
                
                return HttpResponse(simplejson.dumps([save_image]), mimetype=response_type)

            response_data['file_name'] = "/media/" + file_name[:-4]
            
            response_data['image_uid'] = new_series['image'].UID
            response_data['study_uid'] = new_series['study'].UID
            response_data['series_uid'] = new_series['series'].UID

            # allows to generate properly formatted and escaped url queries
            import urllib

            # generate the json data
            response_data = simplejson.dumps([response_data])

            # return the data to the uploading plugin
            return HttpResponse(response_data, mimetype=response_type)

#Creates a new record in our database for the DICOM file
#Right now we hard-coded a list of keys we are interested in
def add_dcm_record(**kwargs):

    #dcm, dcm_dir, filename, title, public, request, study

    # Study
    study_instance_uid = None
    study_id = None
    study_date = None
    study_time = None
    accession_number = None
    study_description = None
    sop_class_uid = None
    # Series
    series_instance_uid = None
    series_description = None
    modality = None
    institution_name = None
    manufacturer = None
    series_number = None
    laterality = None
    series_date = None
    body_part_examined = None
    # Image
    sop_instance_uid = None
    image_number = None
    patient_position = None
    content_date = None
    content_time = None
    transfer_syntax_uid = None

    dcm = kwargs['dcm']
    
    for tag in dcm.dir():

        if tag == "Modality":
            modality = dcm.Modality
        elif tag == "InstitutionName":
            institution_name = dcm.InstitutionName
            institution_name = institution_name.decode('utf-8')
        elif tag == "Manufacturer":
            manufacturer = dcm.Manufacturer
        elif tag == "StudyID":
            study_id = dcm.StudyID
        elif tag == "StudyDescription":
            study_description = dcm.StudyDescription
            study_description = ""
            # study_description = study_description.decode('utf-8')
        elif tag == "StudyDate":
            study_date = dcm.StudyDate
            study_date = convert_date(study_date, "-").encode('utf-8')
        elif tag == "StudyTime":
            study_time = dcm.StudyTime
        elif tag == "StudyInstanceUID":
            # unique identifier for the study
            study_instance_uid = dcm.StudyInstanceUID
        elif tag == "SOPInstanceUID":
            # unique identifier for the image
            sop_instance_uid = dcm.SOPInstanceUID
        elif tag == "SOPClassUID":
            sop_class_uid = dcm.SOPClassUID
        elif tag == "InstanceNumber":
            image_number = int(dcm.InstanceNumber)
        elif tag == "AccessionNumber":
            accession_number = dcm.AccessionNumber
        elif tag == "SeriesInstanceUID":
            # unique identifier for the series
            series_instance_uid = dcm.SeriesInstanceUID.encode('utf-8')
        elif tag == "SeriesNumber":
            series_number = int(dcm.SeriesNumber)
        elif tag == "SeriesDate":
            series_date = dcm.SeriesDate
            series_date = convert_date(series_date, "-").encode('utf-8')
        elif tag == "Laterality":
            laterality = dcm.Laterality
        elif tag == "PatientOrientation":
            patient_position = dcm.PatientOrientation
        elif tag == "ContentDate":
            content_date = dcm.ContentDate
            content_date = convert_date(content_date, "-").encode('utf-8')
        elif tag == "ContentTime":
            content_time = dcm.ContentTime
        elif tag == "BodyPartExamined":
            body_part_examined = dcm.BodyPartExamined
        elif tag == "SeriesDescription":
            series_description = dcm.SeriesDescription

    try:
        transfer_syntax_uid = dcm.file_meta.TransferSyntaxUID
    except:
        pass

    if series_date == None:
        series_date = "1990-01-01"

    if content_date == None:
        content_date = "1990-01-01"

    if content_time == None:
        content_time = "0"

    try:
        study = Study.objects.get(UID = study_instance_uid)

    except (Study.DoesNotExist):

        try:
            study = Study.objects.get(UID = study_instance_uid)

        except:

            study = Study.objects.create(
                    UID = study_instance_uid,
                    study_id = study_id,
                    study_date = study_date,
                    study_time = study_time,
                    accession_number = accession_number,
                    description = study_description,
                    sop_class_uid = sop_class_uid
                )

            study.save()

    try:

        series = Series.objects.get(UID = series_instance_uid)

    except (Series.DoesNotExist):

        try:
            series = Series.objects.get(UID = series_instance_uid)
            
        except:

            series = Series.objects.create(
                dcm_study = study,
                UID = series_instance_uid,
                series_description = series_description,
                modality = modality,
                institution_name = institution_name,
                manufacturer = manufacturer,
                series_number = series_number,
                laterality = laterality,
                body_part_examined = body_part_examined,
                date = series_date
            )

            series.save()

    try:

        image = Image.objects.get(UID = sop_instance_uid)

        return {
            "success": False,
            "image": image,
            "series": series,
            "study": study
        }

    except (Image.DoesNotExist):

        content_time = content_time.decode('utf-8')

        image = Image.objects.create(
            dcm_series = series,
            UID = sop_instance_uid,
            filename = kwargs['filename'],
            transfer_syntax_uid = transfer_syntax_uid,
            content_time = content_time,
            content_date = content_date,
            image_number = image_number,
            #image_position_patient = image_position_patient,
            patient_position = patient_position
            #image_orientation_patient = image_orientation_patient
        )

        image.save()

    return {
        "success": True,
        "image": image,
        "series": series,
        "study": study
    }

# Method that takes a date "20130513" and converts it to "2013-05-13" or whatever
# delimiter inputed
def convert_date(date, delim):

	year = date[:4]
	month = date[4:6]
	day = date[6:8]

	return delim.join([year, month, day])	

def id_generator(size = 6, chars = string.ascii_lowercase + string.digits):

	return ''.join(random.choice(chars) for x in range(size))

def anonymize(filename, output_filename, new_person_name="anonymous",
              new_patient_id="id", remove_curves=True, remove_private_tags=True):
    """Replace data element values to partly anonymize a DICOM file.
    Note: completely anonymizing a DICOM file is very complicated; there
    are many things this example code does not address. USE AT YOUR OWN RISK.
    """

    # Define call-back functions for the dataset.walk() function
    def PN_callback(ds, data_element):
        """Called from the dataset "walk" recursive function for all data elements."""
        if data_element.VR == "PN":
            data_element.value = new_person_name
    def curves_callback(ds, data_element):
        """Called from the dataset "walk" recursive function for all data elements."""
        if data_element.tag.group & 0xFF00 == 0x5000:
            del ds[data_element.tag]
    
    # Load the current dicom file to 'anonymize'
    dataset = dicom.read_file(filename)
    
    # Remove patient name and any other person names
    dataset.walk(PN_callback)
    
    # Change ID
    dataset.PatientID = new_patient_id
    
    # Remove data elements (should only do so if DICOM type 3 optional) 
    # Use general loop so easy to add more later
    # Could also have done: del ds.OtherPatientIDs, etc.
    for name in ['OtherPatientIDs', 'OtherPatientIDsSequence']:
        if name in dataset:
            delattr(dataset, name)

    # Same as above but for blanking data elements that are type 2.
    for name in ['PatientBirthDate']:
        if name in dataset:
            dataset.data_element(name).value = ''
    
    # Remove private tags if function argument says to do so. Same for curves
    if remove_private_tags:
        dataset.remove_private_tags()
    if remove_curves:
        dataset.walk(curves_callback)
        
    # write the 'anonymized' DICOM out under the new filename
    dataset.save_as(output_filename)