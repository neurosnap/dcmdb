$(function() {

		var maxFiles = 20;
		// 5 MB
		var maxFileSize = 5 * Math.pow(2, 20);

		$("#send_files").prop("disabled", true);

		$("#accept_tos").on("click", function() {

				if ($(this).is(":checked")) {
						$("#send_files").prop("disabled", false);
						$(".file_upload").prop("disabled", false);
				} else {
						$("#send_files").prop("disabled", true);
						$(".file_upload").prop("disabled", true);
				}

		});

		$("#send_files").on("click", function() {
			$(".file_upload").click();
		});

		$("#clear_files").on("click", function() {
			if ($(".file_cancel").length > 0)
				$(".file_cancel").click();
		});

		$('#fileupload').fileupload({
				"url": "/dcmupload/handle_upload",
				"dataType": 'json',
				"maxNumberOfFiles": maxFiles,
				"limitConcurrentUploads": 3,
				"submit": function(event, files) {

						var fileCount = files.originalFiles.length;

						if (fileCount > maxFiles) {

								alert("The maximum number of files is " + maxFiles);

								throw 'This is not an error. This is just to abort javascript';

								return false;

						}

				},
				"add": function(e, data) {

						var content = '';
						for (var i = 0; i < data.files.length; i++) {

								var file = data.files[i];

								var bytes_ts = '';

								if (file.hasOwnProperty("size"))
										bytes_ts = bytesToSize(parseInt(file.size));

									content += '<div class="queued" dcm_name="' + file.name + '">' + 
														 '    <div><span class="dcm_done" style="display: none;"></span>' + 
														 '        ' + file.name + ' <strong>' + bytes_ts + '</strong>' + 
														 '    		<button type="button" style="margin-bottom: 5px;" class="btn btn-primary file_upload"><span class="glyphicon glyphicon-upload"></span> Upload</button>' +
														 '    		<button type="button" style="margin-bottom: 5px;" class="btn btn-danger file_cancel"><span class="glyphicon glyphicon-ban-circle"></span> Remove</button>' +
														 '    </div> ' + 
														 '    <div class="progress"><div class="progress-bar"></div></div>' + 
														 '    <div class="dcm_preview"></div>' + 
														 '<hr />' + 
														 '</div>';
						} 

						$("#display_uploads").append(content);

						$(".file_cancel").eq(-1).on("click", function() {

								$(this).parent().parent().remove();

						});

						if (!$("#accept_tos").is(":checked"))
							$(".file_upload").prop("disabled", true);

						$(".file_upload").eq(-1).on("click", function() {

								data.submit();

						});

				},
				"progress": function (e, data) {

						var progress = parseInt(data.loaded / data.total * 100, 10);

						$(".queued").each(function() {

								for (var i = 0; i < data.files.length; i++) {
										if (data.files[i].name == $(this).attr("dcm_name")) {
												$(this).find(".progress-bar").css("width", progress + "%");
										}
								}

						});

				},
				"progressall": function(e, data) {

						var progress = parseInt(data.loaded / data.total * 100, 10);

						$('#progress .progress-bar').css(
								'width',
								progress + '%'
						);

				},
				"done": function(e, data) {

						$.each(data.result, function (index, file) {

								$(".queued").each(function() {

										if (file.name == $(this).attr("dcm_name")) {

												$(this).find(".dcm_done").show();

												if (file.hasOwnProperty("success") && !file.success) {
														$(this).find(".dcm_preview").html('<div class="alert alert-danger">' + file.msg + '</div>');
												} else if (file.hasOwnProperty("error")) {

														if (file.error == "maxFileSize")
																$(this).find(".dcm_preview").html('<div class="alert alert-danger">Exceeded maximum file size, upload failed.</div>');
														else
																$(this).find(".dcm_preview").html('<div class="alert alert-danger">' + file.error + '</div>');
												
												} else {
														$(this).find(".dcm_preview").html('<a href="/dcmview/viewer/' + file.image_uid + '">View DCM</a><img src="' + file.file_name + '_thumb.png" style="margin-left: 15px;" />');
												}

										}

								});

						});

						//$("#send_files").prop("disabled", true);

				}
		});

});

function bytesToSize(bytes) {

		var sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];

		if (bytes == 0) 
				return '0 Bytes';

		var i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));

		return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];

};