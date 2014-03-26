$(function() {

		dcm.reloadTags(true);

		if (dcm.image_gen) {

				dcm.invert = false;
				dcm.greyscale = false;

				dcm.cm_arr = [];

				$("#filters_menu").hide();

				$("#filters_on").on("click", function() {

					if ($(this).is(":checked")) {

						$("#filters_menu").show();
						
						if (window.navigator.appName == "Microsoft Internet Explorer") {

							Caman("#" + dcm.getActiveImg(), function() {
									//this.revert();
									this.render();
							});

							$("#" + dcm.getActiveImg()).css("width", "500px");
							$("#" + dcm.getActiveImg()).css("height", "500px");

						}

					} else {
						$("#filters_menu").hide();
					}

				});

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
						$("#viewer_status").html(job.name);
				});

				Caman.Event.listen("renderFinished", function() {
						$("#viewer_status").html("Render finished!");
				});

			$(".dcm_series").on("click", function(e) {

				/*if (window.navigator.appName == "Microsoft Internet Explorer") {

					window.location = $(this).attr("src");

				} else {*/

					e.preventDefault();

					var switch_img = $(this).find("img").attr("fname");

					if ($("#viewer_image").length > 0 && !$("#viewer_image").is(":hidden"))
							$("#viewer_image").hide();
					else
							$(".preload_dcm").hide();

					$("#dcm_" + switch_img).show();

					var found_img = false;

					for (var i = 0; i < dcm.cm_arr.length; i++)
							if (dcm.cm_arr[i] == switch_img)
									found_img = true;

					if (!found_img && $("#filters_on").is(":checked")) {

						$("#viewer_status").html("Loading ...");

						Caman("#dcm_" + switch_img, function() {

								dcm.applyFilters(this);

								$("#viewer_status").html("Applying filters ...");

								dcm.cm_arr.push(switch_img);

						});

					}

				//}

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
								dcm.applyFilters(this);
						});
				});

				$("#reset").on("click", function() {
						dcm.resetFilters();
				});

				dcm.zoomd = false;

				$("#zoom").on("click", function() {

						var cont = $("#dcm_cont");

						if (!dcm.zoomd) {

								dcm.zoomd = true;
								$(this).removeClass("glyphicon-zoom-in").addClass("glyphicon-zoom-out");
								cont.find("img").css("width", "100%");
								cont.find("canvas").css("width", "100%");

						} else {

								dcm.zoomd = false;
								$(this).removeClass("glyphicon-zoom-out").addClass("glyphicon-zoom-in");
								cont.find("img").css("width", "auto");
								cont.find("canvas").css("width", "auto");

						}

				});

		}

});

dcm.getActiveImg = function() {

		if (!$("#viewer_image").is(":hidden")) {

				return "viewer_image";

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

		if (dcm.invert)
				that.invert();

		if (dcm.greyscale)
				that.greyscale();

		that.render();
};

dcm.resetFilters = function() {

		$(".sliders").each(function() {

				if ($(this).attr("id") == "gamma")
						$(this).slider("value", 1);
				else
						$(this).slider("value", 0);

		});

		if (dcm.invert)
				dcm.invert = false;

		if (dcm.greyscale)
				dcm.greyscale = false;

		Caman("#" + dcm.getActiveImg(), function() {
				this.revert();
				this.render();
		});

}

dcm.reloadTags = function(first) {

		if (typeof first === "undefined")
				first = false;

	var tag_content = '<table id="dcm" class="table table-striped"><thead>' +
												'<tr>' + 
														'<th>Element</th>' + 
														'<th>Value</th>' + 
														'</tr>' + 
											'</thead>' + 
											'<tbody>';

	for (key in dcm.dicom) {

		var value = dcm.sanitizeTags(dcm.dicom[key]);

		if (value != "" || value != " ") {

			tag_content += '<tr>' + 
						'	<td>' + key + '</td>' + 
						'	<td>' + value + '</td>' + 
						'</tr>';

		}

	}

		tag_content += '</tbody></table>';

		var options = {
				"bDestroy": true
		};

		//dataTables initialization
		$("#data").html(tag_content);
		dcm.datatable = $("#dcm").dataTable(options);

};

dcm.sanitizeTags = function(value) {

	return value.toString().replace(/["']/g, '').replace(/[^\w\s]/gi, '').replace(/x00/g, '');

}
