$(function() {

    dcm.reloadTags(true);

    if (dcm.image_gen) {

        dcm.invert = false;

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

    	});

        $("#apply").on("click", function(e) {

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

    }

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

    var options = {
        "bDestroy": true
    };

    //dataTables initialization
    $("#dcm").html(tag_content);
    dcm.datatable = $("#dcm").dataTable(options);

};

