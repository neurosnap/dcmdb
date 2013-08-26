$(function() {
	
	$("#email_validate_info").hide();

	$("#email_validate").on("click", function(e) {

		$.ajax({
			"url": "/users/sendValidation",
			"type": "GET",
			"dataType": "json",
			"success": function(res) {

				$("#email_validate_info").show();
				
				if (res.success) {
					$("#email_validate_info").addClass("alert-success").find("span").html(res.msg);
				} else {
					$("#email_validate_info").addClass("alert-error").find("span").html(res.msg);
				}

			}
		});

	});

});