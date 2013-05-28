$(function() {

	$("#content").on("change", "input[name=new_or_existing]", function() {

		if ($(this).val() == "new") {

			$("#new_dcm_title").show();
			$("#existing_dcm_title").hide();
			//Setting create a bool from string to determine if DICOM is part of new study GOTO 17
			$("#new_study").val("true");

		} else {

			$("#new_dcm_title").hide();
			$("#existing_dcm_title").show();
			$(".inp_dcm_title").select2();
			//or an existing study
			$("#new_study").val("false");

		}

	});
	
});