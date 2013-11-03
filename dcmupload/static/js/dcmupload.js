$(function() {

    $("#send_files").prop("disabled", true);

    $("#accept_tos").on("click", function() {

        if ($(this).is(":checked"))
            $("#send_files").prop("disabled", false);
        else
            $("#send_files").prop("disabled", true);

    });

    $('#fileupload').fileupload({
        "url": "/dcmupload/handle_upload",
        "dataType": 'json',
        "add": function(e, data) {

            var content = '';
            for (var i = 0; i < data.files.length; i++) {

                var file = data.files[i];

                console.log(file);

                var bytes_ts = bytesToSize(file.size);

                content += '<div class="queued" dcm_name="' + file.name + '">' + 
                           '    <div><span class="dcm_done" style="display: none;"></span>' + 
                           '        ' + file.name + ' <strong>' + bytes_ts + '</strong>' + 
                           '    </div>' +
                           '    <div class="progress"><div class="progress-bar"></div></div>' + 
                           '    <div class="dcm_preview"></div>' + 
                           '</div>';

            } 

            $("#display_uploads").append(content);

            //$("#send_files").unbind();
            $("#send_files").on("click", function() {

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
                        } else {
                            $(this).find(".dcm_preview").html('<a href="/dcmview/viewer/' + file.image_uid + '">View DCM</a><img src="' + file.file_name + '_thumb.png" style="margin-left: 15px;" />');
                        }

                    }

                });

            });

            $("#send_files").prop("disabled", true);

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