$(function() {

    dcm.reloadTags(true);

    if (dcm.image_gen) {

        dcm.invert = false;
        dcm.greyscale = false;

        dcm.cm_arr = [];

        $(".sliders").slider({
            "min": -100,
            "max": 100,
            "animate": "slow",
            "stop": function(event, ui) {

                Caman("#" + dcm.getActiveImg(), function() {

                    dcm.applyFilters(this);

                });

            }
        });

        $(".sliders").each(function() {

            if ($(this).attr("id") == "gamma") {
                $(this).slider("value", 1);
                $(this).slider("option", "min", 0);
                $(this).slider("option", "max", 5);
                $(this).slider("option", "step", 0.1);
            } else {
                $(this).slider("value", 0);
            }

            if ($(this).attr("id") == "hue") {
                $(this).slider("option", "min", 0);
                $(this).slider("option", "max", 100);
            }

        });

        Caman.Event.listen("processComplete", function(job) {
            console.log(job.name);
            $("#dcmview_status").html(job.name);
        });

        Caman.Event.listen("renderFinished", function() {
            $("#dcmview_status").html("Render finished!");
        });

    	$(".dcm_series").on("click", function(e) {

            $("#dcmview_status").html("Loading ...");

    		e.preventDefault();

    		var switch_img = $(this).find("img").attr("fname");

            if ($("#dcmview_image").length > 0 && !$("#dcmview_image").is(":hidden"))
                $("#dcmview_image").hide();
            else
                $(".preload_dcm").hide();

            $("#dcm_" + switch_img).show();

            var found_img = false;

            for (var i = 0; i < dcm.cm_arr.length; i++)
                if (dcm.cm_arr[i] == switch_img)
                    found_img = true;

            if (!found_img) {

                Caman("#dcm_" + switch_img, function() {
                    
                    dcm.applyFilters(this);

                    $("#dcmview_status").html("Applying filters ...");

                    dcm.cm_arr.push(switch_img);

                });

            }

    	});

        $("#invert").on("click", function() {

            if (dcm.invert)
                dcm.invert = false;
            else
                dcm.invert = true;

            Caman("#" + dcm.getActiveImg(), function() {
                this.invert().render();
            });
        });

        $("#greyscale").on("click", function() {

            if (dcm.greyscale)
                dcm.greyscale = false;
            else
                dcm.greyscale = true;

            Caman("#" + dcm.getActiveImg(), function() {
                this.greyscale().render();
            });
        });

        $("#reset").on("click", function() {
            dcm.resetFilters();
        });

    }

});

dcm.getActiveImg = function() {

    if (!$("#dcmview_image").is(":hidden")) {

        return "dcmview_image";

    } else {

        var tag = null;

        $(".preload_dcm").each(function() {
            if (!$(this).is(":hidden")) {
                tag = $(this).attr("id");
            }

        });

        return tag;

    }

};

dcm.applyFilters = function(that) {

    var sliders = [];

    $(".sliders").each(function() {

        var type = $(this).attr("id");
        var val = $(this).slider("value");

        if ((type != "gamma" && val != 0) || (type == "gamma" && val != 1)) {
            console.log(type + " made it w " + val);
            sliders.push({
                "type": type,
                "val": val
            });
        }

    });

    that.revert();

    for (var i = 0; i < sliders.length; i++) {
        var filter = sliders[i];
        that[filter.type](filter.val);
    }

    that.render();
};

dcm.resetFilters = function() {

    $(".sliders").each(function() {

        if ($(this).attr("id") == "gamma")
            $(this).slider("value", 1);
        else
            $(this).slider("value", 0);

    });

    if (dcm.invert == true)
        dcm.invert = false;

    Caman("#" + dcm.getActiveImg(), function() {
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

