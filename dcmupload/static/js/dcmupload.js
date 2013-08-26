$(function() {
	
	$('#fineuploader-s3').fineUploaderS3({
      "request": {
          // REQUIRED: We are using a custom domain
          // for our S3 bucket, in this case.  You can
          // use any valid URL that points to your bucket.
          "endpoint": "dicoms.s3-website-us-east-1.amazonaws.com",

          // REQUIRED: The AWS public key for the client-side user
          // we provisioned.
          "accessKey": "AKIAITUKA4QJV4JFOK4A"
      },

      // REQUIRED: Path to our local server where requests
      // can be signed.
      "signature": {
          "endpoint": "/s3demo.php"
      },

      // OPTIONAL: An endopint for Fine Uploader to POST to
      // after the file has been successfully uploaded.
      // Server-side, we can declare this upload a failure
      // if something is wrong with the file.
      "uploadSuccess": {
          "endpoint": "/s3demo.php?success"
      },

      // USUALLY REQUIRED: Blank file on the same domain
      // as this page, for IE9 and older support.
      "iframeSupport": {
          "localBlankPagePath": "/server/success.html"
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
		"uploadButton": '<div><i class="icon-upload icon-white"></i> Upload a file!</div>'
      },

      "template": '<div class="qq-uploader span8">' +
                      '<pre class="qq-upload-drop-area span12"><span>{dragZoneText}</span></pre>' +
                      '<div class="qq-upload-button btn btn-success" style="width: auto;">{uploadButtonText}</div>' +
                      '<span class="qq-drop-processing"><span>{dropProcessingText}</span><span class="qq-drop-processing-spinner"></span></span>' +
                      '<ul class="qq-upload-list" style="margin-top: 10px; text-align: center;"></ul>' +
                    '</div>',
      "classes": {
      	"success": 'alert alert-success',
        "fail": 'alert alert-error'
       }
  });

});
