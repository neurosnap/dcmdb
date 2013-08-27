$(function() {
	
	$('#fineuploader-s3').fineUploaderS3({
      "request": {
        // REQUIRED: We are using a custom domain
        // for our S3 bucket, in this case.  You can
        // use any valid URL that points to your bucket.
        //https://s3.amazonaws.com/dcmdb.org/
        //dcmdb.org.s3-website-us-east-1.amazonaws.com
        "endpoint": "https://s3.amazonaws.com/dcmdb.org/",

        // REQUIRED: The AWS public key for the client-side user
        // we provisioned.
        "accessKey": "AKIAITUKA4QJV4JFOK4A"
      },

      // REQUIRED: Path to our local server where requests
      // can be signed.
      "signature": {
          "endpoint": "/dcmupload/signature"
      },

      // OPTIONAL: An endopint for Fine Uploader to POST to
      // after the file has been successfully uploaded.
      // Server-side, we can declare this upload a failure
      // if something is wrong with the file.
      "uploadSuccess": {
          "endpoint": "/dcmupload/success"
      },

      "callbacks": {
        "": function() {},
        "onComplete": function(id, name, json, xhr) {
            console.log(id);
            console.log(name);
            console.log(json);
        }
      },

      // USUALLY REQUIRED: Blank file on the same domain
      // as this page, for IE9 and older support.
      "iframeSupport": {
          "localBlankPagePath": "/dcmupload/blank"
      },

      // optional feature
      "retry": {
          "showButton": true
      },

      // optional feature
      "chunking": {
          "enabled": true
      },

      // optional feature
      "resume": {
          "enabled": true
      },

      "text": {
		      "uploadButton": '<div><i class="icon-upload icon-white"></i> Click or Drop DICOM to Upload!</div>'
      },

      "template": '<div class="qq-uploader span8">' +
                      '<pre class="qq-upload-drop-area span12"><span>Drop DICOM Here!</span></pre>' +
                      '<div class="qq-upload-button btn btn-info" style="width: auto;">{uploadButtonText}</div>' +
                      '<span class="qq-drop-processing"><span>Processing ...</span><span class="qq-drop-processing-spinner"></span></span>' +
                      '<ul class="qq-upload-list" style="margin-top: 10px; text-align: center;"></ul>' +
                    '</div>',
      "classes": {
        "success": 'alert alert-success',
        "fail": 'alert alert-error'
       },

       "validation": {
            "allowedExtensions": ["dcm"]
       }
  
    });

});
