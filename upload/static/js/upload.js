$(function() {

	$("#content").on("change", "input[name=new_or_existing]", function() {
		console.log('hide');
		if ($(this).val() == "new") {
			$("#new_dcm_title").show();
			$("#existing_dcm_title").hide();
		} else {
			$("#new_dcm_title").hide();
			$("#existing_dcm_title").show();
			$(".inp_dcm_title").select2();
		}

	});
	
});