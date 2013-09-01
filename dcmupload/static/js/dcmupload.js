$(function() {

    $('#fileupload').fileupload({
        "url": "/dcmupload/handle_upload",
        "dataType": 'json',
        "done": function (e, data) {

            $.each(data.result.files, function (index, file) {
                $('<p/>').text(file.name).appendTo(document.body);
            });

        },
        "autoUpload": true/*, 
        "progressall": function (e, data) {
            
            var progress = parseInt(data.loaded / data.total * 100, 10);
            
            $('#progress .bar').css(
                'width',
                progress + '%'
            );

        }*/
    });

});
