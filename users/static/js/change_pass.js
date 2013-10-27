$(function() {

	//disable password update button on load
	$("#btn_pass_change").attr("disabled", "enabled");
	$("#btn_send_pass").attr("disabled", "enabled");

	$("#new_pass_conf").on("keyup", function(e) {

		var cpass = $("#new_pass");
		var ccpass = $("#new_pass_conf");

		//check new password and password confirm are identical
		if (cpass.val() == ccpass.val()) {

			cpass.parent().parent().removeClass("error").addClass("success");
			cpass.parent().find("span").html("Passwords match");

			ccpass.parent().parent().removeClass("error").addClass("success");
			ccpass.parent().find("span").html("Passwords match");

			$("#btn_pass_change").removeAttr("disabled");

		} else {

			cpass.parent().parent().removeClass("success").addClass("error");
			cpass.parent().find("span").html("Passwords do not match");

			ccpass.parent().parent().removeClass("success").addClass("error");
			ccpass.parent().find("span").html("Passwords do not match");

			$("#btn_pass_change").attr("disabled", "enabled");

		}

	});

	$("#user_email").on("keyup", function(e) {

		if ($("#user_email").val() != "" && $("#user_email").val() != " ")
			$("#btn_send_pass").removeAttr("disabled");
		else
			$("#btn_send_pass").attr("disabled", "enabled");

	});

	$("#btn_send_pass").on("click", function(e) {
		
		e.preventDefault();

		$.ajax({
			"url": "/users/sendPass",
			"type": "POST",
			"dataType": "json",
			"data": {
				"user_email": $("#user_email").val()
			},
			"success": function(res) {

				if (res.success) {

					$("#change_pass_response").removeClass("alert-error").addClass("alert-success").html(res.msg);

					$("#btn_send_pass").attr("disabled", "enabled");

				} else {

					$("#change_pass_response").removeClass("alert-success").addClass("alert-error").html(res.msg);

				}

			}
		});

	});

	$("#btn_pass_change").on("click", function(e) {

		e.preventDefault();

		data = {
			"new_pass": $("#new_pass").val()
		}

		if ($("#req_email").length > 0) {
			data.email = $("#req_email").val()
		} else {
			data.cur_pass = $("#cur_pass").val()
		}

		$.ajax({
			"url": "/users/chngPassConfirm",
			"type": "POST",
			"dataType": "json",
			"data": data,
			"success": function(res) {

				if (res.success) {

					$("#change_pass_response").removeClass("alert-error").addClass("alert-success").html(res.msg);

					$("#btn_pass_change").attr("disabled", "enabled");

				} else {

					$("#change_pass_response").removeClass("alert-success").addClass("alert-error").html(res.msg);

				}

			}
		});

	});

});