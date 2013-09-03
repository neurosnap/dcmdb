$(function() {

    $('#fileupload').fileupload({
        "url": "/dcmupload/handle_upload",
        "dataType": 'json',
        "add": function(e, data) {

            var content = '';
            for (var i = 0; i < data.files.length; i++) {

                var file = data.files[i];

                content += '<div class="queued" dcm_name="' + file.name + '">' + 
                           '    <div><span class="dcm_done fui-check-inverted" style="display: none;"></span>' + 
                           '        ' + file.name + ' - ' + file.type + ' - ' + file.size + 
                           '    </div>' +
                           '    <div class="progress"><div class="bar"></div></div>' + 
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
                        $(this).find(".bar").css("width", progress + "%");
                    }
                }

            });

        },
        "progressall": function(e, data) {

            var progress = parseInt(data.loaded / data.total * 100, 10);

            $('#progress .bar').css(
                'width',
                progress + '%'
            );

        },
        "done": function(e, data) {

            $.each(data.result, function (index, file) {
                $(".queued").each(function() {
                    if (file.name == $(this).attr("dcm_name")) {
                        $(this).find(".dcm_done").show();
                        $(this).find(".dcm_preview").html('<a href="/dcmview/">View DCM</a><img src="' + file.file_name + '" style="height: 150px; width: 150px;" />');
                    }
                })
            });

        }
    });

});
