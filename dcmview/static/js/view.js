$(function() {

    console.log(dcm);

    //$('#dcm_tabs a:last').tab('show');

	//dynamically change type to object instead of an array
	dcm.study = dcm.study[0];

    dcm.invert = false;

    $(".breadcrumb").html('<li><a href="/main/explore">Search</a></li><li><a href="/dcmview/study/' + dcm.study.fields.UID + '">Study</a></li><li><a href="/dcmview/series/' + dcm.first_series.fields['UID'] + '">Series</a></li><li>DCM</li>');

	$("#dcm_header").html('<h4>' + dcm.first_series.fields.sop_instance_uid + '</h4>');

	$("#dcmview_image").attr('src', '/media/' + dcm.first_series.fields.filename + '.png');

    //dcm.imageRender();

	var gal_content = '';

	for (var i = 0; i < dcm.series.length; i++) {

		gal_content += '<a href="/dcmview/viewer/' + dcm.series[i].fields.sop_instance_uid + '" class="dcm_series">' + 
					   '	<img src="/media/' + dcm.series[i].fields.filename + '_thumb.png" class="img-thumbnail" style="width: 120px; height: 120px; margin: 2px;" />' + 
					   	'</a>';

	}

	$("#study_gallery").html(gal_content);

    Caman.Event.listen("processComplete", function(job) {
        $("#dcmview_status").html(job.name);
    });

    Caman.Event.listen("renderFinished", function() {
        $("#dcmview_status").html("Render finished!");
    });

	$(".dcm_series").on("click", function(e) {

        $("#dcmview_status").html("Loading ...");

		e.preventDefault();

		var switch_img = $(this).find("img").attr("src").replace("_thumb", "");

        $("#dcmview_image").removeAttr("data-caman-id");

        Caman("#dcmview_image", switch_img, function() {

            dcm.getFilters(this);

            $("#dcmview_status").html("Applying filters ...");

            this.render();

        });

		//$("#dcmview_image").attr('src', switch_img);

         //dcm.imageRender();

		/*$.ajax({
			"url": "/dcmview/series/" + $(this).attr("series_ID"),
			"type": "POST",
			"dataType": "json",
			"success": function(res) {
				dcm.study = res.study;
				dcm.dicom = $.parseJSON(res.dcm);

				dcm.reloadTags();
			}
		});*/

	});



	dcm.reloadTags(true);

    $(".filter").on("keyup", function(e) {

        Caman("#dcmview_image", function() {
            
            var that = this;

            this.revert();

            dcm.getFilters(that);

            //this.contrast($("#contrast").val());
            //this.brightness($("#brightness").val());
            //this.exposure($("#exposure").val());
            //this.gamma($("#gamma").val());
            //this.hue($("#hue").val());
            //this.saturation($("#saturation").val());

            this.render();

        });

    });

    $("#invert").on("click", function() {

        if (dcm.invert)
            dcm.invert = false;
        else
            dcm.invert = true;

        Caman("#dcmview_image", function() {
            this.invert().render();
        });
    });

    $("#reset").on("click", function() {
        dcm.resetFilters();
    });

});

dcm.getFilters = function(context) {

    $(".filter").each(function() {

        var val = $(this).val();

        if (val == "" || (isNaN(val) && val.indexOf("-") == -1)) {
            val = 0;
            $(this).val("0");
        }

        context[$(this).attr("id")](val);

    });

    if (dcm.invert)
        context.invert();

};

dcm.resetFilters = function() {

    $(".filter").each(function() {

        if ($(this).attr("id") == "gamma")
            $(this).val("1");
        else
            $(this).val("0");

    });

    if (dcm.invert == true)
        dcm.invert = false;

    Caman("#dcmview_image", function() {
        this.revert();
        this.render();
    });

}

dcm.imageRender = function() {

    dcm.caman = Caman("#dcmview_image");
    console.log('imageRender');

}

dcm.reloadTags = function(first) {

    if (typeof first === "undefined")
        first = false;

	var tag_content = '<thead>' +
                        '<tr>' + 
                            '<th>Element</th>' + 
                            '<th>Value</th>' + 
                            '</tr>' + 
                      '</thead>' + 
                      '<tbody>';

	for (key in dcm.dicom) {

		if (dcm.dicom[key] !== "" || dcm.dicom[key] !== " ") {

			tag_content += '<tr>' + 
					  '	<td>' + key + '</td>' + 
					  '	<td>' + dcm.dicom[key].replace(/["']/g, "") + '</td>' + 
					  '</tr>';

		}

	}

    tag_content += '</tbody>';

    /*if (!first) {

        dcm.datatable.fnClearTable();
        $("#dcm").html(tag_content);
        dcm.datatable.fnDraw();

    } else {*/

        var options = {
            "bDestroy": true
        };

        //dataTables initialization
        $("#dcm").html(tag_content);
        dcm.datatable = $("#dcm").dataTable(options);

    //}

};

