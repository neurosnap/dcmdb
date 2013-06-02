$(function() {

	var first = true;

	$("#content").on("change", "input[name=new_or_existing]", function() {

		console.log($(this).val());

		if ($(this).val() == "new") {

			$("#new_dcm_title").show();
			$("#existing_dcm_title").hide();
			//Setting create a bool from string to determine if DICOM is part of new study GOTO 17
			$("#new_study").val("true");
			$("#status_radio").show();

		} else {

			$("#new_dcm_title").hide();
			$("#existing_dcm_title").show();

			if (first) {
				$(".inp_dcm_title").select2();
				first = false;
			}
			
			//or an existing study
			$("#new_study").val("false");
			$("#status_radio").hide();

		}

	});

	if (existing_studies.length == 0) {

		$("#new_exist input:radio:first").click();

		$("input[name=new_or_existing]").attr("disabled", true);

	}
	
});